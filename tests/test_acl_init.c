#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <assert.h>

#define ICACHE_FLASH_ATTR
#define os_sprintf sprintf
#define os_memcpy memcpy

// Mock types
struct pbuf { uint16_t len; void *payload; };
struct eth_hdr { uint16_t type; };
struct ip_hdr_dummy { struct { uint32_t addr; } src, dest; };
#define ip_hdr ip_hdr_dummy
struct udp_hdr { uint16_t src; uint16_t dest; };
struct tcp_hdr { uint16_t src; uint16_t dest; };
#define ETHTYPE_ARP 0x0806
#define ETHTYPE_IP  0x0800
#define IP_PROTO_UDP 17
#define IP_PROTO_TCP 6
#define IP_PROTO_ICMP 1
#define IPH_PROTO(ip_h) 17

typedef struct ip_addr {
    uint32_t addr;
} ip_addr_t;

#define IP2STR(addr) 0,0,0,0

uint16_t ntohs(uint16_t n) { return n; }
uint32_t ntohl(uint32_t n) { return n; }

// Dummy macros for user/acl.c
#define os_printf(...)

// Include the entire C file directly to access its statics and globals seamlessly
#include "user/acl.c"

void test_acl_init() {
    // 1. Setup - dirty the state
    acl_allow_count = 10;
    acl_deny_count = 20;
    my_deny_cb = (packet_deny_cb)1;

    for (int i = 0; i < MAX_NO_ACLS; i++) {
        acl_freep[i] = 5;
        for (int j = 0; j < MAX_ACL_ENTRIES; j++) {
            acl[i][j].hit_count = 100;
        }
    }

    // 2. Execute
    acl_init();

    // 3. Verify
    assert(acl_allow_count == 0);
    assert(acl_deny_count == 0);
    assert(my_deny_cb == NULL);

    for (int i = 0; i < MAX_NO_ACLS; i++) {
        assert(acl_freep[i] == 0);
        for (int j = 0; j < MAX_ACL_ENTRIES; j++) {
            assert(acl[i][j].hit_count == 0);
        }
    }
    printf("test_acl_init passed!\n");
}

int main() {
    test_acl_init();
    return 0;
}

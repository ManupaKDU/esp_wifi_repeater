#include <stdio.h>
#include <assert.h>

#define ICACHE_FLASH_ATTR

typedef char I8;
typedef unsigned char U8;
typedef short I16;
typedef unsigned short U16;
typedef long I32;
typedef unsigned long U32;
typedef unsigned long long U64;

#define NULL ((void *)0)

// Dummy os_type.h to satisfy includes when testing without the full ESP SDK
#define _OS_TYPE_H_
#define os_type_h_dummy

// Include the actual source file to test the real implementation
// We create a temporary dummy file to satisfy the missing os_type.h include in ringbuf_mqtt.h
#include "ringbuf_mqtt.c"

void test_ringbuf_put_error_handling() {
    RINGBUF rb;
    U8 buf[2];

    // Test initialization
    I16 ret = RINGBUF_Init(&rb, buf, 2);
    assert(ret == 0);

    // Fill the buffer to capacity
    ret = RINGBUF_Put(&rb, 'A');
    assert(ret == 0);
    assert(rb.fill_cnt == 1);

    ret = RINGBUF_Put(&rb, 'B');
    assert(ret == 0);
    assert(rb.fill_cnt == 2);

    // Verify RINGBUF_Put handles overflow gracefully (should return -1)
    ret = RINGBUF_Put(&rb, 'C');
    assert(ret == -1);

    // Verify the state of the buffer hasn't been corrupted
    assert(rb.fill_cnt == 2);

    printf("test_ringbuf_put_error_handling passed!\n");
}

int main() {
    test_ringbuf_put_error_handling();
    return 0;
}

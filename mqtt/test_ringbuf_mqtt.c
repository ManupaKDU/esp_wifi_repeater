#include <stdio.h>
#include <assert.h>

#ifndef __ets__
#ifndef ICACHE_FLASH_ATTR
#define ICACHE_FLASH_ATTR
#endif
#endif

// We need to ensure that ICACHE_FLASH_ATTR is defined as nothing when we are compiling locally (where __ets__ is not defined).
// If __ets__ is defined (like in the ESP8266 SDK during CI build), it's important that we don't redefine it.
// The ESP8266 SDK defines it via <c_types.h> which is eventually included by "ringbuf_mqtt.c".
// Thus, if __ets__ is NOT defined, we defined it as empty above. If it IS defined, we let the SDK define it.

typedef char I8;
typedef unsigned char U8;
typedef short I16;
typedef unsigned short U16;
typedef long I32;
typedef unsigned long U32;
typedef unsigned long long U64;

#define NULL ((void *)0)

// Dummy os_type.h to satisfy includes when testing without the full ESP SDK
#ifndef __ets__
#ifndef _OS_TYPE_H_
#define _OS_TYPE_H_
#define os_type_h_dummy
#endif
#endif

// Before we include ringbuf_mqtt.c, we need to make sure os_type.h is either mocked or available.
// If compiling without __ets__ (e.g. gcc test), we will create a dummy os_type.h dynamically in the Makefile,
// or we can rely on it being present in the SDK during CI.

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

#ifndef __ets__
    printf("test_ringbuf_put_error_handling passed!\n");
#endif
}

#ifndef __ets__
int main() {
    test_ringbuf_put_error_handling();
    return 0;
}
#endif

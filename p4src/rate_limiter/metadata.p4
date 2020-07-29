#ifndef _METADATA_
#define _METADATA_

struct metadata_t {
    bit<16> tcpLength;
    bit<16> applLength;
    flowblaze_t flowblaze_metadata;
}

#endif
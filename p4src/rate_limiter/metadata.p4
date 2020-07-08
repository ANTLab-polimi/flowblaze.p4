#ifndef _METADATA_
#define _METADATA_

struct metadata_t {
    bit<16> tcpLength;
    bit<16> applLength;
    OPP_t opp_metadata;
}

#endif
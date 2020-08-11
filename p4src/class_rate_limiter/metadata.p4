#ifndef _METADATA_
#define _METADATA_

struct metadata_t {
    bit<16> l4Length;
    //  -------------- FLOWBLAZE metadata ----------------------------
    flowblaze_t flowblaze_metadata;
    // ---------------------------------------------------------------
}

#endif
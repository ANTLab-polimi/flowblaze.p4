#ifndef _OPP_METADATA_
#define _OPP_METADATA_

# This file container the custom metadata needed for the OPP Loop to work

struct OPP_single_update_t {
    bit<8>  operation;
    bit<8>  result;
    bit<8>  op1;
    bit<8>  op2;
    bit<32> operand1;
    bit<32> operand2;
}

struct OPP_update_block_t {
    OPP_single_update_t u_block_0;
    OPP_single_update_t u_block_1;
}

struct OPP_single_condition_t {
    bit<3> cond;
    bit<8> op1;
    bit<8> op2;
    bit<32> operand1;
    bit<32> operand2;
}

struct OPP_condition_block_t {
    OPP_single_condition_t c_block_0;
    OPP_single_condition_t c_block_1;
    OPP_single_condition_t c_block_2;
    OPP_single_condition_t c_block_3;
}

struct OPP_t {
    bit<32> lookup_state_index;
    bit<32> update_state_index;
    bit<16> state;
    bit<32> R0;
    bit<32> R1;
    bit<32> R2;
    bit<32> R3;
    bit<32> G0;
    bit<32> G1;
    bit<32> G2;
    bit<32> G3;
    bit<1>  c0;
    bit<1>  c1;
    bit<1>  c2;
    bit<1>  c3;
    bit<8>  pkt_action;
    bit<32> pkt_data; // Data related to packet header or metadata that can be used as operand in an operation
    OPP_update_block_t update_block;
    OPP_condition_block_t condition_block;   
}

#endif

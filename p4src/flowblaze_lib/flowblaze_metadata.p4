/*
* Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
*                Davide Sanvito <davide.sanvito@neclab.eu>
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

#ifndef _FLOWBLAZE_METADATA_
#define _FLOWBLAZE_METADATA_

# This file contains the custom metadata needed for FlowBlaze to work

struct flowblaze_single_update_t {
    bit<8>  operation;
    bit<8>  result;
    bit<8>  op1;
    bit<8>  op2;
    bit<32> operand1;
    bit<32> operand2;
}

struct flowblaze_update_block_t {
    flowblaze_single_update_t u_block_0;
    flowblaze_single_update_t u_block_1;
    flowblaze_single_update_t u_block_2;
}

struct flowblaze_single_condition_t {
    bit<3> cond;
    bit<8> op1;
    bit<8> op2;
    bit<32> operand1;
    bit<32> operand2;
}

struct flowblaze_condition_block_t {
    flowblaze_single_condition_t c_block_0;
    flowblaze_single_condition_t c_block_1;
    flowblaze_single_condition_t c_block_2;
    flowblaze_single_condition_t c_block_3;
}

struct flowblaze_t {
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
    flowblaze_update_block_t update_block;
    flowblaze_condition_block_t condition_block;
}

#endif

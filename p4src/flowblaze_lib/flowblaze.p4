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

#ifndef _FLOWBLAZE_LIB_
#define _FLOWBLAZE_LIB_

// Useful for using flowblaze.p4 with fabric.p4
#ifndef FABRIC
#define METADATA_NAME metadata_t
#define HEADER_NAME headers
#endif

#define _NO_OP 0x00
#define _PLUS 0x01
#define _MINUS 0x02
#define _R_SHIFT 0x03
#define _L_SHIFT 0x04
#define _MUL 0x05

#define _R0 0x00
#define _R1 0x01
#define _R2 0x02
#define _R3 0x03

#define _G0 0x0F
#define _G1 0x1F
#define _G2 0x2F
#define _G3 0x3F

#define _META 0xF1
#define _TIME_NOW 0xF2
#define _EXPL 0xFF

#define NO_CONDITION    0b000
#define CONDITION_EQ    0b001
#define CONDITION_GT    0b010
#define CONDITION_GTE   0b011
#define CONDITION_LT    0b100
#define CONDITION_LTE   0b101

#ifndef CONTEXT_TABLE_SIZE
    #define CONTEXT_TABLE_SIZE 2014
#endif


// Global Data Variable: 4
register<bit<32>>(4) reg_G;

// 4 Flow Registers
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R0;
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R1;
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R2;
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R3;

// Register that stores the state of the flows
register<bit<16>>(CONTEXT_TABLE_SIZE) reg_state;

control ConditionBlock(inout flowblaze_single_condition_t meta_c_blk,
                       inout flowblaze_t flowblaze_metadata,
                       in standard_metadata_t standard_metadata,
                       out bit<1> c) {
    apply {
        c = 0;
        if(meta_c_blk.cond != NO_CONDITION){
            // Set operand 1
            if(meta_c_blk.op1 == _R0) {
                meta_c_blk.operand1 = flowblaze_metadata.R0;
            }
            if(meta_c_blk.op1 == _R1) {
                meta_c_blk.operand1 = flowblaze_metadata.R1;
            }
            if(meta_c_blk.op1 == _R2) {
                meta_c_blk.operand1 = flowblaze_metadata.R2;
            }
            if(meta_c_blk.op1 == _R3) {
                meta_c_blk.operand1 = flowblaze_metadata.R3;
            }
            if(meta_c_blk.op1 == _G0) {
                meta_c_blk.operand1 = flowblaze_metadata.G0;
            }
            if(meta_c_blk.op1 == _G1) {
                meta_c_blk.operand1 = flowblaze_metadata.G1;
            }
            if(meta_c_blk.op1 == _G2) {
                meta_c_blk.operand1 = flowblaze_metadata.G2;
            }
            if(meta_c_blk.op1 == _G3) {
                meta_c_blk.operand1 = flowblaze_metadata.G3;
            }
            if(meta_c_blk.op1 == _META) {
                meta_c_blk.operand1 = flowblaze_metadata.pkt_data;
            }
            if(meta_c_blk.op1 == _TIME_NOW) {
                meta_c_blk.operand1 = (bit<32>) standard_metadata.ingress_global_timestamp;
            }
            // EXPLICIT IS THE DEFAULT BEHAVIOUR
            //if(meta_c_blk.op1 == _EXPL) {
            //    meta_c_blk.operand1 = meta_c_blk.operand1
            //}

            // Set operand 2
            if(meta_c_blk.op2 == _R0) {
                meta_c_blk.operand2 = flowblaze_metadata.R0;
            }
            if(meta_c_blk.op2 == _R1) {
                meta_c_blk.operand2 = flowblaze_metadata.R1;
            }
            if(meta_c_blk.op2 == _R2) {
                meta_c_blk.operand2 = flowblaze_metadata.R2;
            }
            if(meta_c_blk.op2 == _R3) {
                meta_c_blk.operand2 = flowblaze_metadata.R3;
            }
            if(meta_c_blk.op2 == _G0) {
                meta_c_blk.operand2 = flowblaze_metadata.G0;
            }
            if(meta_c_blk.op2 == _G1) {
                meta_c_blk.operand2 = flowblaze_metadata.G1;
            }
            if(meta_c_blk.op2 == _G2) {
                meta_c_blk.operand2 = flowblaze_metadata.G2;
            }
            if(meta_c_blk.op2 == _G3) {
                meta_c_blk.operand2 = flowblaze_metadata.G3;
            }
            if(meta_c_blk.op2 == _META) {
                meta_c_blk.operand2 = flowblaze_metadata.pkt_data;
            }
            if(meta_c_blk.op2 == _TIME_NOW) {
                meta_c_blk.operand2 = (bit<32>) standard_metadata.ingress_global_timestamp;
            }
            // EXPLICIT IS THE DEFAULT BEHAVIOUR
            //if(meta_c_blk.op2 == _EXPL) {
            //    meta_c_blk.operand1 = meta_c_blk.operand2
            //}

            if(meta_c_blk.cond == CONDITION_EQ) {
                c = (bit<1>) ( meta_c_blk.operand1 == meta_c_blk.operand2);
            }
            if(meta_c_blk.cond == CONDITION_GT) {
                c = (bit<1>) ( meta_c_blk.operand1 > meta_c_blk.operand2);
            }
            if(meta_c_blk.cond == CONDITION_GTE) {
                c = (bit<1>) ( meta_c_blk.operand1 >= meta_c_blk.operand2);
            }
            if(meta_c_blk.cond == CONDITION_LT) {
                c = (bit<1>) ( meta_c_blk.operand1 < meta_c_blk.operand2);
            }
            if(meta_c_blk.cond == CONDITION_LTE) {
                c = (bit<1>) ( meta_c_blk.operand1 <= meta_c_blk.operand2);
            }
        }
    }

}


// ----------------------- UPDATE LOGIC BLOCK ----------------------------------
control UpdateLogic(inout HEADER_NAME hdr,
                    inout flowblaze_t flowblaze_metadata,
                    inout flowblaze_single_update_t update_block,
                    in standard_metadata_t standard_metadata) {

    apply{
        // Calculate update lookup index
        // TODO: (improvement) save hash in metadata when calculated for reading registers
        hash(flowblaze_metadata.update_state_index,
             HashAlgorithm.crc32,
             (bit<32>) 0,
             FLOW_SCOPE,
             (bit<32>) CONTEXT_TABLE_SIZE);
        // Update state using the update lookup index
        reg_state.write(flowblaze_metadata.update_state_index, flowblaze_metadata.state);

        // Check if an operation is requested and then extract operands and operation
        if(update_block.operation != _NO_OP){
            // Set the operand 1
            if(update_block.op1 == _R0) {
                update_block.operand1 = flowblaze_metadata.R0;
            }
            if(update_block.op1 == _R1) {
                update_block.operand1 = flowblaze_metadata.R1;
            }
            if(update_block.op1 == _R2) {
                update_block.operand1 = flowblaze_metadata.R2;
            }
            if(update_block.op1 == _R3) {
                update_block.operand1 = flowblaze_metadata.R3;
            }
            if(update_block.op1 == _G0) {
                update_block.operand1 = flowblaze_metadata.G0;
            }
            if(update_block.op1 == _G1) {
                update_block.operand1 = flowblaze_metadata.G1;
            }
            if(update_block.op1 == _G2) {
                update_block.operand1 = flowblaze_metadata.G2;
            }
            if(update_block.op1 == _G3) {
                update_block.operand1 = flowblaze_metadata.G3;
            }
            if(update_block.op1 == _META) {
                update_block.operand1 = flowblaze_metadata.pkt_data;
            }
            if(update_block.op1 == _TIME_NOW) {
                update_block.operand1 = (bit<32>) standard_metadata.ingress_global_timestamp;
            }
            // EXPLICIT IS THE DEFAULT BEHAVIOUR
            //if(flowblaze_metadata.op1 == _EXPL) {
            //    flowblaze_metadata.operand1 = flowblaze_metadata.operand1
            //}

            // Set the operand 2
            if(update_block.op2 == _R0) {
               update_block.operand2 = flowblaze_metadata.R0;
            }
            if(update_block.op2 == _R1) {
                update_block.operand2 = flowblaze_metadata.R1;
            }
            if(update_block.op2 == _R2) {
                update_block.operand2 = flowblaze_metadata.R2;
            }
            if(update_block.op2 == _R3) {
                update_block.operand2 = flowblaze_metadata.R3;
            }
            if(update_block.op2 == _G0) {
                update_block.operand2 = flowblaze_metadata.G0;
            }
            if(update_block.op2 == _G1) {
                update_block.operand2 = flowblaze_metadata.G1;
            }
            if(update_block.op2 == _G2) {
                update_block.operand2 = flowblaze_metadata.G2;
            }
            if(update_block.op2 == _G3) {
                update_block.operand2 = flowblaze_metadata.G3;
            }
            if(update_block.op2 == _META) {
                update_block.operand2 = flowblaze_metadata.pkt_data;
            }
             if(update_block.op2 == _TIME_NOW) {
                update_block.operand2 = (bit<32>) standard_metadata.ingress_global_timestamp;
            }
            // EXPLICIT IS THE DEFAULT BEHAVIOUR
            //if(flowblaze_metadata.op2 == _EXPL) {
            //    flowblaze_metadata.operand2 = flowblaze_metadata.operand2
            //}

            // Do the actual operation
            bit<32> t_result = 0;
            bit<1> op_done= 0b0;
            if(update_block.operation == _PLUS) {
                t_result = update_block.operand1 + update_block.operand2;
                op_done = 0b1;
            }
            if(update_block.operation == _MINUS) {
                t_result = update_block.operand1 - update_block.operand2;
                op_done = 0b1;
            }
            if(update_block.operation == _R_SHIFT) {
                t_result = update_block.operand1 >> (bit<8>) update_block.operand2;
                op_done = 0b1;
            }
            if(update_block.operation == _L_SHIFT) {
                t_result = update_block.operand1 << (bit<8>) update_block.operand2;
                op_done = 0b1;
            }
            if(update_block.operation == _MUL) {
                t_result = update_block.operand1 * update_block.operand2;
                op_done = 0b1;
            }

            // Update the result on the correct register
            if (op_done == 0b1){
                if(update_block.result == _R0) {
                    reg_R0.write(flowblaze_metadata.update_state_index, t_result);
                }
                if(update_block.result == _R1) {
                    reg_R1.write(flowblaze_metadata.update_state_index, t_result);
                }
                if(update_block.result == _R2) {
                    reg_R2.write(flowblaze_metadata.update_state_index, t_result);
                }
                if(update_block.result == _R3) {
                    reg_R3.write(flowblaze_metadata.update_state_index, t_result);
                }

                if(update_block.result == _G0) {
                    reg_G.write(0, t_result);
                }
                if(update_block.result == _G1) {
                    reg_G.write(1, t_result);
                }
                if(update_block.result == _G2) {
                    reg_G.write(2, t_result);
                }
                if(update_block.result == _G3) {
                    reg_G.write(3, t_result);
                }
            }
        }
    }
}
// ------------------------------------------------------------------------------------

control FlowBlaze (inout HEADER_NAME hdr,
                 inout METADATA_NAME meta,
                 inout standard_metadata_t standard_metadata){
    // ------------------------ EFSM TABLE -----------------------------
    @name(".FlowBlaze.define_operation_update_state")
    action define_operation_update_state(bit<16> state,
                                         bit<8> operation_0,
                                         bit<8> result_0,
                                         bit<8> op1_0,
                                         bit<8> op2_0,
                                         bit<32> operand1_0,
                                         bit<32> operand2_0,
                                         bit<8> operation_1,
                                         bit<8> result_1,
                                         bit<8> op1_1,
                                         bit<8> op2_1,
                                         bit<32> operand1_1,
                                         bit<32> operand2_1,
                                         bit<8> operation_2,
                                         bit<8> result_2,
                                         bit<8> op1_2,
                                         bit<8> op2_2,
                                         bit<32> operand1_2,
                                         bit<32> operand2_2,
                                         bit<8> pkt_action
                                         ) {

        // Update the state
        meta.flowblaze_metadata.state = state;

        // Set the packet action to be applied by the main P4 Program,
        //   in this way the user can define arbitrary action to be applied to packet.
        meta.flowblaze_metadata.pkt_action = pkt_action;

        // Set operation 1: result = operation(op1, op2)
        meta.flowblaze_metadata.update_block.u_block_0.operation = operation_0;
        meta.flowblaze_metadata.update_block.u_block_0.result = result_0;
        meta.flowblaze_metadata.update_block.u_block_0.op1 = op1_0;
        meta.flowblaze_metadata.update_block.u_block_0.op2 = op2_0;
        meta.flowblaze_metadata.update_block.u_block_0.operand1 = operand1_0;
        meta.flowblaze_metadata.update_block.u_block_0.operand2 = operand2_0;

        // Set operation 2: result = operation(op1, op2)
        meta.flowblaze_metadata.update_block.u_block_1.operation = operation_1;
        meta.flowblaze_metadata.update_block.u_block_1.result = result_1;
        meta.flowblaze_metadata.update_block.u_block_1.op1 = op1_1;
        meta.flowblaze_metadata.update_block.u_block_1.op2 = op2_1;
        meta.flowblaze_metadata.update_block.u_block_1.operand1 = operand1_1;
        meta.flowblaze_metadata.update_block.u_block_1.operand2 = operand2_1;

        // Set operation 3: result = operation(op1, op2)
        meta.flowblaze_metadata.update_block.u_block_2.operation = operation_2;
        meta.flowblaze_metadata.update_block.u_block_2.result = result_2;
        meta.flowblaze_metadata.update_block.u_block_2.op1 = op1_2;
        meta.flowblaze_metadata.update_block.u_block_2.op2 = op2_2;
        meta.flowblaze_metadata.update_block.u_block_2.operand1 = operand1_2;
        meta.flowblaze_metadata.update_block.u_block_2.operand2 = operand2_2;
    }

    @name(".FlowBlaze.EFSM_table_counter")
    direct_counter(CounterType.packets_and_bytes) EFSM_table_counter;
    @name(".FlowBlaze.EFSM_table")
    table EFSM_table {
        actions = {
            define_operation_update_state;
            NoAction;
        }
        key = {
            meta.flowblaze_metadata.state                : ternary @name("FlowBlaze.state");
            meta.flowblaze_metadata.c0                   : ternary @name("FlowBlaze.condition0");
            meta.flowblaze_metadata.c1                   : ternary @name("FlowBlaze.condition1");
            meta.flowblaze_metadata.c2                   : ternary @name("FlowBlaze.condition2");
            meta.flowblaze_metadata.c3                   : ternary @name("FlowBlaze.condition3");
            #ifdef EFSM_MATCH_FIELDS
                EFSM_MATCH_FIELDS
            #endif
        }
        default_action = NoAction;
        counters = EFSM_table_counter;
    }
    // ------------------------------------------------------------------------

    // ----------------------------- CONTEXT LOOKUP ---------------------------
    @name(".FlowBlaze.lookup_context_table")
    action lookup_context_table() {
        // Calculate lookup index
        hash(meta.flowblaze_metadata.lookup_state_index,
             HashAlgorithm.crc32,
             (bit<32>) 0,
             FLOW_SCOPE,
             (bit<32>)CONTEXT_TABLE_SIZE);

        // Extract the state and all the registers related to the current lookup
        reg_state.read(meta.flowblaze_metadata.state, meta.flowblaze_metadata.lookup_state_index);
        reg_R0.read(meta.flowblaze_metadata.R0, meta.flowblaze_metadata.lookup_state_index);
        reg_R1.read(meta.flowblaze_metadata.R1, meta.flowblaze_metadata.lookup_state_index);
        reg_R2.read(meta.flowblaze_metadata.R2, meta.flowblaze_metadata.lookup_state_index);
        reg_R3.read(meta.flowblaze_metadata.R3, meta.flowblaze_metadata.lookup_state_index);

        // Extract also the global register
        reg_G.read(meta.flowblaze_metadata.G0, 0);
        reg_G.read(meta.flowblaze_metadata.G1, 1);
        reg_G.read(meta.flowblaze_metadata.G2, 2);
        reg_G.read(meta.flowblaze_metadata.G3, 3);
    }

    @name(".FlowBlaze.context_lookup_counter")
    direct_counter(CounterType.packets_and_bytes) context_lookup_counter;
    @name(".FlowBlaze.context_lookup")
    table context_lookup {
        actions = {
            lookup_context_table;
            NoAction;
        }
        default_action = lookup_context_table();
        counters = context_lookup_counter;
    }
    // --------------------------------------------------------------------------


    // -------------------------------- CONDITION TABLE -------------------------
    @name(".FlowBlaze.set_condition_fields")
    action set_condition_fields(bit<3> cond0,
                                bit<8> op1_0,
                                bit<8> op2_0,
                                bit<32> operand1_0,
                                bit<32> operand2_0,
                                bit<3> cond1,
                                bit<8> op1_1,
                                bit<8> op2_1,
                                bit<32> operand1_1,
                                bit<32> operand2_1,
                                bit<3> cond2,
                                bit<8> op1_2,
                                bit<8> op2_2,
                                bit<32> operand1_2,
                                bit<32> operand2_2,
                                bit<3> cond3,
                                bit<8> op1_3,
                                bit<8> op2_3,
                                bit<32> operand1_3,
                                bit<32> operand2_3) {
        meta.flowblaze_metadata.condition_block.c_block_0.cond = cond0;
        meta.flowblaze_metadata.condition_block.c_block_0.op1 = op1_0;
        meta.flowblaze_metadata.condition_block.c_block_0.op2 = op2_0;
        meta.flowblaze_metadata.condition_block.c_block_0.operand1 = operand1_0;
        meta.flowblaze_metadata.condition_block.c_block_0.operand2 = operand2_0;
        meta.flowblaze_metadata.condition_block.c_block_1.cond = cond1;
        meta.flowblaze_metadata.condition_block.c_block_1.op1 = op1_1;
        meta.flowblaze_metadata.condition_block.c_block_1.op2 = op2_1;
        meta.flowblaze_metadata.condition_block.c_block_1.operand1 = operand1_1;
        meta.flowblaze_metadata.condition_block.c_block_1.operand2 = operand2_1;
        meta.flowblaze_metadata.condition_block.c_block_2.cond = cond2;
        meta.flowblaze_metadata.condition_block.c_block_2.op1 = op1_2;
        meta.flowblaze_metadata.condition_block.c_block_2.op2 = op2_2;
        meta.flowblaze_metadata.condition_block.c_block_2.operand1 = operand1_2;
        meta.flowblaze_metadata.condition_block.c_block_2.operand2 = operand2_2;
        meta.flowblaze_metadata.condition_block.c_block_3.cond = cond3;
        meta.flowblaze_metadata.condition_block.c_block_3.op1 = op1_3;
        meta.flowblaze_metadata.condition_block.c_block_3.op2 = op2_3;
        meta.flowblaze_metadata.condition_block.c_block_3.operand1 = operand1_3;
        meta.flowblaze_metadata.condition_block.c_block_3.operand2 = operand2_3;
    }

    @name(".FlowBlaze.condition_table_counter")
    direct_counter(CounterType.packets_and_bytes) condition_table_counter;
    @name(".FlowBlaze.condition_table")
    table condition_table {
        actions = {
            set_condition_fields;
            NoAction;
        }
        default_action = NoAction;
        counters = condition_table_counter;
    }

    #ifdef CUSTOM_ACTIONS_DEFINITION
        CUSTOM_ACTIONS_DEFINITION
    #endif

    @name(".FlowBlaze.pkt_action_counter")
    direct_counter(CounterType.packets_and_bytes) pkt_action_counter;
    @name(".FlowBlaze.pkt_action")
    table pkt_action {
        key = {
            // TODO: we can use exact match instead of ternary
            meta.flowblaze_metadata.pkt_action : ternary @name("FlowBlaze.pkt_action");
        }
        actions = {
            #ifdef CUSTOM_ACTIONS_DECLARATION
                CUSTOM_ACTIONS_DECLARATION
            #endif
            NoAction;
        }
        // Keep NoAction as default action
        default_action = NoAction();
        counters = pkt_action_counter;
    }
    // --------------------------------------------------------------------------


    UpdateLogic() update_logic;
    ConditionBlock() condition_block;
    apply {
        #ifdef METADATA_OPERATION_COND
            // FIXME: is cast really necessary?
            meta.flowblaze_metadata.pkt_data = (bit<32>) (METADATA_OPERATION_COND & 0xFFFFFFFF);
        #endif
        context_lookup.apply();
        condition_table.apply();
        bit<1> tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_0, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c0 = tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_1, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c1 = tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_2, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c2 = tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_3, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c3 = tmp_cnd;

        EFSM_table.apply();
        update_logic.apply(hdr, meta.flowblaze_metadata, meta.flowblaze_metadata.update_block.u_block_0, standard_metadata);
        update_logic.apply(hdr, meta.flowblaze_metadata, meta.flowblaze_metadata.update_block.u_block_1, standard_metadata);
        update_logic.apply(hdr, meta.flowblaze_metadata, meta.flowblaze_metadata.update_block.u_block_2, standard_metadata);

        pkt_action.apply();

    }
}
#endif

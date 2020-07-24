#ifndef _OPP_LIB_
#define _OPP_LIB_

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

/*
* TODO:
*  - Timeouts are not implemented 
*  - Lack of conditions of packet header (implementable).
*  - BI-FLOW not implemented (it can be implemented adding a second
*       lookup hash field and loading also the register of the corresponding second lookup. 
*       This logic is valid also for the update.)
*  - Check corner cases like condition not set and update not evaluated.
*  - Some problems with multicast groups.
*/

// Global Data Variable: 4
register<bit<32>>(4) reg_G;

// 4 Flow Registers 
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R0;
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R1;
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R2;
register<bit<32>>(CONTEXT_TABLE_SIZE) reg_R3;



// Register that stores the state of the flows
register<bit<16>>(CONTEXT_TABLE_SIZE) reg_state;

control ConditionBlock(inout OPP_single_condition_t meta_c_blk, 
                       inout OPP_t opp_metadata,
                       in standard_metadata_t standard_metadata,
                       out bit<1> c) {
    apply {
        c = 0;
        if(meta_c_blk.cond != NO_CONDITION){
            // Set operand 1
            if(meta_c_blk.op1 == _R0) {
                meta_c_blk.operand1 = opp_metadata.R0;
            }
            if(meta_c_blk.op1 == _R1) {
                meta_c_blk.operand1 = opp_metadata.R1;
            }
            if(meta_c_blk.op1 == _R2) {
                meta_c_blk.operand1 = opp_metadata.R2;
            }
            if(meta_c_blk.op1 == _R3) {
                meta_c_blk.operand1 = opp_metadata.R3;
            }
            if(meta_c_blk.op1 == _G0) {
                meta_c_blk.operand1 = opp_metadata.G0;
            }
            if(meta_c_blk.op1 == _G1) {
                meta_c_blk.operand1 = opp_metadata.G1;
            }
            if(meta_c_blk.op1 == _G2) {
                meta_c_blk.operand1 = opp_metadata.G2;
            }
            if(meta_c_blk.op1 == _G3) {
                meta_c_blk.operand1 = opp_metadata.G3;
            }
            if(meta_c_blk.op1 == _META) {
                meta_c_blk.operand1 = opp_metadata.pkt_data;
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
                meta_c_blk.operand2 = opp_metadata.R0;
            }
            if(meta_c_blk.op2 == _R1) {
                meta_c_blk.operand2 = opp_metadata.R1;
            }
            if(meta_c_blk.op2 == _R2) {
                meta_c_blk.operand2 = opp_metadata.R2;
            }
            if(meta_c_blk.op2 == _R3) {
                meta_c_blk.operand2 = opp_metadata.R3;
            }
            if(meta_c_blk.op2 == _G0) {
                meta_c_blk.operand2 = opp_metadata.G0;
            }
            if(meta_c_blk.op2 == _G1) {
                meta_c_blk.operand2 = opp_metadata.G1;
            }
            if(meta_c_blk.op2 == _G2) {
                meta_c_blk.operand2 = opp_metadata.G2;
            }
            if(meta_c_blk.op2 == _G3) {
                meta_c_blk.operand2 = opp_metadata.G3;
            }
            if(meta_c_blk.op2 == _META) {
                meta_c_blk.operand2 = opp_metadata.pkt_data;
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
control UpdateLogic(inout headers hdr,
                    inout OPP_t opp_metadata,
                    inout OPP_single_update_t update_block,
                    in standard_metadata_t standard_metadata) {

    apply{
        // Calculate update lookup index
        // TODO: (improvement) save hash in metadata when calculated for reading registers
        hash(opp_metadata.update_state_index, 
             HashAlgorithm.crc32, 
             (bit<32>) 0,
             FLOW_SCOPE,
             (bit<32>) CONTEXT_TABLE_SIZE);
        // Update state using the update lookup index
        reg_state.write(opp_metadata.update_state_index, opp_metadata.state);

        // Check if an operation is requested and then extract operands and operation
        if(update_block.operation != _NO_OP){
            // Set the operand 1
            if(update_block.op1 == _R0) {
                update_block.operand1 = opp_metadata.R0;
            }
            if(update_block.op1 == _R1) {
                update_block.operand1 = opp_metadata.R1;
            }
            if(update_block.op1 == _R2) {
                update_block.operand1 = opp_metadata.R2;
            }
            if(update_block.op1 == _R3) {
                update_block.operand1 = opp_metadata.R3;
            }
            if(update_block.op1 == _G0) {
                update_block.operand1 = opp_metadata.G0;
            }
            if(update_block.op1 == _G1) {
                update_block.operand1 = opp_metadata.G1;
            }
            if(update_block.op1 == _G2) {
                update_block.operand1 = opp_metadata.G2;
            }
            if(update_block.op1 == _G3) {
                update_block.operand1 = opp_metadata.G3;
            }
            if(update_block.op1 == _META) {
                update_block.operand1 = opp_metadata.pkt_data;
            }
            if(update_block.op1 == _TIME_NOW) {
                update_block.operand1 = (bit<32>) standard_metadata.ingress_global_timestamp;
            }
            // EXPLICIT IS THE DEFAULT BEHAVIOUR
            //if(opp_metadata.op1 == _EXPL) {
            //    opp_metadata.operand1 = opp_metadata.operand1
            //}

            // Set the operand 2
            if(update_block.op2 == _R0) {
               update_block.operand2 = opp_metadata.R0;
            }
            if(update_block.op2 == _R1) {
                update_block.operand2 = opp_metadata.R1;
            }
            if(update_block.op2 == _R2) {
                update_block.operand2 = opp_metadata.R2;
            }
            if(update_block.op2 == _R3) {
                update_block.operand2 = opp_metadata.R3;
            }
            if(update_block.op2 == _G0) {
                update_block.operand2 = opp_metadata.G0;
            }
            if(update_block.op2 == _G1) {
                update_block.operand2 = opp_metadata.G1;
            }
            if(update_block.op2 == _G2) {
                update_block.operand2 = opp_metadata.G2;
            }
            if(update_block.op2 == _G3) {
                update_block.operand2 = opp_metadata.G3;
            }
            if(update_block.op2 == _META) {
                update_block.operand2 = opp_metadata.pkt_data;
            }
             if(update_block.op2 == _TIME_NOW) {
                update_block.operand2 = (bit<32>) standard_metadata.ingress_global_timestamp;
            }
            // EXPLICIT IS THE DEFAULT BEHAVIOUR
            //if(opp_metadata.op2 == _EXPL) {
            //    opp_metadata.operand2 = opp_metadata.operand2
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
                    reg_R0.write(opp_metadata.update_state_index, t_result);
                }
                if(update_block.result == _R1) {
                    reg_R1.write(opp_metadata.update_state_index, t_result);
                }
                if(update_block.result == _R2) {
                    reg_R2.write(opp_metadata.update_state_index, t_result);
                }
                if(update_block.result == _R3) {
                    reg_R3.write(opp_metadata.update_state_index, t_result);
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

// TODO: change the metadata passed, otherwise meta overwrite OPP_t
control OPPLoop (inout headers hdr, 
                 //inout OPP_t opp_metadata,
                 inout metadata_t meta,
                 in standard_metadata_t standard_metadata){
    
    // ------------------------ EFSM TABLE -----------------------------
    action define_operation_update_state(bit<16> state,
                                         //bit<9> port,
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
                                         bit<8> pkt_action
                                         ) {

        // Update the state
        meta.opp_metadata.state = state;

        // Set the packet action to be applied by the main P4 Program,
        //   in this way the user can define arbitrary action to be applied to packet.
        meta.opp_metadata.pkt_action = pkt_action;
        
        // Set operation 1: result = operation(op1, op2)
        meta.opp_metadata.update_block.u_block_0.operation = operation_0;
        meta.opp_metadata.update_block.u_block_0.result = result_0;
        meta.opp_metadata.update_block.u_block_0.op1 = op1_0;
        meta.opp_metadata.update_block.u_block_0.op2 = op2_0;
        meta.opp_metadata.update_block.u_block_0.operand1 = operand1_0;
        meta.opp_metadata.update_block.u_block_0.operand2 = operand2_0;

        // Set operation 2: result = operation(op1, op2)
        meta.opp_metadata.update_block.u_block_1.operation = operation_1;
        meta.opp_metadata.update_block.u_block_1.result = result_1;
        meta.opp_metadata.update_block.u_block_1.op1 = op1_1;
        meta.opp_metadata.update_block.u_block_1.op2 = op2_1;
        meta.opp_metadata.update_block.u_block_1.operand1 = operand1_1;
        meta.opp_metadata.update_block.u_block_1.operand2 = operand2_1;
    }

    direct_counter(CounterType.packets_and_bytes) EFSM_table_counter;
    table EFSM_table {
        actions = {
            define_operation_update_state;
            NoAction;
        }
        key = {
            meta.opp_metadata.state                : ternary;
            meta.opp_metadata.c0                   : ternary;
            meta.opp_metadata.c1                   : ternary;
            meta.opp_metadata.c2                   : ternary;
            meta.opp_metadata.c3                   : ternary;
            EFSM_MATCH_FIELDS
        }
        default_action = NoAction;
        counters = EFSM_table_counter;
    }
    
    // ------------------------------------------------------------------------

    // ----------------------------- CONTEXT LOOKUP ---------------------------
    action lookup_context_table() {
        // Calculate lookup index
        hash(meta.opp_metadata.lookup_state_index, 
             HashAlgorithm.crc32, 
             (bit<32>) 0,
             FLOW_SCOPE,
             (bit<32>)CONTEXT_TABLE_SIZE);

        // Extract the state and all the registers related to the current lookup
        reg_state.read(meta.opp_metadata.state, meta.opp_metadata.lookup_state_index);
        reg_R0.read(meta.opp_metadata.R0, meta.opp_metadata.lookup_state_index);
        reg_R1.read(meta.opp_metadata.R1, meta.opp_metadata.lookup_state_index);
        reg_R2.read(meta.opp_metadata.R2, meta.opp_metadata.lookup_state_index);
        reg_R3.read(meta.opp_metadata.R3, meta.opp_metadata.lookup_state_index);

        // Extract also the global register
        reg_G.read(meta.opp_metadata.G0, 0);
        reg_G.read(meta.opp_metadata.G1, 1);
        reg_G.read(meta.opp_metadata.G2, 2);
        reg_G.read(meta.opp_metadata.G3, 3);
    }

    direct_counter(CounterType.packets_and_bytes) context_lookup_counter;
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
        meta.opp_metadata.condition_block.c_block_0.cond = cond0;
        meta.opp_metadata.condition_block.c_block_0.op1 = op1_0;
        meta.opp_metadata.condition_block.c_block_0.op2 = op2_0;
        meta.opp_metadata.condition_block.c_block_0.operand1 = operand1_0;
        meta.opp_metadata.condition_block.c_block_0.operand2 = operand2_0;
        meta.opp_metadata.condition_block.c_block_1.cond = cond1;
        meta.opp_metadata.condition_block.c_block_1.op1 = op1_1;
        meta.opp_metadata.condition_block.c_block_1.op2 = op2_1;
        meta.opp_metadata.condition_block.c_block_1.operand1 = operand1_1;
        meta.opp_metadata.condition_block.c_block_1.operand2 = operand2_1;
        meta.opp_metadata.condition_block.c_block_2.cond = cond2;
        meta.opp_metadata.condition_block.c_block_2.op1 = op1_2;
        meta.opp_metadata.condition_block.c_block_2.op2 = op2_2;
        meta.opp_metadata.condition_block.c_block_2.operand1 = operand1_2;
        meta.opp_metadata.condition_block.c_block_2.operand2 = operand2_2;
        meta.opp_metadata.condition_block.c_block_3.cond = cond3;
        meta.opp_metadata.condition_block.c_block_3.op1 = op1_3;
        meta.opp_metadata.condition_block.c_block_3.op2 = op2_3;
        meta.opp_metadata.condition_block.c_block_3.operand1 = operand1_3;
        meta.opp_metadata.condition_block.c_block_3.operand2 = operand2_3;

    }
    direct_counter(CounterType.packets_and_bytes) condition_table_counter;
    table condition_table {
        actions = {
            set_condition_fields;
            NoAction;
        }
        default_action = NoAction;
        counters = condition_table_counter;
    }

    // --------------------------------------------------------------------------


    UpdateLogic() update_logic;
    ConditionBlock() condition_block;

    apply {
        // FIXME: is cast really necessary?
        meta.opp_metadata.pkt_data = (bit<32>) (METADATA_OPERATION_COND & 0xFFFFFFFF);
        context_lookup.apply();
        // TODO: FIND a way to implement in a clever way the condition block. It's a little bit messy and ugly like this
        condition_table.apply();
        bit<1> tmp_cnd;
        condition_block.apply(meta.opp_metadata.condition_block.c_block_0, meta.opp_metadata, standard_metadata, tmp_cnd);
        meta.opp_metadata.c0 = tmp_cnd;
        condition_block.apply(meta.opp_metadata.condition_block.c_block_1, meta.opp_metadata, standard_metadata, tmp_cnd);
        meta.opp_metadata.c1 = tmp_cnd;
        condition_block.apply(meta.opp_metadata.condition_block.c_block_2, meta.opp_metadata, standard_metadata, tmp_cnd);
        meta.opp_metadata.c2 = tmp_cnd;
        condition_block.apply(meta.opp_metadata.condition_block.c_block_3, meta.opp_metadata, standard_metadata, tmp_cnd);
        meta.opp_metadata.c3 = tmp_cnd;
        

        EFSM_table.apply();
        update_logic.apply(hdr, meta.opp_metadata, meta.opp_metadata.update_block.u_block_0, standard_metadata);
        update_logic.apply(hdr, meta.opp_metadata, meta.opp_metadata.update_block.u_block_1, standard_metadata);

    }

}
#endif

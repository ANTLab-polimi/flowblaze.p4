package org.polimi.flowblaze;

import org.onosproject.net.pi.model.PiActionId;
import org.onosproject.net.pi.model.PiMatchFieldId;
import org.onosproject.net.pi.model.PiTableId;

public final class FlowblazeConst {

    public static final int MAX_CONDITIONS = 4;
    public static final int MAX_OPERATIONS = 3;

    public static final byte CONDITION_NOP  = 0b000;
    public static final byte CONDITION_EQ   = 0b001;
    public static final byte CONDITION_GTE  = 0b011;
    public static final byte CONDITION_LTE  = 0b101;
    public static final byte CONDITION_GT   = 0b010;
    public static final byte CONDITION_LT   = 0b100;

    public static final byte OPERATION_NOP      = (byte) 0x00;
    public static final byte OPERATION_PLUS     = (byte) 0x01;
    public static final byte OPERATION_MINUS    = (byte) 0x02;
    public static final byte OPERATION_R_SHIFT  = (byte) 0x03;
    public static final byte OPERATION_L_SHIFT  = (byte) 0x04;
    public static final byte OPERATION_MUL      = (byte) 0x05;

    public static final byte REGISTER_META      = (byte) 0xF1;
    public static final byte REGISTER_NOW       = (byte) 0xF2;


    // Valid for conditions as well as for operations
    public static final byte EXPLICIT_OPERAND = (byte) 0xFF;


    public static final PiActionId ACTION_SET_CONDITION_FIELDS =
            PiActionId.of("FabricIngress.FlowBlazeLoop.set_condition_fields");
    public static final PiActionId ACTION_DEFINE_OPERATION_UPDATE_STATE =
            PiActionId.of("FabricIngress.FlowBlazeLoop.define_operation_update_state");
    public static final PiTableId TABLE_CONDITION_TABLE =
            PiTableId.of("FabricIngress.FlowBlazeLoop.condition_table");
    public static final PiTableId TABLE_EFSM_TABLE =
            PiTableId.of("FabricIngress.FlowBlazeLoop.EFSM_table");
    public static final PiTableId TABLE_PKT_ACTION =
            PiTableId.of("FabricIngress.FlowBlazeLoop.pkt_action");

    public static final PiMatchFieldId FIELD_EFSM_TABLE_STATE =
            PiMatchFieldId.of("meta.flowblaze_metadata.state");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C0 =
            PiMatchFieldId.of("meta.flowblaze_metadata.c0");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C1 =
            PiMatchFieldId.of("meta.flowblaze_metadata.c1");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C2 =
            PiMatchFieldId.of("meta.flowblaze_metadata.c2");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C3 =
            PiMatchFieldId.of("meta.flowblaze_metadata.c3");

    public static final PiMatchFieldId FIELD_PKT_ACTION_PKT_ACTION =
            PiMatchFieldId.of("meta.flowblaze_metadata.pkt_actio");


    public static final byte[] ONE = {1};
    public static final byte[] ZERO = {0};

    private FlowblazeConst() {
        // Hide constructor
    }
}

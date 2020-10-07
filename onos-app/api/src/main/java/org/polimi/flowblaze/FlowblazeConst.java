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

package org.polimi.flowblaze;

import com.google.common.collect.BiMap;
import com.google.common.collect.ImmutableBiMap;
import org.onosproject.net.pi.model.PiActionId;
import org.onosproject.net.pi.model.PiMatchFieldId;
import org.onosproject.net.pi.model.PiTableId;

public final class FlowblazeConst {

    public static final int MAX_CONDITIONS = 4;
    public static final int MAX_OPERATIONS = 3;

    public static final byte CONDITION_NOP = 0b000;
    public static final byte CONDITION_EQ = 0b001;
    public static final byte CONDITION_GTE = 0b011;
    public static final byte CONDITION_LTE = 0b101;
    public static final byte CONDITION_GT = 0b010;
    public static final byte CONDITION_LT = 0b100;

    public static final byte OPERATION_NOP = (byte) 0x00;
    public static final byte OPERATION_PLUS = (byte) 0x01;
    public static final byte OPERATION_MINUS = (byte) 0x02;
    public static final byte OPERATION_R_SHIFT = (byte) 0x03;
    public static final byte OPERATION_L_SHIFT = (byte) 0x04;
    public static final byte OPERATION_MUL = (byte) 0x05;

    public static final byte REGISTER_META = (byte) 0xF1;
    public static final byte REGISTER_NOW = (byte) 0xF2;

    public static final byte EXPLICIT_OPERAND = (byte) 0xFF;


    public static final PiActionId ACTION_SET_CONDITION_FIELDS =
            PiActionId.of("FlowBlaze.set_condition_fields");
    public static final PiActionId ACTION_DEFINE_OPERATION_UPDATE_STATE =
            PiActionId.of("FlowBlaze.define_operation_update_state");
    public static final PiTableId TABLE_CONDITION_TABLE =
            PiTableId.of("FlowBlaze.condition_table");
    public static final PiTableId TABLE_EFSM_TABLE =
            PiTableId.of("FlowBlaze.EFSM_table");
    public static final PiTableId TABLE_PKT_ACTION =
            PiTableId.of("FlowBlaze.pkt_action");

    public static final PiMatchFieldId FIELD_EFSM_TABLE_STATE =
            PiMatchFieldId.of("FlowBlaze.state");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C0 =
            PiMatchFieldId.of("FlowBlaze.condition0");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C1 =
            PiMatchFieldId.of("FlowBlaze.condition1");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C2 =
            PiMatchFieldId.of("FlowBlaze.condition2");
    public static final PiMatchFieldId FIELD_EFSM_TABLE_C3 =
            PiMatchFieldId.of("FlowBlaze.condition3");

    public static final PiMatchFieldId FIELD_PKT_ACTION_PKT_ACTION =
            PiMatchFieldId.of("FlowBlaze.pkt_action");


    public static final String STRING_META_REGISTER = "META";
    public static final String STRING_CONST_REGISTER = "CONST";
    public static final String STRING_NOW_REGISTER = "NOW";

    public static final byte[] ONE = {1};
    public static final byte[] ZERO = {0};


    public static final BiMap<String, Byte> REGISTERS = new ImmutableBiMap.Builder<String, Byte>()
            .put(STRING_META_REGISTER, REGISTER_META)
            .put(STRING_NOW_REGISTER, REGISTER_NOW)
            .put(STRING_CONST_REGISTER, EXPLICIT_OPERAND)
            .build();

    public static final BiMap<Byte, String> REVERSE_REGISTERS = REGISTERS.inverse();


    private FlowblazeConst() {
        // Hide constructor
    }
}

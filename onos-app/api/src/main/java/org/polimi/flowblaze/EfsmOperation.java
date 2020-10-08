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

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.base.MoreObjects;

import static org.polimi.flowblaze.FlowblazeConst.*;
import static org.polimi.flowblaze.Utils.stringToByte;

/**
 * Representation of an EFSM Operation.
 */
public class EfsmOperation {
    public final byte operand1;
    public final byte operand2;
    public final byte result;
    public final int constOperand1;
    public final int constOperand2;
    public final EfsmOperation.Operation operation;

    @JsonCreator
    public EfsmOperation(@JsonProperty("operation") EfsmOperation.Operation op,
                         @JsonProperty("operand1") String op1,
                         @JsonProperty("operand2") String op2,
                         @JsonProperty("result") String result,
                         @JsonProperty("constOperand1") int constOp1,
                         @JsonProperty("constOperand2") int constOp2) {
        this.operand1 = REGISTERS.containsKey(op1) ? REGISTERS.get(op1) : stringToByte(op1);
        this.constOperand1 = op1.equals(STRING_CONST_REGISTER) ? constOp1 : 0;

        this.operand2 = REGISTERS.containsKey(op2) ? REGISTERS.get(op2) : stringToByte(op2);
        this.constOperand2 = op2.equals(STRING_CONST_REGISTER) ? constOp2 : 0;

        this.result = stringToByte(result);
        this.operation = op;
    }

    public static EfsmOperation defaultEfsmOperation() {
        return new EfsmOperation(EfsmOperation.Operation.NOP, "0", "0", "0", 0, 0);
    }

    public enum Operation {
        NOP,
        PLUS,
        MINUS,
        R_SHIFT,
        L_SHIFT,
        MUL;

        public byte getFlowblazeConst() {
            switch (this) {
                case PLUS:
                    return FlowblazeConst.OPERATION_PLUS;
                case MINUS:
                    return FlowblazeConst.OPERATION_MINUS;
                case R_SHIFT:
                    return FlowblazeConst.OPERATION_R_SHIFT;
                case L_SHIFT:
                    return FlowblazeConst.OPERATION_L_SHIFT;
                case MUL:
                    return FlowblazeConst.OPERATION_MUL;
                case NOP:
                default:
                    return FlowblazeConst.OPERATION_NOP;
            }
        }
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("operand1", REVERSE_REGISTERS.getOrDefault(operand1, Byte.toString(operand1)))
                .add("operand2", REVERSE_REGISTERS.getOrDefault(operand2, Byte.toString(operand2)))
                .add("result", result)
                .add("operation", operation)
                .add("constOperand1", constOperand1)
                .add("constOperand2", constOperand2)
                .toString();
    }
}

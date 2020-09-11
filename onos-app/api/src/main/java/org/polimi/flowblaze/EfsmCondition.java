package org.polimi.flowblaze;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.base.MoreObjects;

import static org.polimi.flowblaze.FlowblazeConst.*;
import static org.polimi.flowblaze.Utils.stringToByte;

/**
 * Representation of an EFSM Condition.
 */
public class EfsmCondition {
    public final byte operand1;
    public final byte operand2;
    public final int constOperand1;
    public final int constOperand2;
    public final Operation operation;

    @JsonCreator
    public EfsmCondition(@JsonProperty("operation") Operation op,
                         @JsonProperty("operand1") String op1,
                         @JsonProperty("operand2") String op2,
                         @JsonProperty("constOperand1") int constOp1,
                         @JsonProperty("constOperand2") int constOp2) {
        this.operand1 = REGISTERS.getOrDefault(op1, stringToByte(op1));
        this.constOperand1 = op1.equals(STRING_CONST_REGISTER) ? constOp1 : 0;

        this.operand2 = REGISTERS.getOrDefault(op2, stringToByte(op2));
        this.constOperand2 = op2.equals(STRING_CONST_REGISTER) ? constOp2 : 0;

        this.operation = op;
    }

    public static EfsmCondition defaultEfsmCondition() {
        return new EfsmCondition(Operation.NOP, "0", "0", 0, 0);
    }

    public enum Operation {
        NOP,
        LT,
        LTE,
        GT,
        GTE,
        EQ;

        public byte getFlowblazeConst() {
            switch (this) {
                case LT:
                    return FlowblazeConst.CONDITION_LT;
                case LTE:
                    return FlowblazeConst.CONDITION_LTE;
                case GT:
                    return FlowblazeConst.CONDITION_GT;
                case GTE:
                    return FlowblazeConst.CONDITION_GTE;
                case EQ:
                    return FlowblazeConst.CONDITION_EQ;
                case NOP:
                default:
                    return FlowblazeConst.CONDITION_NOP;
            }
        }
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("operand1", REVERSE_REGISTERS.getOrDefault(operand1, Byte.toString(operand1)))
                .add("operand2", REVERSE_REGISTERS.getOrDefault(operand2, Byte.toString(operand2)))
                .add("constOperand1", constOperand1)
                .add("constOperand2", constOperand2)
                .add("operation", operation)
                .toString();
    }
}

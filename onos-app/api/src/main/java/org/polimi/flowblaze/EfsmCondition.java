package org.polimi.flowblaze;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

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
        switch (op1) {
            case "CONST":
                this.operand1 = FlowblazeConst.EXPLICIT_OPERAND;
                this.constOperand1 = constOp1;
                break;
            case "META":
                this.operand1 = FlowblazeConst.REGISTER_META;
                this.constOperand1 = 0;
                break;
            case "NOW":
                this.operand1 = FlowblazeConst.REGISTER_NOW;
                this.constOperand1 = 0;
                break;
            default:
                this.operand1 = Byte.parseByte(op1);
                this.constOperand1 = 0;
                break;
        }
        switch (op2) {
            case "CONST":
                this.operand2 = FlowblazeConst.EXPLICIT_OPERAND;
                this.constOperand2 = constOp2;
                break;
            case "META":
                this.operand2 = FlowblazeConst.REGISTER_META;
                this.constOperand2 = 0;
                break;
            case "NOW":
                this.operand2 = FlowblazeConst.REGISTER_NOW;
                this.constOperand2 = 0;
                break;
            default:
                this.operand2 = Byte.parseByte(op2);
                this.constOperand2 = 0;
                break;
        }
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
}

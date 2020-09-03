package org.polimi.flowblaze;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;

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
                         @JsonProperty("result") byte result,
                         @JsonProperty("constOperand1") int constOp1,
                         @JsonProperty("constOperand2")int constOp2) {
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
        this.result = result;
        this.operation = op;
    }

    public static EfsmOperation defaultEfsmOperation() {
        return new EfsmOperation(EfsmOperation.Operation.NOP, "0", "0", (byte) 0, 0, 0);
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
}

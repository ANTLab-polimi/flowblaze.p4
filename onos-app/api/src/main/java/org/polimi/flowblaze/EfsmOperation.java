package org.polimi.flowblaze;

import java.util.Optional;

/**
 * Representation of an EFSM Operation.
 */
public class EfsmOperation {
    public final int operand1;
    public final int operand2;
    public final int result;
    public final int constOperand1;
    public final int constOperand2;
    public final EfsmOperation.Operation operation;

    public EfsmOperation(EfsmOperation.Operation op, int op1, int op2, int result,
                         Optional<Integer> constOp1, Optional<Integer> constOp2) {
        if (constOp1.isPresent()) {
            this.operand1 = FlowblazeConst.EXPLICIT_OPERAND;
            this.constOperand1 = constOp1.get();
        } else {
            this.operand1 = op1;
            this.constOperand1 = 0;
        }
        if (constOp2.isPresent()) {
            this.operand2 = FlowblazeConst.EXPLICIT_OPERAND;
            this.constOperand2 = constOp2.get();
        } else {
            this.operand2 = op2;
            this.constOperand2 = 0;
        }
        this.result = result;
        this.operation = op;
    }

    public static EfsmOperation defaultEfsmOperation() {
        return new EfsmOperation(EfsmOperation.Operation.NOP, 0, 0, 0, Optional.empty(), Optional.empty());
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

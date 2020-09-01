package org.polimi.flowblaze.data;


import org.polimi.flowblaze.FlowblazeConst;

import java.util.Optional;

public class EfsmCondition {
    public final int operand1;
    public final int operand2;
    public final int constOperand1;
    public final int constOperand2;
    public final Operation operation;

    public EfsmCondition(Operation op, int op1, int op2,  Optional<Integer> constOp1, Optional<Integer> constOp2) {
        if(constOp1.isPresent()) {
            this.operand1 = FlowblazeConst.EXPLICIT_OPERAND;
            this.constOperand1 = constOp1.get();
        } else {
            this.operand1 = op1;
            this.constOperand1 = 0;
        }
        if(constOp2.isPresent()) {
            this.operand2 = FlowblazeConst.EXPLICIT_OPERAND;
            this.constOperand2 = constOp2.get();
        } else {
            this.operand2 = op2;
            this.constOperand2 = 0;
        }
        this.operation = op;
    }

    public static EfsmCondition defaultEfsmCondition(){
        return new EfsmCondition(Operation.NOP,0, 0,  Optional.empty(), Optional.empty());
    }

    public enum Operation{
        NOP,
        LT,
        LTE,
        GT,
        GTE,
        EQ;

        public byte getFlowblazeConst() {
            switch (this) {
                case LT: return FlowblazeConst.CONDITION_LT;
                case LTE: return FlowblazeConst.CONDITION_LTE;
                case GT: return FlowblazeConst.CONDITION_GT;
                case GTE: return FlowblazeConst.CONDITION_GTE;
                case EQ: return FlowblazeConst.CONDITION_EQ;
                case NOP:
                default: return FlowblazeConst.CONDITION_NOP;
            }
        }
    }
}

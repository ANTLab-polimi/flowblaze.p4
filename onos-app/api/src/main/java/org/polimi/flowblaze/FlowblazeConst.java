package org.polimi.flowblaze;

public final class FlowblazeConst {
    public static final byte CONDITION_NOP  = 0b000;
    public static final byte CONDITION_EQ   = 0b001;
    public static final byte CONDITION_GTE  = 0b011;
    public static final byte CONDITION_LTE  = 0b101;
    public static final byte CONDITION_GT   = 0b010;
    public static final byte CONDITION_LT   = 0b100;

    public static final byte EXPLICIT_OPERAND = (byte) 0xFF;

    private FlowblazeConst() {
        // Hide constructor
    }
}

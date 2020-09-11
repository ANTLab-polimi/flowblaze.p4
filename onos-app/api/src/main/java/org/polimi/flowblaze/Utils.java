package org.polimi.flowblaze;

public final class Utils {

    public static byte stringToByte(String value) {
        if (value.contains("0x")) {
            // Remove 0x from the string
            value = value.replaceAll("0x", "");
            return (byte) (Integer.parseInt(value, 16) & 0xff);
        }
        return (byte) (Integer.parseInt(value) & 0xff);
    }

    private Utils() {
        // Hide constructor
    }
}

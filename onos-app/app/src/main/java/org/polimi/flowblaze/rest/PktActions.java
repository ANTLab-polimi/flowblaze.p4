package org.polimi.flowblaze.rest;

import java.util.List;

public class PktActions {
    public List<PktAction> pktActions;

    public static class PktAction {
        public String action;
        public byte id;
    }
}

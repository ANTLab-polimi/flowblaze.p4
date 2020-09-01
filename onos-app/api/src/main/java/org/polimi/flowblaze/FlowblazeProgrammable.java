package org.polimi.flowblaze;

import org.onosproject.net.driver.HandlerBehaviour;

public interface FlowblazeProgrammable extends HandlerBehaviour {

    void cleanUp() throws FlowblazeProgrammableException;

    void setupConditions() throws FlowblazeProgrammableException;

    void setupEfsmTable() throws FlowblazeProgrammableException;

    void setupPktActions() throws FlowblazeProgrammableException;

    class FlowblazeProgrammableException extends Exception {
        public FlowblazeProgrammableException(String message) {
            super(message);
        }
    }
}




package org.polimi.flowblaze.impl;

import org.onosproject.net.driver.AbstractHandlerBehaviour;
import org.onosproject.net.driver.DriverData;
import org.onosproject.net.driver.DriverHandler;
import org.polimi.flowblaze.FlowblazeProgrammable;

public class FabricFlowblazeProgrammable extends AbstractHandlerBehaviour
        implements FlowblazeProgrammable {
    @Override
    public void cleanUp() throws FlowblazeProgrammableException {

    }

    @Override
    public void setupConditions() throws FlowblazeProgrammableException {

    }

    @Override
    public void setupEfsmTable() throws FlowblazeProgrammableException {

    }

    @Override
    public void setupPktActions() throws FlowblazeProgrammableException {

    }

    @Override
    public DriverHandler handler() {
        return null;
    }

    @Override
    public void setHandler(DriverHandler handler) {

    }

    @Override
    public DriverData data() {
        return null;
    }

    @Override
    public void setData(DriverData data) {

    }
}

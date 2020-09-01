package org.polimi.flowblaze;

import org.onosproject.net.DeviceId;

import java.util.List;

public interface FlowblazeService {

    void setupEfsm();
    void setupConditions(List<EfsmCondition> conditions);
    void setupEfsmTable();
    void setupPktActions();
    void setFlowblazeDeviceId(DeviceId deviceId);
}

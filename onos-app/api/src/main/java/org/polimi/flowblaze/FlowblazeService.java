package org.polimi.flowblaze;

import org.onosproject.net.DeviceId;
import org.polimi.flowblaze.data.EfsmCondition;

import java.util.List;

public interface FlowblazeService {

    void setupEfsm();
   void setupConditions(List<EfsmCondition> conditions);
    void setupEfsmTable();
    void setupPktActions();
    void setDeviceId(DeviceId deviceId);
}

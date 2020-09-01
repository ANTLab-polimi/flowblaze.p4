package org.polimi.flowblaze;

import org.onosproject.net.DeviceId;

import java.util.List;

public interface FlowblazeService {

    void setupConditions(List<EfsmCondition> conditions);
    void setupEfsmTable(EfsmMatch match, int nextState, List<EfsmOperation> operations, byte pktAction);
    void setupPktActions(byte pktAction, String action);
    void setFlowblazeDeviceId(DeviceId deviceId);
}

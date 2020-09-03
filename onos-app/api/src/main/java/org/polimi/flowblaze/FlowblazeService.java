package org.polimi.flowblaze;

import org.onosproject.net.DeviceId;

import java.util.List;

public interface FlowblazeService {

    boolean setupConditions(List<EfsmCondition> conditions);
    boolean setupEfsmTable(EfsmMatch match, int nextState, List<EfsmOperation> operations, byte pktAction);
    boolean setupPktAction(byte pktAction, String action);
    void setFlowblazeDeviceId(DeviceId deviceId);

    DeviceId getFlowBlazeDeviceId();

}

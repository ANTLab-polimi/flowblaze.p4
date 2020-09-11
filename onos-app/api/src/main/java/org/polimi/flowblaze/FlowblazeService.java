package org.polimi.flowblaze;

import org.onosproject.net.DeviceId;

import java.util.List;

public interface FlowblazeService {

    boolean setupConditions(List<EfsmCondition> conditions);

    boolean setupEfsmTable(EfsmMatch match, int nextState, List<EfsmOperation> operations, byte pktAction);

    boolean setupPktAction(byte pktAction, String action);

    boolean setFlowblazeDeviceId(DeviceId deviceId);

    boolean resetFlowblaze();

    boolean resetPktActions();

    boolean resetConditions();

    boolean resetEfsmEntries();

    DeviceId getFlowBlazeDeviceId();

}

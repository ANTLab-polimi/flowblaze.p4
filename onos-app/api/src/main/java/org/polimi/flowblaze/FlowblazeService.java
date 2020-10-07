/*
 * Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
 *                Davide Sanvito <davide.sanvito@neclab.eu>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

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

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

package org.polimi.flowblaze.impl;

import org.onosproject.core.ApplicationId;
import org.onosproject.net.DeviceId;
import org.onosproject.net.flow.DefaultFlowRule;
import org.onosproject.net.flow.DefaultTrafficSelector;
import org.onosproject.net.flow.DefaultTrafficTreatment;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.criteria.PiCriterion;
import org.onosproject.net.pi.model.PiTableId;
import org.onosproject.net.pi.runtime.PiTableAction;

public final class Utils {
    private static final int DEFAULT_FLOW_RULE_PRIORITY = 20;

    public static FlowRule buildFlowRule(DeviceId switchId, ApplicationId appId,
                                         PiTableId tableId, PiCriterion piCriterion,
                                         PiTableAction piAction) {
        return DefaultFlowRule.builder()
                .forDevice(switchId)
                .fromApp(appId)
                .forTable(tableId)
                .withPriority(DEFAULT_FLOW_RULE_PRIORITY)
                .makePermanent()
                .withSelector(DefaultTrafficSelector.builder()
                                      .matchPi(piCriterion).build())
                .withTreatment(DefaultTrafficTreatment.builder()
                                       .piTableAction(piAction).build())
                .build();
    }

    public static FlowRule buildDefaultActionFlowRule(DeviceId switchId, ApplicationId appId,
                                         PiTableId tableId, PiTableAction piAction) {
        return DefaultFlowRule.builder()
                .forDevice(switchId)
                .fromApp(appId)
                .forTable(tableId)
                .withPriority(DEFAULT_FLOW_RULE_PRIORITY)
                .makePermanent()
                .withSelector(DefaultTrafficSelector.builder().build())
                .withTreatment(DefaultTrafficTreatment.builder()
                                       .piTableAction(piAction).build())
                .build();
    }

    private Utils() {
        // Hide constructor
    }
}

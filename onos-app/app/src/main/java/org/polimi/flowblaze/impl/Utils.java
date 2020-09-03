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

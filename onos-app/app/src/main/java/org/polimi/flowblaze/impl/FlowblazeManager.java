package org.polimi.flowblaze.impl;

import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.DeviceId;
import org.onosproject.net.device.DeviceEvent;
import org.onosproject.net.device.DeviceListener;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.flow.criteria.PiCriterion;
import org.onosproject.net.pi.model.PiActionId;
import org.onosproject.net.pi.model.PiActionParamId;
import org.onosproject.net.pi.runtime.PiAction;
import org.onosproject.net.pi.runtime.PiActionParam;
import org.onosproject.net.pi.runtime.PiTableAction;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Deactivate;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.polimi.flowblaze.FlowblazeService;
import org.polimi.flowblaze.data.EfsmCondition;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Collections;
import java.util.List;

@Component(immediate = true)
public class FlowblazeManager implements FlowblazeService {

    public static final String FLOWBLAZE_APP = "org.polimi.flowblaze";

    private final Logger log = LoggerFactory.getLogger(getClass());

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected DeviceService deviceService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected FlowRuleService flowRuleService;

    private InternalDeviceListener deviceListener;
    private DeviceId flowblazeDeviceId = null;
    private ApplicationId appId;

    @Activate
    protected void activate() {
        appId = coreService.registerApplication(FLOWBLAZE_APP);
        deviceListener = new InternalDeviceListener();
        if(flowblazeDeviceId != null) {
            deviceService.addListener(deviceListener);
        }

        log.info("FlowBlaze app activated");
    }

    @Deactivate
    protected void deactivate() {
        deviceService.removeListener(deviceListener);
        log.info("FlowBlaze app deactivated");
    }

    @Override
    public void setupEfsm() {
        if(flowblazeDeviceId == null) {
            log.error("You can't set the EFSM before setting the FlowBlaze Device ID");
            return;
        }
        // TODO: what happens if the device associated to the flowblazeDeviceId is not available?
        // TODO: should we check if the flowblazeDeviceId has a FlowBlaze pipeline?
    }

    @Override
    public void setupConditions(List<EfsmCondition> conditions) {
        log.info("Adding Conditions on {}...", flowblazeDeviceId);
        // TODO: check conditions length

        String tableId = "ingress.FlowBlazeLoop.condition_table";
        List<PiActionParam> conditionParams = Collections.emptyList();
        int i = 0;
        for (EfsmCondition c : conditions) {
            conditionParams.add(new PiActionParam(PiActionParamId.of(String.format("cond%d", i)), c.operation.getFlowblazeConst()));
            conditionParams.add(new PiActionParam(PiActionParamId.of(String.format("op1_%d", i)), c.operand1));
            conditionParams.add(new PiActionParam(PiActionParamId.of(String.format("op2_%d", i)), c.operand2));
            conditionParams.add(new PiActionParam(PiActionParamId.of(String.format("operand1_%d", i)), c.constOperand1));
            conditionParams.add(new PiActionParam(PiActionParamId.of(String.format("operand2_%d", i)), c.constOperand2));
            i++;
        }
        PiCriterion match = PiCriterion.builder().build();

        PiTableAction action = PiAction.builder()
                .withId(PiActionId.of("ingress.FlowBlazeLoop.condition_table.set_condition_fields"))
                .withParameters(conditionParams)
                .build();

        FlowRule myStationRule = Utils.buildFlowRule(
                flowblazeDeviceId, appId, tableId, match, action);

        flowRuleService.applyFlowRules(myStationRule);
    }

    @Override
    public void setupEfsmTable() {

    }

    @Override
    public void setupPktActions() {

    }

    @Override
    public void setDeviceId(DeviceId deviceId) {
        if(deviceId != null) {
            log.error("You can modify the FlowBlaze Device ID if already set");
            return;
        }
        flowblazeDeviceId = deviceId;
        deviceService.addListener(deviceListener);
    }
    /**
     * React to devices.
     */
    private class InternalDeviceListener implements DeviceListener {
        @Override
        public void event(DeviceEvent event) {
            DeviceId deviceId = event.subject().id();
            if (deviceId.equals(flowblazeDeviceId)) {
                switch (event.type()) {
                    case DEVICE_ADDED:
                    case DEVICE_UPDATED:
                    case DEVICE_AVAILABILITY_CHANGED:
                        if (deviceService.isAvailable(deviceId)) {
                            log.debug("Event: {}, FlowBlaze device available", event.type());
                        }
                        break;
                    case DEVICE_REMOVED:
                    case DEVICE_SUSPENDED:
                        log.debug("Event: {}, FlowBlaze device not available", event.type());
                        break;
                    case PORT_ADDED:
                    case PORT_UPDATED:
                    case PORT_REMOVED:
                    case PORT_STATS_UPDATED:
                        break;
                    default:
                        log.warn("Unknown device event type {}", event.type());
                }
            }
        }
    }
}

package org.polimi.flowblaze.impl;

import com.google.common.collect.Lists;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.DeviceId;
import org.onosproject.net.device.DeviceEvent;
import org.onosproject.net.device.DeviceListener;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.FlowRuleService;
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
import org.polimi.flowblaze.EfsmCondition;
import org.polimi.flowblaze.FlowblazeService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

@Component(immediate = true, service = {FlowblazeService.class})
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

        deviceService.addListener(deviceListener);

        log.info("FlowBlaze app activated");
    }

    @Deactivate
    protected void deactivate() {
        deviceService.removeListener(deviceListener);
        log.info("FlowBlaze app deactivated");
    }

    @Override
    public void setupEfsm() {
        if (flowblazeDeviceId == null) {
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

        String tableId = "FabricIngress.FlowBlazeLoop.condition_table";
        List<PiActionParam> conditionParams = Lists.newArrayList();
        int i = 0;
        for (EfsmCondition c : conditions) {
            conditionParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("cond%d", i)),
                    c.operation.getFlowblazeConst()));
            conditionParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("op1_%d", i)),
                    c.operand1));
            conditionParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("op2_%d", i)),
                    c.operand2));
            conditionParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("operand1_%d", i)),
                    c.constOperand1));
            conditionParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("operand2_%d", i)),
                    c.constOperand2));
            i++;
        }

        PiTableAction action = PiAction.builder()
                .withId(PiActionId.of("FabricIngress.FlowBlazeLoop.set_condition_fields"))
                .withParameters(conditionParams)
                .build();

        FlowRule myStationRule = Utils.buildDefaultActionFlowRule(
                flowblazeDeviceId, appId, tableId, action);

        flowRuleService.applyFlowRules(myStationRule);
    }

    @Override
    public void setupEfsmTable() {

    }

    @Override
    public void setupPktActions() {

    }

    @Override
    public void setFlowblazeDeviceId(DeviceId deviceId) {
        if (flowblazeDeviceId != null) {
            log.error("You can modify the FlowBlaze Device ID if already set");
            return;
        }
        flowblazeDeviceId = deviceId;
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

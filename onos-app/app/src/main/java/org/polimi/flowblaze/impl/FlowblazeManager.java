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

import com.google.common.collect.Lists;
import com.google.common.collect.Streams;
import org.apache.commons.lang3.tuple.Pair;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.onosproject.net.DeviceId;
import org.onosproject.net.flow.FlowEntry;
import org.onosproject.net.flow.FlowRule;
import org.onosproject.net.flow.FlowRuleService;
import org.onosproject.net.flow.TableId;
import org.onosproject.net.flow.criteria.PiCriterion;
import org.onosproject.net.pi.model.PiActionId;
import org.onosproject.net.pi.model.PiActionParamId;
import org.onosproject.net.pi.model.PiMatchFieldId;
import org.onosproject.net.pi.runtime.PiAction;
import org.onosproject.net.pi.runtime.PiActionParam;
import org.onosproject.net.pi.runtime.PiTableAction;
import org.onosproject.net.pi.service.PiPipeconfService;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Deactivate;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.polimi.flowblaze.EfsmCondition;
import org.polimi.flowblaze.EfsmMatch;
import org.polimi.flowblaze.EfsmOperation;
import org.polimi.flowblaze.FlowblazeService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import static org.polimi.flowblaze.FlowblazeConst.*;

@Component(immediate = true, service = {FlowblazeService.class})
public class FlowblazeManager implements FlowblazeService {

    public static final String FLOWBLAZE_APP = "org.polimi.flowblaze";

    private final Logger log = LoggerFactory.getLogger(getClass());

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected FlowRuleService flowRuleService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    protected PiPipeconfService piPipeconfService;

    private DeviceId flowblazeDeviceId = null;
    private ApplicationId appId;

    @Activate
    protected void activate() {
        appId = coreService.registerApplication(FLOWBLAZE_APP);
        log.info("FlowBlaze app activated");
    }

    @Deactivate
    protected void deactivate() {
        flowRuleService.removeFlowRulesById(appId);
        log.info("FlowBlaze app deactivated");
    }

    @Override
    public boolean setupConditions(List<EfsmCondition> conditions) {
        if (!checkFlowBlazeDevice()) {
            return false;
        }
        // N.B: conditions are ordered!!! Must be filled in order!
        log.info("Adding Conditions on {}...", flowblazeDeviceId);
        log.debug("Conditions: {}", conditions);
        if (conditions.size() != MAX_CONDITIONS) {
            log.error(String.format("Wrong number of conditions! (Provided: %d, Required: %d)",
                                    conditions.size(), MAX_CONDITIONS));
            return false;
        }
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
                .withId(ACTION_SET_CONDITION_FIELDS)
                .withParameters(conditionParams)
                .build();

        FlowRule conditionsRule = Utils.buildDefaultActionFlowRule(
                flowblazeDeviceId, appId, TABLE_CONDITION_TABLE, action);

        flowRuleService.applyFlowRules(conditionsRule);
        return true;
    }

    @Override
    public boolean setupEfsmTable(EfsmMatch match, int nextState, List<EfsmOperation> operations, byte pktAction) {
        // TODO: should we check if the pkt_action is actually available?
        //  This would mean that first we have to push pkt_actions and then setup the EFSM Table.
        if (!checkFlowBlazeDevice()) {
            return false;
        }
        log.info("Adding EFSM Table entry on {}...", flowblazeDeviceId);
        log.debug("Match: {}, Next State: {}, Operations: {}, Packet Action: {}",
                  match, nextState, operations, pktAction);
        if (operations.size() != MAX_OPERATIONS) {
            log.error(String.format("Missing operations! (Provided: %d, Required: %d)",
                                    operations.size(), MAX_OPERATIONS));
            return false;
        }
        // TODO: not sure this check if necessary, the translator would fail
        //  anyway and no exception would be generated. Maybe we can issue a simple warning?
        // Check that the EFSM Extra match field is present in the actual pipeline.
        if (!match.checkEfsmExtraMatchFields(piPipeconfService.getPipeconf(flowblazeDeviceId).get())) {
            log.error("EFSM Extra Match Fields not available!, use a device with a different pipeconf");
            return false;
        }

        // Build action and action parameters
        List<PiActionParam> operationParams = Lists.newArrayList();
        int i = 0;
        for (EfsmOperation o : operations) {
            operationParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("operation_%d", i)),
                    o.operation.getFlowblazeConst()));
            operationParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("result_%d", i)),
                    o.result));
            operationParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("op1_%d", i)),
                    o.operand1));
            operationParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("op2_%d", i)),
                    o.operand2));
            operationParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("operand1_%d", i)),
                    o.constOperand1));
            operationParams.add(new PiActionParam(
                    PiActionParamId.of(String.format("operand2_%d", i)),
                    o.constOperand2));
            i++;
        }

        PiTableAction action = PiAction.builder()
                .withId(ACTION_DEFINE_OPERATION_UPDATE_STATE)
                .withParameters(operationParams)
                .withParameter(new PiActionParam(PiActionParamId.of("state"), nextState))
                .withParameter(new PiActionParam(PiActionParamId.of("pkt_action"), pktAction))
                .build();

        // Build match part of EFSM table entry
        PiCriterion.Builder criterionBuilder = PiCriterion.builder()
                .matchTernary(FIELD_EFSM_TABLE_STATE, match.state, 0xFFFF);
        if (match.condition0 != null) {
            criterionBuilder.matchTernary(FIELD_EFSM_TABLE_C0, match.condition0 ? ONE : ZERO, ONE);
        }
        if (match.condition1 != null) {
            criterionBuilder.matchTernary(FIELD_EFSM_TABLE_C1, match.condition1 ? ONE : ZERO, ONE);
        }
        if (match.condition2 != null) {
            criterionBuilder.matchTernary(FIELD_EFSM_TABLE_C2, match.condition2 ? ONE : ZERO, ONE);
        }
        if (match.condition3 != null) {
            criterionBuilder.matchTernary(FIELD_EFSM_TABLE_C3, match.condition3 ? ONE : ZERO, ONE);
        }
        // Build the EFSM Extra match field
        for (Map.Entry<String, Pair<byte[], byte[]>> field : match.efsmExtraMatchFields.entrySet()) {
            criterionBuilder.matchTernary(PiMatchFieldId.of(field.getKey()),
                                          field.getValue().getLeft(),
                                          field.getValue().getRight());
        }

        // Build EFSM Rule
        FlowRule efsmRule = Utils.buildFlowRule(
                flowblazeDeviceId, appId, TABLE_EFSM_TABLE,
                criterionBuilder.build(), action);

        flowRuleService.applyFlowRules(efsmRule);
        return true;
    }

    @Override
    public boolean setupPktAction(byte pktAction, String actionName) {
        if (!checkFlowBlazeDevice()) {
            return false;
        }
        log.info("Adding packet action entry on {}...", flowblazeDeviceId);
        log.debug("Packet action ID: {}, Packet action name: {}", pktAction, actionName);
        PiCriterion criteria = PiCriterion.builder()
                .matchTernary(FIELD_PKT_ACTION_PKT_ACTION, pktAction, 0xFF)
                .build();

        // TODO: support actions with parameters!!
        PiTableAction action = PiAction.builder()
                .withId(PiActionId.of(actionName))
                .build();

        FlowRule pktActionRule = Utils.buildFlowRule(
                flowblazeDeviceId, appId, TABLE_PKT_ACTION, criteria, action);

        flowRuleService.applyFlowRules(pktActionRule);
        return true;
    }

    @Override
    public boolean setFlowblazeDeviceId(DeviceId deviceId) {
        if (flowblazeDeviceId != null) {
            log.error("You cannot modify the FlowBlaze Device ID if it is already set");
            return false;
        }
        flowblazeDeviceId = deviceId;
        return true;
    }

    @Override
    public boolean resetFlowblaze() {
        if (flowblazeDeviceId == null) {
            log.error("Device ID not set!");
            return false;
        }
        flowRuleService.removeFlowRulesById(appId);
        return true;
    }

    @Override
    public boolean resetPktActions() {
        return resetFlowRules(TABLE_PKT_ACTION);
    }

    @Override
    public boolean resetConditions() {
        return resetFlowRules(TABLE_CONDITION_TABLE);
    }

    @Override
    public boolean resetEfsmEntries() {
        return resetFlowRules(TABLE_EFSM_TABLE);
    }

    @Override
    public DeviceId getFlowBlazeDeviceId() {
        return flowblazeDeviceId;
    }

    private boolean resetFlowRules(TableId tableId) {
        if (flowblazeDeviceId == null) {
            log.error("Device ID not set!");
            return false;
        }
        List<FlowEntry> flowRules = Streams.stream(flowRuleService.getFlowEntriesById(appId))
                .filter(flowEntry -> flowEntry.table().equals(tableId))
                .collect(Collectors.toList());
        if (flowRules.size() == 0) {
            log.info("NO rule for the reset on the requested table!");
            return false;
        }
        flowRuleService.removeFlowRules(flowRules.toArray(FlowRule[]::new));
        return true;
    }

    /**
     * @return True if the FlowBlaze device is not null and the pipeconf is present, False otherwise.
     */
    private boolean checkFlowBlazeDevice() {
        if (flowblazeDeviceId == null) {
            log.error("First set the FlowBlaze Device ID");
            return false;
        }
        if (!piPipeconfService.getPipeconf(flowblazeDeviceId).isPresent()) {
            log.info("No pipeconf present for {} device", flowblazeDeviceId);
            return false;
        }
        return true;
    }

}

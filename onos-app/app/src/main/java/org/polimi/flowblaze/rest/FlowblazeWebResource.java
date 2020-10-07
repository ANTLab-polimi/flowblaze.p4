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

package org.polimi.flowblaze.rest;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.onosproject.net.DeviceId;
import org.onosproject.rest.AbstractWebResource;
import org.polimi.flowblaze.EfsmCondition;
import org.polimi.flowblaze.EfsmOperation;
import org.polimi.flowblaze.FlowblazeService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.io.InputStream;
import java.util.stream.LongStream;

import static org.polimi.flowblaze.FlowblazeConst.MAX_CONDITIONS;
import static org.polimi.flowblaze.FlowblazeConst.MAX_OPERATIONS;

/**
 * Intent Monitor and Reroute REST API.
 */
@Path("flowblaze")
public class FlowblazeWebResource extends AbstractWebResource {
    //TODO: add swagger documentation

    private final Logger log = LoggerFactory.getLogger(getClass());

    private FlowblazeService flowblazeService;

    @POST
    @Path("setPktActions")
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_JSON)
    public Response setPktActions(InputStream stream) {
        flowblazeService = get(FlowblazeService.class);
        ObjectNode result = mapper().createObjectNode();
        StringBuilder resultString = new StringBuilder();

        mapper().configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        try {
            PktActions msg = mapper().readValue(stream, PktActions.class);
            String outcome;
            for (PktActions.PktAction action : msg.pktActions) {
                try {
                    if (!flowblazeService.setupPktAction(action.id, action.action)) {
                        outcome = String.format("Error on submitting %s action with ID %d", action.action, action.id);
                    } else {
                        outcome = "OK";
                    }
                } catch (IllegalArgumentException | NullPointerException ex) {
                    outcome = ex.getMessage();
                }
                if (!outcome.equals("OK")) {
                    if (resultString.length() > 0) {
                        resultString.append(" ");
                    }
                    resultString.append(outcome);
                }
                if (resultString.length() > 0) {
                    result.put("response", "setPktActions() failed: ".concat(resultString.toString()));
                } else {
                    result.put("response", "OK");
                }
            }
            return ok(result).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).
                    entity(e.toString())
                    .build();
        }
    }


    @POST
    @Path("setConditions")
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_JSON)
    public Response setConditions(InputStream stream) {
        flowblazeService = get(FlowblazeService.class);
        ObjectNode result = mapper().createObjectNode();
        StringBuilder resultString = new StringBuilder();

        mapper().configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        try {
            EfsmConditions msg = mapper().readValue(stream, EfsmConditions.class);
            // Fill-up missing conditions
            if (msg.conditions != null && msg.conditions.size() < MAX_CONDITIONS) {
                int diff = MAX_CONDITIONS - msg.conditions.size();
                LongStream.range(0, diff).forEach(i -> msg.conditions.add(EfsmCondition.defaultEfsmCondition()));
            }
            String outcome;
            try {
                if (!flowblazeService.setupConditions(msg.conditions)) {
                    outcome = "Error on submitting conditions";
                } else {
                    outcome = "OK";
                }
            } catch (IllegalArgumentException | NullPointerException ex) {
                outcome = ex.getMessage();
            }
            if (!outcome.equals("OK")) {
                resultString.append(outcome);
            }
            if (resultString.length() > 0) {
                result.put("response", "setConditions() failed: ".concat(resultString.toString()));
            } else {
                result.put("response", "OK");
            }
            return ok(result).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).
                    entity(e.toString())
                    .build();
        }
    }

    @POST
    @Path("setEfsmEntry")
    @Produces(MediaType.APPLICATION_JSON)
    @Consumes(MediaType.APPLICATION_JSON)
    public Response setEfsmEntry(InputStream stream) {
        flowblazeService = get(FlowblazeService.class);
        ObjectNode result = mapper().createObjectNode();
        StringBuilder resultString = new StringBuilder();

        mapper().configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        try {
            EfsmEntry msg = mapper().readValue(stream, EfsmEntry.class);
            // Fill-up missing operations
            if (msg.operations != null && msg.operations.size() < MAX_OPERATIONS) {
                int diff = MAX_OPERATIONS - msg.operations.size();
                LongStream.range(0, diff).forEach(i -> msg.operations.add(EfsmOperation.defaultEfsmOperation()));
            }
            String outcome;
            try {
                if (!flowblazeService.setupEfsmTable(msg.match, msg.nextState, msg.operations, msg.pktAction)) {
                    outcome = "Error on submitting EFSM Entry";
                } else {
                    outcome = "OK";
                }
            } catch (IllegalArgumentException | NullPointerException ex) {
                outcome = ex.getMessage();
            }
            if (!outcome.equals("OK")) {
                resultString.append(outcome);
            }
            if (resultString.length() > 0) {
                result.put("response", "setConditions() failed: ".concat(resultString.toString()));
            } else {
                result.put("response", "OK");
            }
            return ok(result).build();
        } catch (Exception e) {
            return Response.status(Response.Status.INTERNAL_SERVER_ERROR).
                    entity(e.toString())
                    .build();
        }
    }

    @GET
    @Path("getDeviceId")
    @Produces(MediaType.APPLICATION_JSON)
    public Response getDeviceId() {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        DeviceId devId = flowblazeService.getFlowBlazeDeviceId();
        ObjectNode result = new ObjectMapper().createObjectNode();
        result.put("DeviceId", devId != null ? devId.toString() : "none");
        return ok(result.toString()).build();
    }

    @GET
    @Path("resetFlowblaze")
    @Produces(MediaType.APPLICATION_JSON)
    public Response resetFlowblaze() {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        ObjectNode result = new ObjectMapper().createObjectNode();
        if (!flowblazeService.resetFlowblaze()) {
            result.put("response", "Error when resetting FlowBlaze device");
        }
        return ok(result.toString()).build();
    }

    @GET
    @Path("resetConditions")
    @Produces(MediaType.APPLICATION_JSON)
    public Response resetConditions() {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        ObjectNode result = new ObjectMapper().createObjectNode();
        if (!flowblazeService.resetConditions()) {
            result.put("response", "Error when resetting conditions");
        }
        return ok(result.toString()).build();
    }

    @GET
    @Path("resetEfsmEntries")
    @Produces(MediaType.APPLICATION_JSON)
    public Response resetEfsmEntries() {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        ObjectNode result = new ObjectMapper().createObjectNode();
        if (!flowblazeService.resetConditions()) {
            result.put("response", "Error when resetting EFSM entries");
        }
        return ok(result.toString()).build();
    }

    @GET
    @Path("resetPktActions")
    @Produces(MediaType.APPLICATION_JSON)
    public Response resetPktActions() {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        ObjectNode result = new ObjectMapper().createObjectNode();
        if (!flowblazeService.resetPktActions()) {
            result.put("response", "Error when resetting packet actions");
        }
        return ok(result.toString()).build();
    }

    @GET
    @Path("setDeviceId/{deviceId}")
    @Produces(MediaType.APPLICATION_JSON)
    public Response setDeviceId(@PathParam("deviceId") String deviceId) {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        flowblazeService.setFlowblazeDeviceId(DeviceId.deviceId(deviceId));
        ObjectNode result = new ObjectMapper().createObjectNode();
        return ok(result.toString()).build();
    }
}

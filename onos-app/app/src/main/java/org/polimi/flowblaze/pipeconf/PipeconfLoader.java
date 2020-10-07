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

package org.polimi.flowblaze.pipeconf;

import org.onosproject.net.device.PortStatisticsDiscovery;
import org.onosproject.net.driver.DriverAdminService;
import org.onosproject.net.driver.DriverProvider;
import org.onosproject.net.pi.model.DefaultPiPipeconf;
import org.onosproject.net.pi.model.PiPipeconf;
import org.onosproject.net.pi.model.PiPipeconfId;
import org.onosproject.net.pi.service.PiPipeconfService;
import org.onosproject.p4runtime.model.P4InfoParserException;
import org.onosproject.pipelines.fabric.FabricPipeconfService;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Deactivate;
import org.osgi.service.component.annotations.Reference;
import org.osgi.service.component.annotations.ReferenceCardinality;
import org.polimi.flowblaze.impl.PortStatisticsDiscoveryImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.net.URL;
import java.util.List;
import java.util.stream.Collectors;

import static org.onosproject.net.pi.model.PiPipeconf.ExtensionType.BMV2_JSON;

/**
 * Component that builds and register the pipeconf at app activation.
 */
@Component(immediate = true, service = PipeconfLoader.class)
public final class PipeconfLoader {

    public static final String FABRIC_FLOWBLAZE_PROFILE = "fabric-flowblaze";
    private final Logger log = LoggerFactory.getLogger(getClass());
    private static final String BASE_PATH = "/p4c-out/fabric-flowblaze/bmv2/default/";
    private static final String P4INFO = "p4info.txt";
    private static final String BMV2_JSON_FILE = "bmv2.json";
    private static final String CPU_PORT = "cpu_port.txt";
    private static final PiPipeconfId PIPECONF_ID = new PiPipeconfId("org.polimi.fabric-flowblaze");


    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private PiPipeconfService pipeconfService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private FabricPipeconfService fabricPipeconfService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY)
    private DriverAdminService driverAdminService;

    @Activate
    public void activate() {
        // Registers the pipeconf at component activation.
        if (pipeconfService.getPipeconf(PIPECONF_ID).isPresent()) {
            // Remove first if already registered, to support reloading of the
            // pipeconf during the tutorial.
            pipeconfService.unregister(PIPECONF_ID);
        }
        removePipeconfDrivers();
        try {
            pipeconfService.register(buildPipeconf());
        } catch (P4InfoParserException e) {
            log.error("Unable to register " + PIPECONF_ID, e);
        }
    }

    @Deactivate
    public void deactivate() {
        // Do nothing.
    }

    private PiPipeconf buildPipeconf() throws P4InfoParserException {

        final URL p4InfoUrl = PipeconfLoader.class.getResource(BASE_PATH + P4INFO);
        final URL bmv2JsonUrlUrl = PipeconfLoader.class.getResource(BASE_PATH + BMV2_JSON_FILE);
        final URL cpuPortUrl = PipeconfLoader.class.getResource(BASE_PATH + CPU_PORT);

        DefaultPiPipeconf.Builder builder = DefaultPiPipeconf.builder()
                .withId(PIPECONF_ID)
                .addBehaviour(PortStatisticsDiscovery.class, PortStatisticsDiscoveryImpl.class)
                .addExtension(BMV2_JSON, bmv2JsonUrlUrl);

        // Use the standard Fabric Pipeliner
        return fabricPipeconfService.buildFabricPipeconf(builder, FABRIC_FLOWBLAZE_PROFILE, p4InfoUrl, cpuPortUrl);
    }

    private void removePipeconfDrivers() {
        List<DriverProvider> driverProvidersToRemove = driverAdminService
                .getProviders().stream()
                .filter(p -> p.getDrivers().stream()
                        .anyMatch(d -> d.name().endsWith(PIPECONF_ID.id())))
                .collect(Collectors.toList());

        if (driverProvidersToRemove.isEmpty()) {
            return;
        }

        log.info("Found {} outdated drivers for pipeconf '{}', removing...",
                 driverProvidersToRemove.size(), PIPECONF_ID);

        driverProvidersToRemove.forEach(driverAdminService::unregisterProvider);
    }
}
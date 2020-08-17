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

#include <core.p4>
#include <v1model.p4>

################################################## FLOWBLAZE PARAMETERS #############################################

#define FLOW_SCOPE {  }
#define METADATA_OPERATION_COND (bit<32>)
#define EFSM_MATCH_FIELDS
#define CONTEXT_TABLE_SIZE
#define CUSTOM_ACTIONS_DEFINITION
#define CUSTOM_ACTIONS_DECLARATION
####################################################################################################################

#include "../flowblaze_lib/flowblaze_metadata.p4"

// HERE  here the definition of your header and metadata
#inclue "metadata_header.p4"

#include "../flowblaze_lib/flowblaze_loop.p4"

parser ParserImpl(packet_in packet, out headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    // Define your Parser

}

control ingress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {

   // Define your ingress processing

    apply {
        // Invoke FlowBlaze machine
        FlowBlazeLoop.apply(hdr, meta, standard_metadata);
    }
}

control egress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    // Define your egress processing
    apply {

    }
}

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        // Define your deparser
    }
}

control verifyChecksum(inout headers hdr, inout metadata_t meta) {
    apply {
        // define you verify checksum
    }
}

control computeChecksum(inout headers hdr, inout metadata_t meta) {
    apply {
        // define you compute checksum
    }
}

V1Switch(
    ParserImpl(),
    verifyChecksum(),
    ingress(),
    egress(),
    computeChecksum(),
    DeparserImpl()
) main;


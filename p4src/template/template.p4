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

    // Define the flowblazeLoop that has to be invoked in the apply block
    FlowBlazeLoop() flowblazeLoop;

    apply {
        // Invoke FlowBlaze machine
        flowblazeLoop.apply(hdr, meta, standard_metadata);
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


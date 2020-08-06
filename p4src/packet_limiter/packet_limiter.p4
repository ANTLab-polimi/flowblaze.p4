#include <core.p4>
#include <v1model.p4>


################################################## FLOWBLAZE PARAMETERS #############################################

#define FLOW_SCOPE { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr }
#define CUSTOM_ACTIONS_DEFINITION action forward() { \
                                    \
                                  } \
                                  action drop() { \
                                    mark_to_drop(standard_metadata); \
                                    exit; \
                                  }
#define CUSTOM_ACTIONS_DECLARATION forward; drop;
// Configuration parameter left black because not needed
//    #define METADATA_OPERATION_COND
//    #define EFSM_MATCH_FIELDS
//    #define CONTEXT_TABLE_SIZE
####################################################################################################################

#include "../flowblaze_lib/flowblaze_metadata.p4"
#include "headers.p4"
#include "metadata.p4"
#include "../flowblaze_lib/flowblaze_loop.p4"


// Needed in case you want to use it with ONOS
const bit<9> CPU_PORT = 255;

const bit<16> ETH_TYPE_IPV4 = 0x800;
const bit<16> ETH_TYPE_ARP  = 0x806;
const bit<8>  IP_TYPE_TCP   = 0x06;
const bit<8>  IP_TYPE_UDP   = 0x11;


parser ParserImpl(packet_in packet, out headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    
    state start {
         transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            ETH_TYPE_IPV4: parse_ipv4;
            ETH_TYPE_ARP:  accept;
        }
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        meta.tcpLength = hdr.ipv4.totalLen - 16w20;
        transition select(hdr.ipv4.protocol) {
            IP_TYPE_TCP:    parse_tcp;
            IP_TYPE_UDP:    parse_udp;
            default:        accept;
        }
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        meta.applLength = hdr.ipv4.totalLen - 16w40;
        transition accept;
    }

    state parse_udp {
        packet.extract(hdr.udp);
        meta.applLength = meta.tcpLength - 16w28;
        transition accept;
    }

}

control ingress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {

    // -------------------------------- TABLE L2 FWD -------------------------------------------
    
    action main_forward(bit<9> port) {
      standard_metadata.egress_spec = port;
    }

    action main_drop() {
      mark_to_drop(standard_metadata);
      exit;
    }

    direct_counter(CounterType.packets_and_bytes) l2_fwd_counter;
    table t_l2_fwd {
        key = {
            standard_metadata.ingress_port : ternary;
            hdr.ethernet.dstAddr           : ternary;
            hdr.ethernet.srcAddr           : ternary;
            hdr.ethernet.etherType         : ternary;
        }
        actions = {
            main_forward;
            main_drop;
            NoAction;
        }
        default_action = NoAction();
        counters = l2_fwd_counter;
    }

    apply {
        if (hdr.ethernet.isValid()) {
            FlowBlazeLoop.apply(hdr, meta, standard_metadata);
            t_l2_fwd.apply();
        }
    }
}

control egress(inout headers hdr, inout metadata_t meta, inout standard_metadata_t standard_metadata) {
    apply {
    }
}

control DeparserImpl(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
    }
}

control verifyChecksum(inout headers hdr, inout metadata_t meta) {
    apply {
        verify_checksum(
            hdr.ipv4.isValid(), 
            { hdr.ipv4.version,
              hdr.ipv4.ihl, 
              hdr.ipv4.diffserv, 
              hdr.ipv4.totalLen, 
              hdr.ipv4.identification, 
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset, 
              hdr.ipv4.ttl, 
              hdr.ipv4.protocol, 
              hdr.ipv4.srcAddr, 
              hdr.ipv4.dstAddr 
            }, 
            hdr.ipv4.hdrChecksum, 
            HashAlgorithm.csum16);
    }
}

control computeChecksum(inout headers hdr, inout metadata_t meta) {
    apply {
        update_checksum(
            hdr.ipv4.isValid(),
            { hdr.ipv4.version, 
              hdr.ipv4.ihl, 
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen, 
              hdr.ipv4.identification, 
              hdr.ipv4.flags, 
              hdr.ipv4.fragOffset, 
              hdr.ipv4.ttl, 
              hdr.ipv4.protocol, 
              hdr.ipv4.srcAddr, 
              hdr.ipv4.dstAddr 
            }, 
            hdr.ipv4.hdrChecksum, 
            HashAlgorithm.csum16);

        update_checksum_with_payload(
            hdr.tcp.isValid(), 
            { hdr.ipv4.srcAddr, 
              hdr.ipv4.dstAddr, 
              8w0, 
              hdr.ipv4.protocol, 
              meta.tcpLength, 
              hdr.tcp.srcPort, 
              hdr.tcp.dstPort, 
              hdr.tcp.seqNo, 
              hdr.tcp.ackNo, 
              hdr.tcp.dataOffset, 
              hdr.tcp.res, 
              hdr.tcp.ecn,
              hdr.tcp.ctrl,
              hdr.tcp.window,
             hdr.tcp.urgentPtr 
            }, 
            hdr.tcp.checksum, 
            HashAlgorithm.csum16);
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


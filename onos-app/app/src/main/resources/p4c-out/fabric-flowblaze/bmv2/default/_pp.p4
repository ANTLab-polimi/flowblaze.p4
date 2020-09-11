#include <core.p4>
#include <v1model.p4>

struct flowblaze_single_update_t {
    bit<8>  operation;
    bit<8>  result;
    bit<8>  op1;
    bit<8>  op2;
    bit<32> operand1;
    bit<32> operand2;
}

struct flowblaze_update_block_t {
    flowblaze_single_update_t u_block_0;
    flowblaze_single_update_t u_block_1;
    flowblaze_single_update_t u_block_2;
}

struct flowblaze_single_condition_t {
    bit<3>  cond;
    bit<8>  op1;
    bit<8>  op2;
    bit<32> operand1;
    bit<32> operand2;
}

struct flowblaze_condition_block_t {
    flowblaze_single_condition_t c_block_0;
    flowblaze_single_condition_t c_block_1;
    flowblaze_single_condition_t c_block_2;
    flowblaze_single_condition_t c_block_3;
}

struct flowblaze_t {
    bit<32>                     lookup_state_index;
    bit<32>                     update_state_index;
    bit<16>                     state;
    bit<32>                     R0;
    bit<32>                     R1;
    bit<32>                     R2;
    bit<32>                     R3;
    bit<32>                     G0;
    bit<32>                     G1;
    bit<32>                     G2;
    bit<32>                     G3;
    bit<1>                      c0;
    bit<1>                      c1;
    bit<1>                      c2;
    bit<1>                      c3;
    bit<8>                      pkt_action;
    bit<32>                     pkt_data;
    flowblaze_update_block_t    update_block;
    flowblaze_condition_block_t condition_block;
}

typedef bit<3> fwd_type_t;
typedef bit<32> next_id_t;
typedef bit<20> mpls_label_t;
typedef bit<9> port_num_t;
typedef bit<48> mac_addr_t;
typedef bit<16> mcast_group_id_t;
typedef bit<12> vlan_id_t;
typedef bit<32> ipv4_addr_t;
typedef bit<16> l4_port_t;
typedef bit<2> direction_t;
typedef bit<8> spgw_interface_t;
typedef bit<1> pcc_gate_status_t;
typedef bit<32> sdf_rule_id_t;
typedef bit<32> pcc_rule_id_t;
typedef bit<32> far_id_t;
typedef bit<32> pdr_ctr_id_t;
typedef bit<32> teid_t;
const spgw_interface_t SPGW_IFACE_UNKNOWN = 8w0;
const spgw_interface_t SPGW_IFACE_ACCESS = 8w1;
const spgw_interface_t SPGW_IFACE_CORE = 8w2;
const direction_t SPGW_DIR_UNKNOWN = 2w0;
const direction_t SPGW_DIR_UPLINK = 2w1;
const direction_t SPGW_DIR_DOWNLINK = 2w2;
const bit<16> ETHERTYPE_QINQ = 0x88a8;
const bit<16> ETHERTYPE_QINQ_NON_STD = 0x9100;
const bit<16> ETHERTYPE_VLAN = 0x8100;
const bit<16> ETHERTYPE_MPLS = 0x8847;
const bit<16> ETHERTYPE_MPLS_MULTICAST = 0x8848;
const bit<16> ETHERTYPE_IPV4 = 0x800;
const bit<16> ETHERTYPE_IPV6 = 0x86dd;
const bit<16> ETHERTYPE_ARP = 0x806;
const bit<16> ETHERTYPE_PPPOED = 0x8863;
const bit<16> ETHERTYPE_PPPOES = 0x8864;
const bit<16> PPPOE_PROTOCOL_IP4 = 0x21;
const bit<16> PPPOE_PROTOCOL_IP6 = 0x57;
const bit<16> PPPOE_PROTOCOL_MPLS = 0x281;
const bit<8> PROTO_ICMP = 1;
const bit<8> PROTO_TCP = 6;
const bit<8> PROTO_UDP = 17;
const bit<8> PROTO_ICMPV6 = 58;
const bit<4> IPV4_MIN_IHL = 5;
const fwd_type_t FWD_BRIDGING = 0;
const fwd_type_t FWD_MPLS = 1;
const fwd_type_t FWD_IPV4_UNICAST = 2;
const fwd_type_t FWD_IPV4_MULTICAST = 3;
const fwd_type_t FWD_IPV6_UNICAST = 4;
const fwd_type_t FWD_IPV6_MULTICAST = 5;
const fwd_type_t FWD_UNKNOWN = 7;
const vlan_id_t DEFAULT_VLAN_ID = 12w4094;
const bit<8> DEFAULT_MPLS_TTL = 64;
const bit<8> DEFAULT_IPV4_TTL = 64;
const bit<6> INT_DSCP = 0x1;
const bit<8> INT_HEADER_LEN_WORDS = 4;
const bit<16> INT_HEADER_LEN_BYTES = 16;
const bit<8> CPU_MIRROR_SESSION_ID = 250;
const bit<32> REPORT_MIRROR_SESSION_ID = 500;
const bit<4> NPROTO_ETHERNET = 0;
const bit<4> NPROTO_TELEMETRY_DROP_HEADER = 1;
const bit<4> NPROTO_TELEMETRY_SWITCH_LOCAL_HEADER = 2;
const bit<6> HW_ID = 1;
const bit<8> REPORT_FIXED_HEADER_LEN = 12;
const bit<8> DROP_REPORT_HEADER_LEN = 12;
const bit<8> LOCAL_REPORT_HEADER_LEN = 16;
const bit<8> ETH_HEADER_LEN = 14;
const bit<8> IPV4_MIN_HEAD_LEN = 20;
const bit<8> UDP_HEADER_LEN = 8;
action nop() {
    NoAction();
}
struct int_metadata_t {
    bool    source;
    bool    transit;
    bool    sink;
    bit<32> switch_id;
    bit<8>  new_words;
    bit<16> new_bytes;
    bit<32> ig_tstamp;
    bit<32> eg_tstamp;
}

header int_header_t {
    bit<2>  ver;
    bit<2>  rep;
    bit<1>  c;
    bit<1>  e;
    bit<5>  rsvd1;
    bit<5>  ins_cnt;
    bit<8>  max_hop_cnt;
    bit<8>  total_hop_cnt;
    bit<4>  instruction_mask_0003;
    bit<4>  instruction_mask_0407;
    bit<4>  instruction_mask_0811;
    bit<4>  instruction_mask_1215;
    bit<16> rsvd2;
}

header intl4_shim_t {
    bit<8> int_type;
    bit<8> rsvd1;
    bit<8> len_words;
    bit<8> rsvd2;
}

header intl4_tail_t {
    bit<8>  next_proto;
    bit<16> dest_port;
    bit<2>  padding;
    bit<6>  dscp;
}

@controller_header("packet_in") header packet_in_header_t {
    port_num_t ingress_port;
    bit<7>     _pad;
}

@controller_header("packet_out") header packet_out_header_t {
    port_num_t egress_port;
    bit<7>     _pad;
}

header ethernet_t {
    mac_addr_t dst_addr;
    mac_addr_t src_addr;
}

header eth_type_t {
    bit<16> value;
}

header vlan_tag_t {
    bit<16>   eth_type;
    bit<3>    pri;
    bit<1>    cfi;
    vlan_id_t vlan_id;
}

header mpls_t {
    bit<20> label;
    bit<3>  tc;
    bit<1>  bos;
    bit<8>  ttl;
}

header pppoe_t {
    bit<4>  version;
    bit<4>  type_id;
    bit<8>  code;
    bit<16> session_id;
    bit<16> length;
    bit<16> protocol;
}

header ipv4_t {
    bit<4>  version;
    bit<4>  ihl;
    bit<6>  dscp;
    bit<2>  ecn;
    bit<16> total_len;
    bit<16> identification;
    bit<3>  flags;
    bit<13> frag_offset;
    bit<8>  ttl;
    bit<8>  protocol;
    bit<16> hdr_checksum;
    bit<32> src_addr;
    bit<32> dst_addr;
}

header ipv6_t {
    bit<4>   version;
    bit<8>   traffic_class;
    bit<20>  flow_label;
    bit<16>  payload_len;
    bit<8>   next_hdr;
    bit<8>   hop_limit;
    bit<128> src_addr;
    bit<128> dst_addr;
}

header tcp_t {
    bit<16> sport;
    bit<16> dport;
    bit<32> seq_no;
    bit<32> ack_no;
    bit<4>  data_offset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgent_ptr;
}

header udp_t {
    bit<16> sport;
    bit<16> dport;
    bit<16> len;
    bit<16> checksum;
}

header icmp_t {
    bit<8>  icmp_type;
    bit<8>  icmp_code;
    bit<16> checksum;
    bit<16> identifier;
    bit<16> sequence_number;
    bit<64> timestamp;
}

struct fabric_metadata_t {
    bit<16>      ip_eth_type;
    vlan_id_t    vlan_id;
    bit<3>       vlan_pri;
    bit<1>       vlan_cfi;
    mpls_label_t mpls_label;
    bit<8>       mpls_ttl;
    bool         skip_forwarding;
    bool         skip_next;
    fwd_type_t   fwd_type;
    next_id_t    next_id;
    bool         is_multicast;
    bool         is_controller_packet_out;
    bit<8>       ip_proto;
    bit<16>      l4_sport;
    bit<16>      l4_dport;
    bit<32>      ipv4_src_addr;
    bit<32>      ipv4_dst_addr;
    flowblaze_t  flowblaze_metadata;
}

struct parsed_headers_t {
    ethernet_t          ethernet;
    vlan_tag_t          vlan_tag;
    vlan_tag_t          inner_vlan_tag;
    eth_type_t          eth_type;
    mpls_t              mpls;
    ipv4_t              ipv4;
    tcp_t               tcp;
    udp_t               udp;
    icmp_t              icmp;
    packet_out_header_t packet_out;
    packet_in_header_t  packet_in;
}

register<bit<32>>(4) reg_G;

register<bit<32>>(2014) reg_R0;

register<bit<32>>(2014) reg_R1;

register<bit<32>>(2014) reg_R2;

register<bit<32>>(2014) reg_R3;

register<bit<16>>(2014) reg_state;

control ConditionBlock(inout flowblaze_single_condition_t meta_c_blk, inout flowblaze_t flowblaze_metadata, in standard_metadata_t standard_metadata, out bit<1> c) {
    apply {
        c = 0;
        if (meta_c_blk.cond != 0b0) {
            if (meta_c_blk.op1 == 0x0) {
                meta_c_blk.operand1 = flowblaze_metadata.R0;
            }
            if (meta_c_blk.op1 == 0x1) {
                meta_c_blk.operand1 = flowblaze_metadata.R1;
            }
            if (meta_c_blk.op1 == 0x2) {
                meta_c_blk.operand1 = flowblaze_metadata.R2;
            }
            if (meta_c_blk.op1 == 0x3) {
                meta_c_blk.operand1 = flowblaze_metadata.R3;
            }
            if (meta_c_blk.op1 == 0xf) {
                meta_c_blk.operand1 = flowblaze_metadata.G0;
            }
            if (meta_c_blk.op1 == 0x1f) {
                meta_c_blk.operand1 = flowblaze_metadata.G1;
            }
            if (meta_c_blk.op1 == 0x2f) {
                meta_c_blk.operand1 = flowblaze_metadata.G2;
            }
            if (meta_c_blk.op1 == 0x3f) {
                meta_c_blk.operand1 = flowblaze_metadata.G3;
            }
            if (meta_c_blk.op1 == 0xf1) {
                meta_c_blk.operand1 = flowblaze_metadata.pkt_data;
            }
            if (meta_c_blk.op1 == 0xf2) {
                meta_c_blk.operand1 = (bit<32>)standard_metadata.ingress_global_timestamp;
            }
            if (meta_c_blk.op2 == 0x0) {
                meta_c_blk.operand2 = flowblaze_metadata.R0;
            }
            if (meta_c_blk.op2 == 0x1) {
                meta_c_blk.operand2 = flowblaze_metadata.R1;
            }
            if (meta_c_blk.op2 == 0x2) {
                meta_c_blk.operand2 = flowblaze_metadata.R2;
            }
            if (meta_c_blk.op2 == 0x3) {
                meta_c_blk.operand2 = flowblaze_metadata.R3;
            }
            if (meta_c_blk.op2 == 0xf) {
                meta_c_blk.operand2 = flowblaze_metadata.G0;
            }
            if (meta_c_blk.op2 == 0x1f) {
                meta_c_blk.operand2 = flowblaze_metadata.G1;
            }
            if (meta_c_blk.op2 == 0x2f) {
                meta_c_blk.operand2 = flowblaze_metadata.G2;
            }
            if (meta_c_blk.op2 == 0x3f) {
                meta_c_blk.operand2 = flowblaze_metadata.G3;
            }
            if (meta_c_blk.op2 == 0xf1) {
                meta_c_blk.operand2 = flowblaze_metadata.pkt_data;
            }
            if (meta_c_blk.op2 == 0xf2) {
                meta_c_blk.operand2 = (bit<32>)standard_metadata.ingress_global_timestamp;
            }
            if (meta_c_blk.cond == 0b1) {
                c = (bit<1>)(meta_c_blk.operand1 == meta_c_blk.operand2);
            }
            if (meta_c_blk.cond == 0b10) {
                c = (bit<1>)(meta_c_blk.operand1 > meta_c_blk.operand2);
            }
            if (meta_c_blk.cond == 0b11) {
                c = (bit<1>)(meta_c_blk.operand1 >= meta_c_blk.operand2);
            }
            if (meta_c_blk.cond == 0b100) {
                c = (bit<1>)(meta_c_blk.operand1 < meta_c_blk.operand2);
            }
            if (meta_c_blk.cond == 0b101) {
                c = (bit<1>)(meta_c_blk.operand1 <= meta_c_blk.operand2);
            }
        }
    }
}

control UpdateLogic(inout parsed_headers_t hdr, inout flowblaze_t flowblaze_metadata, inout flowblaze_single_update_t update_block, in standard_metadata_t standard_metadata) {
    apply {
        hash(flowblaze_metadata.update_state_index, HashAlgorithm.crc32, (bit<32>)0, { hdr.ipv4.src_addr }, (bit<32>)2014);
        reg_state.write(flowblaze_metadata.update_state_index, flowblaze_metadata.state);
        if (update_block.operation != 0x0) {
            if (update_block.op1 == 0x0) {
                update_block.operand1 = flowblaze_metadata.R0;
            }
            if (update_block.op1 == 0x1) {
                update_block.operand1 = flowblaze_metadata.R1;
            }
            if (update_block.op1 == 0x2) {
                update_block.operand1 = flowblaze_metadata.R2;
            }
            if (update_block.op1 == 0x3) {
                update_block.operand1 = flowblaze_metadata.R3;
            }
            if (update_block.op1 == 0xf) {
                update_block.operand1 = flowblaze_metadata.G0;
            }
            if (update_block.op1 == 0x1f) {
                update_block.operand1 = flowblaze_metadata.G1;
            }
            if (update_block.op1 == 0x2f) {
                update_block.operand1 = flowblaze_metadata.G2;
            }
            if (update_block.op1 == 0x3f) {
                update_block.operand1 = flowblaze_metadata.G3;
            }
            if (update_block.op1 == 0xf1) {
                update_block.operand1 = flowblaze_metadata.pkt_data;
            }
            if (update_block.op1 == 0xf2) {
                update_block.operand1 = (bit<32>)standard_metadata.ingress_global_timestamp;
            }
            if (update_block.op2 == 0x0) {
                update_block.operand2 = flowblaze_metadata.R0;
            }
            if (update_block.op2 == 0x1) {
                update_block.operand2 = flowblaze_metadata.R1;
            }
            if (update_block.op2 == 0x2) {
                update_block.operand2 = flowblaze_metadata.R2;
            }
            if (update_block.op2 == 0x3) {
                update_block.operand2 = flowblaze_metadata.R3;
            }
            if (update_block.op2 == 0xf) {
                update_block.operand2 = flowblaze_metadata.G0;
            }
            if (update_block.op2 == 0x1f) {
                update_block.operand2 = flowblaze_metadata.G1;
            }
            if (update_block.op2 == 0x2f) {
                update_block.operand2 = flowblaze_metadata.G2;
            }
            if (update_block.op2 == 0x3f) {
                update_block.operand2 = flowblaze_metadata.G3;
            }
            if (update_block.op2 == 0xf1) {
                update_block.operand2 = flowblaze_metadata.pkt_data;
            }
            if (update_block.op2 == 0xf2) {
                update_block.operand2 = (bit<32>)standard_metadata.ingress_global_timestamp;
            }
            bit<32> t_result = 0;
            bit<1> op_done = 0b0;
            if (update_block.operation == 0x1) {
                t_result = update_block.operand1 + update_block.operand2;
                op_done = 0b1;
            }
            if (update_block.operation == 0x2) {
                t_result = update_block.operand1 - update_block.operand2;
                op_done = 0b1;
            }
            if (update_block.operation == 0x3) {
                t_result = update_block.operand1 >> (bit<8>)update_block.operand2;
                op_done = 0b1;
            }
            if (update_block.operation == 0x4) {
                t_result = update_block.operand1 << (bit<8>)update_block.operand2;
                op_done = 0b1;
            }
            if (update_block.operation == 0x5) {
                t_result = update_block.operand1 * update_block.operand2;
                op_done = 0b1;
            }
            if (op_done == 0b1) {
                if (update_block.result == 0x0) {
                    reg_R0.write(flowblaze_metadata.update_state_index, t_result);
                }
                if (update_block.result == 0x1) {
                    reg_R1.write(flowblaze_metadata.update_state_index, t_result);
                }
                if (update_block.result == 0x2) {
                    reg_R2.write(flowblaze_metadata.update_state_index, t_result);
                }
                if (update_block.result == 0x3) {
                    reg_R3.write(flowblaze_metadata.update_state_index, t_result);
                }
                if (update_block.result == 0xf) {
                    reg_G.write(0, t_result);
                }
                if (update_block.result == 0x1f) {
                    reg_G.write(1, t_result);
                }
                if (update_block.result == 0x2f) {
                    reg_G.write(2, t_result);
                }
                if (update_block.result == 0x3f) {
                    reg_G.write(3, t_result);
                }
            }
        }
    }
}

control FlowBlazeLoop(inout parsed_headers_t hdr, inout fabric_metadata_t meta, inout standard_metadata_t standard_metadata) {
    @name(".FlowBlaze.define_operation_update_state") action define_operation_update_state(bit<16> state, bit<8> operation_0, bit<8> result_0, bit<8> op1_0, bit<8> op2_0, bit<32> operand1_0, bit<32> operand2_0, bit<8> operation_1, bit<8> result_1, bit<8> op1_1, bit<8> op2_1, bit<32> operand1_1, bit<32> operand2_1, bit<8> operation_2, bit<8> result_2, bit<8> op1_2, bit<8> op2_2, bit<32> operand1_2, bit<32> operand2_2, bit<8> pkt_action) {
        meta.flowblaze_metadata.state = state;
        meta.flowblaze_metadata.pkt_action = pkt_action;
        meta.flowblaze_metadata.update_block.u_block_0.operation = operation_0;
        meta.flowblaze_metadata.update_block.u_block_0.result = result_0;
        meta.flowblaze_metadata.update_block.u_block_0.op1 = op1_0;
        meta.flowblaze_metadata.update_block.u_block_0.op2 = op2_0;
        meta.flowblaze_metadata.update_block.u_block_0.operand1 = operand1_0;
        meta.flowblaze_metadata.update_block.u_block_0.operand2 = operand2_0;
        meta.flowblaze_metadata.update_block.u_block_1.operation = operation_1;
        meta.flowblaze_metadata.update_block.u_block_1.result = result_1;
        meta.flowblaze_metadata.update_block.u_block_1.op1 = op1_1;
        meta.flowblaze_metadata.update_block.u_block_1.op2 = op2_1;
        meta.flowblaze_metadata.update_block.u_block_1.operand1 = operand1_1;
        meta.flowblaze_metadata.update_block.u_block_1.operand2 = operand2_1;
        meta.flowblaze_metadata.update_block.u_block_2.operation = operation_2;
        meta.flowblaze_metadata.update_block.u_block_2.result = result_2;
        meta.flowblaze_metadata.update_block.u_block_2.op1 = op1_2;
        meta.flowblaze_metadata.update_block.u_block_2.op2 = op2_2;
        meta.flowblaze_metadata.update_block.u_block_2.operand1 = operand1_2;
        meta.flowblaze_metadata.update_block.u_block_2.operand2 = operand2_2;
    }
    @name(".FlowBlaze.EFSM_table_counter") direct_counter(CounterType.packets_and_bytes) EFSM_table_counter;
    @name(".FlowBlaze.EFSM_table") table EFSM_table {
        actions = {
            define_operation_update_state;
            NoAction;
        }
        key = {
            meta.flowblaze_metadata.state: ternary @name("FlowBlaze.state") ;
            meta.flowblaze_metadata.c0   : ternary @name("FlowBlaze.condition0") ;
            meta.flowblaze_metadata.c1   : ternary @name("FlowBlaze.condition1") ;
            meta.flowblaze_metadata.c2   : ternary @name("FlowBlaze.condition2") ;
            meta.flowblaze_metadata.c3   : ternary @name("FlowBlaze.condition3") ;
            hdr.ipv4.src_addr            : ternary;
        }
        default_action = NoAction;
        counters = EFSM_table_counter;
    }
    @name(".FlowBlaze.lookup_context_table") action lookup_context_table() {
        hash(meta.flowblaze_metadata.lookup_state_index, HashAlgorithm.crc32, (bit<32>)0, { hdr.ipv4.src_addr }, (bit<32>)2014);
        reg_state.read(meta.flowblaze_metadata.state, meta.flowblaze_metadata.lookup_state_index);
        reg_R0.read(meta.flowblaze_metadata.R0, meta.flowblaze_metadata.lookup_state_index);
        reg_R1.read(meta.flowblaze_metadata.R1, meta.flowblaze_metadata.lookup_state_index);
        reg_R2.read(meta.flowblaze_metadata.R2, meta.flowblaze_metadata.lookup_state_index);
        reg_R3.read(meta.flowblaze_metadata.R3, meta.flowblaze_metadata.lookup_state_index);
        reg_G.read(meta.flowblaze_metadata.G0, 0);
        reg_G.read(meta.flowblaze_metadata.G1, 1);
        reg_G.read(meta.flowblaze_metadata.G2, 2);
        reg_G.read(meta.flowblaze_metadata.G3, 3);
    }
    @name(".FlowBlaze.context_lookup_counter") direct_counter(CounterType.packets_and_bytes) context_lookup_counter;
    @name(".FlowBlaze.context_lookup") table context_lookup {
        actions = {
            lookup_context_table;
            NoAction;
        }
        default_action = lookup_context_table();
        counters = context_lookup_counter;
    }
    @name(".FlowBlaze.set_condition_fields") action set_condition_fields(bit<3> cond0, bit<8> op1_0, bit<8> op2_0, bit<32> operand1_0, bit<32> operand2_0, bit<3> cond1, bit<8> op1_1, bit<8> op2_1, bit<32> operand1_1, bit<32> operand2_1, bit<3> cond2, bit<8> op1_2, bit<8> op2_2, bit<32> operand1_2, bit<32> operand2_2, bit<3> cond3, bit<8> op1_3, bit<8> op2_3, bit<32> operand1_3, bit<32> operand2_3) {
        meta.flowblaze_metadata.condition_block.c_block_0.cond = cond0;
        meta.flowblaze_metadata.condition_block.c_block_0.op1 = op1_0;
        meta.flowblaze_metadata.condition_block.c_block_0.op2 = op2_0;
        meta.flowblaze_metadata.condition_block.c_block_0.operand1 = operand1_0;
        meta.flowblaze_metadata.condition_block.c_block_0.operand2 = operand2_0;
        meta.flowblaze_metadata.condition_block.c_block_1.cond = cond1;
        meta.flowblaze_metadata.condition_block.c_block_1.op1 = op1_1;
        meta.flowblaze_metadata.condition_block.c_block_1.op2 = op2_1;
        meta.flowblaze_metadata.condition_block.c_block_1.operand1 = operand1_1;
        meta.flowblaze_metadata.condition_block.c_block_1.operand2 = operand2_1;
        meta.flowblaze_metadata.condition_block.c_block_2.cond = cond2;
        meta.flowblaze_metadata.condition_block.c_block_2.op1 = op1_2;
        meta.flowblaze_metadata.condition_block.c_block_2.op2 = op2_2;
        meta.flowblaze_metadata.condition_block.c_block_2.operand1 = operand1_2;
        meta.flowblaze_metadata.condition_block.c_block_2.operand2 = operand2_2;
        meta.flowblaze_metadata.condition_block.c_block_3.cond = cond3;
        meta.flowblaze_metadata.condition_block.c_block_3.op1 = op1_3;
        meta.flowblaze_metadata.condition_block.c_block_3.op2 = op2_3;
        meta.flowblaze_metadata.condition_block.c_block_3.operand1 = operand1_3;
        meta.flowblaze_metadata.condition_block.c_block_3.operand2 = operand2_3;
    }
    @name(".FlowBlaze.condition_table_counter") direct_counter(CounterType.packets_and_bytes) condition_table_counter;
    @name(".FlowBlaze.condition_table") table condition_table {
        actions = {
            set_condition_fields;
            NoAction;
        }
        default_action = NoAction;
        counters = condition_table_counter;
    }
    @name(".FlowBlaze.forward") action forward() {
    }
    @name(".FlowBlaze.drop") action drop() {
        mark_to_drop(standard_metadata);
        exit;
    }
    @name(".FlowBlaze.pkt_action_counter") direct_counter(CounterType.packets_and_bytes) pkt_action_counter;
    @name(".FlowBlaze.pkt_action") table pkt_action {
        key = {
            meta.flowblaze_metadata.pkt_action: ternary @name("FlowBlaze.pkt_action") ;
        }
        actions = {
            forward;
            drop;
            NoAction;
        }
        default_action = NoAction();
        counters = pkt_action_counter;
    }
    UpdateLogic() update_logic;
    ConditionBlock() condition_block;
    apply {
        meta.flowblaze_metadata.pkt_data = (bit<32>)((bit<32>)hdr.ipv4.total_len & 0xffffffff);
        context_lookup.apply();
        condition_table.apply();
        bit<1> tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_0, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c0 = tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_1, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c1 = tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_2, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c2 = tmp_cnd;
        condition_block.apply(meta.flowblaze_metadata.condition_block.c_block_3, meta.flowblaze_metadata, standard_metadata, tmp_cnd);
        meta.flowblaze_metadata.c3 = tmp_cnd;
        EFSM_table.apply();
        update_logic.apply(hdr, meta.flowblaze_metadata, meta.flowblaze_metadata.update_block.u_block_0, standard_metadata);
        update_logic.apply(hdr, meta.flowblaze_metadata, meta.flowblaze_metadata.update_block.u_block_1, standard_metadata);
        update_logic.apply(hdr, meta.flowblaze_metadata, meta.flowblaze_metadata.update_block.u_block_2, standard_metadata);
        pkt_action.apply();
    }
}

control Filtering(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    direct_counter(CounterType.packets_and_bytes) ingress_port_vlan_counter;
    action deny() {
        fabric_metadata.skip_forwarding = true;
        fabric_metadata.skip_next = true;
        ingress_port_vlan_counter.count();
    }
    action permit() {
        ingress_port_vlan_counter.count();
    }
    action permit_with_internal_vlan(vlan_id_t vlan_id) {
        fabric_metadata.vlan_id = vlan_id;
        permit();
    }
    table ingress_port_vlan {
        key = {
            standard_metadata.ingress_port: exact @name("ig_port") ;
            hdr.vlan_tag.isValid()        : exact @name("vlan_is_valid") ;
            hdr.vlan_tag.vlan_id          : ternary @name("vlan_id") ;
        }
        actions = {
            deny();
            permit();
            permit_with_internal_vlan();
        }
        const default_action = deny();
        counters = ingress_port_vlan_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) fwd_classifier_counter;
    action set_forwarding_type(fwd_type_t fwd_type) {
        fabric_metadata.fwd_type = fwd_type;
        fwd_classifier_counter.count();
    }
    table fwd_classifier {
        key = {
            standard_metadata.ingress_port: exact @name("ig_port") ;
            hdr.ethernet.dst_addr         : ternary @name("eth_dst") ;
            hdr.eth_type.value            : ternary @name("eth_type") ;
            fabric_metadata.ip_eth_type   : exact @name("ip_eth_type") ;
        }
        actions = {
            set_forwarding_type;
        }
        const default_action = set_forwarding_type(FWD_BRIDGING);
        counters = fwd_classifier_counter;
        size = 1024;
    }
    apply {
        if (hdr.vlan_tag.isValid()) {
            fabric_metadata.vlan_id = hdr.vlan_tag.vlan_id;
            fabric_metadata.vlan_pri = hdr.vlan_tag.pri;
            fabric_metadata.vlan_cfi = hdr.vlan_tag.cfi;
        }
        if (!hdr.mpls.isValid()) {
            fabric_metadata.mpls_ttl = DEFAULT_MPLS_TTL + 1;
        }
        ingress_port_vlan.apply();
        fwd_classifier.apply();
    }
}

control Forwarding(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    @hidden action set_next_id(next_id_t next_id) {
        fabric_metadata.next_id = next_id;
    }
    direct_counter(CounterType.packets_and_bytes) bridging_counter;
    action set_next_id_bridging(next_id_t next_id) {
        set_next_id(next_id);
        bridging_counter.count();
    }
    table bridging {
        key = {
            fabric_metadata.vlan_id: exact @name("vlan_id") ;
            hdr.ethernet.dst_addr  : ternary @name("eth_dst") ;
        }
        actions = {
            set_next_id_bridging;
            @defaultonly nop;
        }
        const default_action = nop();
        counters = bridging_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) mpls_counter;
    action pop_mpls_and_next(next_id_t next_id) {
        fabric_metadata.mpls_label = 0;
        set_next_id(next_id);
        mpls_counter.count();
    }
    table mpls {
        key = {
            fabric_metadata.mpls_label: exact @name("mpls_label") ;
        }
        actions = {
            pop_mpls_and_next;
            @defaultonly nop;
        }
        const default_action = nop();
        counters = mpls_counter;
        size = 1024;
    }
    action set_next_id_routing_v4(next_id_t next_id) {
        set_next_id(next_id);
    }
    action nop_routing_v4() {
    }
    table routing_v4 {
        key = {
            fabric_metadata.ipv4_dst_addr: lpm @name("ipv4_dst") ;
        }
        actions = {
            set_next_id_routing_v4;
            nop_routing_v4;
            @defaultonly nop;
        }
        default_action = nop();
        size = 1024;
    }
    apply {
        if (fabric_metadata.fwd_type == FWD_BRIDGING) 
            bridging.apply();
        else 
            if (fabric_metadata.fwd_type == FWD_MPLS) 
                mpls.apply();
            else 
                if (fabric_metadata.fwd_type == FWD_IPV4_UNICAST) 
                    routing_v4.apply();
    }
}

control Acl(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    direct_counter(CounterType.packets_and_bytes) acl_counter;
    action set_next_id_acl(next_id_t next_id) {
        fabric_metadata.next_id = next_id;
        acl_counter.count();
    }
    action punt_to_cpu() {
        standard_metadata.egress_spec = 255;
        fabric_metadata.skip_next = true;
        acl_counter.count();
    }
    action set_clone_session_id(bit<32> clone_id) {
        clone3(CloneType.I2E, clone_id, { standard_metadata.ingress_port });
        acl_counter.count();
    }
    action drop() {
        mark_to_drop(standard_metadata);
        fabric_metadata.skip_next = true;
        acl_counter.count();
    }
    action nop_acl() {
        acl_counter.count();
    }
    table acl {
        key = {
            standard_metadata.ingress_port: ternary @name("ig_port") ;
            fabric_metadata.ip_proto      : ternary @name("ip_proto") ;
            fabric_metadata.l4_sport      : ternary @name("l4_sport") ;
            fabric_metadata.l4_dport      : ternary @name("l4_dport") ;
            hdr.ethernet.dst_addr         : ternary @name("eth_dst") ;
            hdr.ethernet.src_addr         : ternary @name("eth_src") ;
            hdr.vlan_tag.vlan_id          : ternary @name("vlan_id") ;
            hdr.eth_type.value            : ternary @name("eth_type") ;
            hdr.ipv4.src_addr             : ternary @name("ipv4_src") ;
            hdr.ipv4.dst_addr             : ternary @name("ipv4_dst") ;
            hdr.icmp.icmp_type            : ternary @name("icmp_type") ;
            hdr.icmp.icmp_code            : ternary @name("icmp_code") ;
        }
        actions = {
            set_next_id_acl;
            punt_to_cpu;
            set_clone_session_id;
            drop;
            nop_acl;
        }
        const default_action = nop_acl();
        size = 1024;
        counters = acl_counter;
    }
    apply {
        acl.apply();
    }
}

control Next(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    @hidden action output(port_num_t port_num) {
        standard_metadata.egress_spec = port_num;
    }
    @hidden action rewrite_smac(mac_addr_t smac) {
        hdr.ethernet.src_addr = smac;
    }
    @hidden action rewrite_dmac(mac_addr_t dmac) {
        hdr.ethernet.dst_addr = dmac;
    }
    @hidden action set_mpls_label(mpls_label_t label) {
        fabric_metadata.mpls_label = label;
    }
    @hidden action routing(port_num_t port_num, mac_addr_t smac, mac_addr_t dmac) {
        rewrite_smac(smac);
        rewrite_dmac(dmac);
        output(port_num);
    }
    @hidden action mpls_routing(port_num_t port_num, mac_addr_t smac, mac_addr_t dmac, mpls_label_t label) {
        set_mpls_label(label);
        routing(port_num, smac, dmac);
    }
    direct_counter(CounterType.packets_and_bytes) next_vlan_counter;
    action set_vlan(vlan_id_t vlan_id) {
        fabric_metadata.vlan_id = vlan_id;
        next_vlan_counter.count();
    }
    table next_vlan {
        key = {
            fabric_metadata.next_id: exact @name("next_id") ;
        }
        actions = {
            set_vlan;
            @defaultonly nop;
        }
        const default_action = nop();
        counters = next_vlan_counter;
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) xconnect_counter;
    action output_xconnect(port_num_t port_num) {
        output(port_num);
        xconnect_counter.count();
    }
    action set_next_id_xconnect(next_id_t next_id) {
        fabric_metadata.next_id = next_id;
        xconnect_counter.count();
    }
    table xconnect {
        key = {
            standard_metadata.ingress_port: exact @name("ig_port") ;
            fabric_metadata.next_id       : exact @name("next_id") ;
        }
        actions = {
            output_xconnect;
            set_next_id_xconnect;
            @defaultonly nop;
        }
        counters = xconnect_counter;
        const default_action = nop();
        size = 1024;
    }
    @max_group_size(16) action_selector(HashAlgorithm.crc16, 32w1024, 32w16) hashed_selector;
    direct_counter(CounterType.packets_and_bytes) hashed_counter;
    action output_hashed(port_num_t port_num) {
        output(port_num);
        hashed_counter.count();
    }
    action routing_hashed(port_num_t port_num, mac_addr_t smac, mac_addr_t dmac) {
        routing(port_num, smac, dmac);
        hashed_counter.count();
    }
    action mpls_routing_hashed(port_num_t port_num, mac_addr_t smac, mac_addr_t dmac, mpls_label_t label) {
        mpls_routing(port_num, smac, dmac, label);
        hashed_counter.count();
    }
    table hashed {
        key = {
            fabric_metadata.next_id      : exact @name("next_id") ;
            fabric_metadata.ipv4_src_addr: selector;
            fabric_metadata.ipv4_dst_addr: selector;
            fabric_metadata.ip_proto     : selector;
            fabric_metadata.l4_sport     : selector;
            fabric_metadata.l4_dport     : selector;
        }
        actions = {
            output_hashed;
            routing_hashed;
            mpls_routing_hashed;
            @defaultonly nop;
        }
        implementation = hashed_selector;
        counters = hashed_counter;
        const default_action = nop();
        size = 1024;
    }
    direct_counter(CounterType.packets_and_bytes) multicast_counter;
    action set_mcast_group_id(mcast_group_id_t group_id) {
        standard_metadata.mcast_grp = group_id;
        fabric_metadata.is_multicast = true;
        multicast_counter.count();
    }
    table multicast {
        key = {
            fabric_metadata.next_id: exact @name("next_id") ;
        }
        actions = {
            set_mcast_group_id;
            @defaultonly nop;
        }
        counters = multicast_counter;
        const default_action = nop();
        size = 1024;
    }
    apply {
        xconnect.apply();
        hashed.apply();
        multicast.apply();
        next_vlan.apply();
    }
}

control EgressNextControl(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    @hidden action pop_mpls_if_present() {
        hdr.mpls.setInvalid();
        hdr.eth_type.value = fabric_metadata.ip_eth_type;
    }
    @hidden action set_mpls() {
        hdr.mpls.setValid();
        hdr.mpls.label = fabric_metadata.mpls_label;
        hdr.mpls.tc = 3w0;
        hdr.mpls.bos = 1w1;
        hdr.mpls.ttl = fabric_metadata.mpls_ttl;
        hdr.eth_type.value = ETHERTYPE_MPLS;
    }
    @hidden action push_vlan() {
        hdr.vlan_tag.setValid();
        hdr.vlan_tag.cfi = fabric_metadata.vlan_cfi;
        hdr.vlan_tag.pri = fabric_metadata.vlan_pri;
        hdr.vlan_tag.eth_type = ETHERTYPE_VLAN;
        hdr.vlan_tag.vlan_id = fabric_metadata.vlan_id;
    }
    direct_counter(CounterType.packets_and_bytes) egress_vlan_counter;
    action pop_vlan() {
        hdr.vlan_tag.setInvalid();
        egress_vlan_counter.count();
    }
    table egress_vlan {
        key = {
            fabric_metadata.vlan_id      : exact @name("vlan_id") ;
            standard_metadata.egress_port: exact @name("eg_port") ;
        }
        actions = {
            pop_vlan;
            @defaultonly nop;
        }
        const default_action = nop();
        counters = egress_vlan_counter;
        size = 1024;
    }
    apply {
        if (fabric_metadata.is_multicast == true && standard_metadata.ingress_port == standard_metadata.egress_port) {
            mark_to_drop(standard_metadata);
        }
        if (fabric_metadata.mpls_label == 0) {
            if (hdr.mpls.isValid()) 
                pop_mpls_if_present();
        }
        else {
            set_mpls();
        }
        if (!egress_vlan.apply().hit) {
            if (fabric_metadata.vlan_id != DEFAULT_VLAN_ID) {
                push_vlan();
            }
        }
        if (hdr.mpls.isValid()) {
            hdr.mpls.ttl = hdr.mpls.ttl - 1;
            if (hdr.mpls.ttl == 0) 
                mark_to_drop(standard_metadata);
        }
        else {
            if (hdr.ipv4.isValid()) {
                hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
                if (hdr.ipv4.ttl == 0) 
                    mark_to_drop(standard_metadata);
            }
        }
    }
}

control PacketIoIngress(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    apply {
        if (hdr.packet_out.isValid()) {
            standard_metadata.egress_spec = hdr.packet_out.egress_port;
            hdr.packet_out.setInvalid();
            fabric_metadata.is_controller_packet_out = true;
            exit;
        }
    }
}

control PacketIoEgress(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    apply {
        if (fabric_metadata.is_controller_packet_out == true) {
            exit;
        }
        if (standard_metadata.egress_port == 255) {
            hdr.packet_in.setValid();
            hdr.packet_in.ingress_port = standard_metadata.ingress_port;
            exit;
        }
    }
}

control FabricComputeChecksum(inout parsed_headers_t hdr, inout fabric_metadata_t meta) {
    apply {
        update_checksum(hdr.ipv4.isValid(), { hdr.ipv4.version, hdr.ipv4.ihl, hdr.ipv4.dscp, hdr.ipv4.ecn, hdr.ipv4.total_len, hdr.ipv4.identification, hdr.ipv4.flags, hdr.ipv4.frag_offset, hdr.ipv4.ttl, hdr.ipv4.protocol, hdr.ipv4.src_addr, hdr.ipv4.dst_addr }, hdr.ipv4.hdr_checksum, HashAlgorithm.csum16);
    }
}

control FabricVerifyChecksum(inout parsed_headers_t hdr, inout fabric_metadata_t meta) {
    apply {
        verify_checksum(hdr.ipv4.isValid(), { hdr.ipv4.version, hdr.ipv4.ihl, hdr.ipv4.dscp, hdr.ipv4.ecn, hdr.ipv4.total_len, hdr.ipv4.identification, hdr.ipv4.flags, hdr.ipv4.frag_offset, hdr.ipv4.ttl, hdr.ipv4.protocol, hdr.ipv4.src_addr, hdr.ipv4.dst_addr }, hdr.ipv4.hdr_checksum, HashAlgorithm.csum16);
    }
}

parser FabricParser(packet_in packet, out parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    bit<6> last_ipv4_dscp = 0;
    state start {
        transition select(standard_metadata.ingress_port) {
            255: parse_packet_out;
            default: parse_ethernet;
        }
    }
    state parse_packet_out {
        packet.extract(hdr.packet_out);
        transition parse_ethernet;
    }
    state parse_ethernet {
        packet.extract(hdr.ethernet);
        fabric_metadata.vlan_id = DEFAULT_VLAN_ID;
        transition select(packet.lookahead<bit<16>>()) {
            ETHERTYPE_QINQ: parse_vlan_tag;
            ETHERTYPE_QINQ_NON_STD: parse_vlan_tag;
            ETHERTYPE_VLAN: parse_vlan_tag;
            default: parse_eth_type;
        }
    }
    state parse_vlan_tag {
        packet.extract(hdr.vlan_tag);
        transition select(packet.lookahead<bit<16>>()) {
            ETHERTYPE_VLAN: parse_inner_vlan_tag;
            default: parse_eth_type;
        }
    }
    state parse_inner_vlan_tag {
        packet.extract(hdr.inner_vlan_tag);
        transition parse_eth_type;
    }
    state parse_eth_type {
        packet.extract(hdr.eth_type);
        transition select(hdr.eth_type.value) {
            ETHERTYPE_MPLS: parse_mpls;
            ETHERTYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
    state parse_mpls {
        packet.extract(hdr.mpls);
        fabric_metadata.mpls_label = hdr.mpls.label;
        fabric_metadata.mpls_ttl = hdr.mpls.ttl;
        transition select(packet.lookahead<bit<4>>()) {
            4: parse_ipv4;
            default: parse_ethernet;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        fabric_metadata.ip_proto = hdr.ipv4.protocol;
        fabric_metadata.ip_eth_type = ETHERTYPE_IPV4;
        fabric_metadata.ipv4_src_addr = hdr.ipv4.src_addr;
        fabric_metadata.ipv4_dst_addr = hdr.ipv4.dst_addr;
        last_ipv4_dscp = hdr.ipv4.dscp;
        transition select(hdr.ipv4.protocol) {
            PROTO_TCP: parse_tcp;
            PROTO_UDP: parse_udp;
            PROTO_ICMP: parse_icmp;
            default: accept;
        }
    }
    state parse_tcp {
        packet.extract(hdr.tcp);
        fabric_metadata.l4_sport = hdr.tcp.sport;
        fabric_metadata.l4_dport = hdr.tcp.dport;
        transition accept;
    }
    state parse_udp {
        packet.extract(hdr.udp);
        fabric_metadata.l4_sport = hdr.udp.sport;
        fabric_metadata.l4_dport = hdr.udp.dport;
        transition select(hdr.udp.dport) {
            default: accept;
        }
    }
    state parse_icmp {
        packet.extract(hdr.icmp);
        transition accept;
    }
}

control FabricDeparser(packet_out packet, in parsed_headers_t hdr) {
    apply {
        packet.emit(hdr.packet_in);
        packet.emit(hdr.ethernet);
        packet.emit(hdr.vlan_tag);
        packet.emit(hdr.inner_vlan_tag);
        packet.emit(hdr.eth_type);
        packet.emit(hdr.mpls);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
        packet.emit(hdr.icmp);
    }
}

control PortCountersControl(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    counter(511, CounterType.packets_and_bytes) egress_port_counter;
    counter(511, CounterType.packets_and_bytes) ingress_port_counter;
    apply {
        if (standard_metadata.egress_spec < 511) {
            egress_port_counter.count((bit<32>)standard_metadata.egress_spec);
        }
        if (standard_metadata.ingress_port < 511) {
            ingress_port_counter.count((bit<32>)standard_metadata.ingress_port);
        }
    }
}

control FabricIngress(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    PacketIoIngress() pkt_io_ingress;
    Filtering() filtering;
    Forwarding() forwarding;
    Acl() acl;
    Next() next;
    PortCountersControl() port_counters_control;
    apply {
        pkt_io_ingress.apply(hdr, fabric_metadata, standard_metadata);
        filtering.apply(hdr, fabric_metadata, standard_metadata);
        if (fabric_metadata.skip_forwarding == false) {
            forwarding.apply(hdr, fabric_metadata, standard_metadata);
        }
        acl.apply(hdr, fabric_metadata, standard_metadata);
        if (fabric_metadata.skip_next == false) {
            next.apply(hdr, fabric_metadata, standard_metadata);
            port_counters_control.apply(hdr, fabric_metadata, standard_metadata);
        }
        FlowBlazeLoop.apply(hdr, fabric_metadata, standard_metadata);
    }
}

control FabricEgress(inout parsed_headers_t hdr, inout fabric_metadata_t fabric_metadata, inout standard_metadata_t standard_metadata) {
    PacketIoEgress() pkt_io_egress;
    EgressNextControl() egress_next;
    apply {
        pkt_io_egress.apply(hdr, fabric_metadata, standard_metadata);
        egress_next.apply(hdr, fabric_metadata, standard_metadata);
    }
}

V1Switch(FabricParser(), FabricVerifyChecksum(), FabricIngress(), FabricEgress(), FabricComputeChecksum(), FabricDeparser()) main;


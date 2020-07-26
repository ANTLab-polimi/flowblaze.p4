from collections import OrderedDict

OPERATIONS = {
    "NOP":  '0x00',    # _NO_OP = 0x00
    "+":    '0x01',    # _PLUS = 0x01
    "-":    '0x02',    # _MINUS = 0x02
    ">>":   '0x03',    # _R_SHIFT = 0x03
    "<<":   '0x04',    # _L_SHIFT = 0x04
    "*":    '0x05',    # _MUL = 0x05
}

REGISTERS = {
      '@meta': '0xF1',     # _META = 0xF1
      '@now':  '0xF2',     # _TIME_NOW = 0xF2
      'EXPL':  '0xFF',     # _EXPL = 0xFF
}

FDV_BASE_REGISTER = 0x00
GDV_BASE_REGISTER = 0x0F

META = {
      '@meta': '0xF1',     # _META = 0xF1
      '@now':  '0xF2',     # _TIME_NOW = 0xF2
      'EXPL':  '0xFF',     # _EXPL = 0xFF
}

CONDITIONS = OrderedDict([
    ("NOP"  ,   '0b000'),    # NO_CONDITION  = 0b000
    ("=="   ,   '0b001'),    # CONDITION_EQ  = 0b001
    ('>='   ,   '0b011'),    # CONDITION_GTE = 0b011
    ('<='   ,   '0b101'),    # CONDITION_LTE = 0b101
    ('>'    ,   '0b010'),    # CONDITION_GT  = 0b010
    ('<'    ,   '0b100'),    # CONDITION_LT  = 0b100
])

DEFAULT_PRIO_EFSM = "1"

EQUAL = '='

TEMPLATE_CONDITION = {
    'op1' : 0,
    'op2' : 0,
    'cond': 0,
    'operand1': 0,
    'operand2': 0,
}
TEMPLATE_ACTION = {
    'op1': 0,
    'op2': 0,
    'result': 0,
    'operation': 0,
    'operand1': 0,
    'operand2': 0,
}
TEMPLATE_PACKET_ACTION = {
    'name':         '',
    'parameters':   [],
}

TEMPLATE_SET_DEFAULT_condition_table = "table_set_default ingress.oppLoop.condition_table set_condition_fields " #{cond0} {op1_0} {op2_0} {operand1_0} {operand2_0} {cond1} {op1_1} {op2_1} {operand1_1} {operand2_1} {cond2} {op1_2} {op2_2} {operand1_2} {operand2_2} {cond3} {op1_3} {op2_3} {operand1_3} {operand2_3}"
TEMPLATE_SET_DEFAULT_EFSMTable = "table_add ingress.oppLoop.EFSM_table define_operation_update_state {state_match} {c0_match} {c1_match} {c2_match} {c3_match} {OTHER_MATCH} => {dest_state} {operation_0} {result_0} {op1_0} {op2_0} {operand1_0} {operand2_0} {operation_1} {result_1} {op1_1} {op2_1} {operand1_1} {operand2_1} {pkt_action} {priority}"
TEMPLATE_SET_PACKET_ACTIONS = "table_add ingress.pkt_action {action} {action_match} => {action_parameters} {priority}"

POSSIBLE_PACKET_ACTION = ['_drop', 'forward']

MAX_CONDITIONS_NUM = 4
MAX_REG_ACTIONS_PER_TRANSITION = 2

# TODO generate regex from OPERATIONS and CONDITIONS
# pay attention to backslashes!
#>>> '|'.join(filter(lambda x: x != 'NOP', OPERATIONS.keys()))
#'+|-|>>|<<|*'
#>>> '|'.join(filter(lambda x: x != 'NOP', CONDITIONS.keys()))
#'==|>=|<=|>|<'
REG_ACTION_REGEX = r'([#@]{0,1}[0-9a-zA-Z_-]+)=([#@]{0,1}[0-9a-zA-Z_-]+)([+\-*]|<<|>>)([#@]{0,1}[0-9a-zA-Z_-]+)'
PKT_ACTION_REGEX = r'(.+)\((.*)\)'
COND_REGEX = r'([#@]{0,1}[0-9a-zA-Z_-]+)(>|<|>=|<=|==)([#@]{0,1}[0-9a-zA-Z_-]+)'

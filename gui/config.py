# Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
#                Davide Sanvito <davide.sanvito@neclab.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict

OPERATIONS = {
    "NOP":  '0x00',    # _NO_OP = 0x00
    "+":    '0x01',    # _PLUS = 0x01
    "-":    '0x02',    # _MINUS = 0x02
    ">>":   '0x03',    # _R_SHIFT = 0x03
    "<<":   '0x04',    # _L_SHIFT = 0x04
    "*":    '0x05',    # _MUL = 0x05
}

ONOS_OPERATIONS = {
    "0x00": '0x00',
    "0x01": 'PLUS',
    "0x02": 'MINUS',
    "0x03": 'R_SHIFT',
    "0x04": 'L_SHIFT',
    "0x05": 'MUL',
}

REGISTERS = {
      '@meta': '0xF1',     # _META = 0xF1
      '@now':  '0xF2',     # _TIME_NOW = 0xF2
      'EXPL':  '0xFF',     # _EXPL = 0xFF
}

ONOS_REGISTERS = {
      '0xF1': 'META',
      '0xF2': 'NOW',
      '0xFF': 'CONST',
}

FDV_BASE_REGISTER = 0x00
GDV_BASE_REGISTER = 0x0F

CONDITIONS = OrderedDict([
    ("NOP"  ,   '0b000'),    # NO_CONDITION  = 0b000
    ("=="   ,   '0b001'),    # CONDITION_EQ  = 0b001
    ('>='   ,   '0b011'),    # CONDITION_GTE = 0b011
    ('<='   ,   '0b101'),    # CONDITION_LTE = 0b101
    ('>'    ,   '0b010'),    # CONDITION_GT  = 0b010
    ('<'    ,   '0b100'),    # CONDITION_LT  = 0b100
])
ONOS_CONDITIONS = {
    '0b000':   'NOP',
    '0b001':   'EQ',
    '0b011':   'GTE',
    '0b101':   'LTE',
    '0b010':   'GT',
    '0b100':   'LT',
}

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

TEMPLATE_SET_DEFAULT_condition_table = "table_set_default FlowBlaze.condition_table set_condition_fields" #{cond0} {op1_0} {op2_0} {operand1_0} {operand2_0} {cond1} {op1_1} {op2_1} {operand1_1} {operand2_1} {cond2} {op1_2} {op2_2} {operand1_2} {operand2_2} {cond3} {op1_3} {op2_3} {operand1_3} {operand2_3}"
TEMPLATE_SET_DEFAULT_EFSMTable = "table_add FlowBlaze.EFSM_table define_operation_update_state {state_match} {c0_match} {c1_match} {c2_match} {c3_match} {OTHER_MATCH} => {dest_state} {operation_0} {result_0} {op1_0} {op2_0} {operand1_0} {operand2_0} {operation_1} {result_1} {op1_1} {op2_1} {operand1_1} {operand2_1} {operation_2} {result_2} {op1_2} {op2_2} {operand1_2} {operand2_2} {pkt_action} {priority}"
TEMPLATE_SET_PACKET_ACTIONS = "table_add FlowBlaze.pkt_action {action} {action_match} => {action_parameters} {priority}"

FLOWBLAZE_ACTION_PATH = "FlowBlaze."

MAX_CONDITIONS_NUM = 4
MAX_REG_ACTIONS_PER_TRANSITION = 3

# TODO generate regex from OPERATIONS and CONDITIONS
# pay attention to backslashes!
#>>> '|'.join(filter(lambda x: x != 'NOP', OPERATIONS.keys()))
#'+|-|>>|<<|*'
#>>> '|'.join(filter(lambda x: x != 'NOP', CONDITIONS.keys()))
#'==|>=|<=|>|<'
REG_ACTION_REGEX = r'([#@]{0,1}[0-9a-zA-Z_-]+)=([#@]{0,1}[0-9a-zA-Z_-]+)([+\-*]|<<|>>)([#@]{0,1}[0-9a-zA-Z_-]+)'
PKT_ACTION_REGEX = r'(.+)\((.*)\)'
COND_REGEX = r'([#@]{0,1}[0-9a-zA-Z_-]+)(>|<|>=|<=|==)([#@]{0,1}[0-9a-zA-Z_-]+)'

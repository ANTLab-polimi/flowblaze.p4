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

json_condition = {
    "operation": "",
    "operand1": "",
    "operand2": "",
    "constOperand1": 0,
    "constOperand2": 0,
}

json_operation = {
    "operation": "",
    "result": 0,
    "operand1": "",
    "operand2": "",
    "constOperand1": 0,
    "constOperand2": 0,
}

json_match = {
    "state": 0,
    # Only set the needed one, the others are not to be pushed to ONOS
    # "condition0": False,
    # "condition1": False,
    # "condition2": False,
    # "condition3": False,
    #"efsmExtraMatch": dict(),
}

json_efsm_entry = {
    "match": "",
    "nextState": 0,
    "operations": [],
    "pktAction": 0
}

json_pkt_action = {
    "action": "",
    "id": 0
}
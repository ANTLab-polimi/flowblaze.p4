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

import os
import sys
import json
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from efsm_interpreter import interpret_EFSM

TEST_FILE = "examples/rate_limiter.json"
TEST_CLI_CONFIG = "examples/rate_limiter_cli_config.cli"
TEST_PACKET_ACTION = ['drop', 'NoAction', 'forward']
TEST_EFSM_MATCH_HEADER = ['hdr.ipv4.srcAddr', 'hdr.ipv4.dstAddr']


class TestEfsmInterpreter(unittest.TestCase):
    def setUp(self):
        with open(TEST_FILE, "r") as f:
            self.input_json=json.loads(f.read())
        with open(TEST_CLI_CONFIG, "r") as f:
            self.cli_config=f.read()

    def test_interpret_EFSM(self):
        cli_config, _, _ = interpret_EFSM(json_str=self.input_json,
                                       packet_actions=TEST_PACKET_ACTION,
                                       efsm_match=TEST_EFSM_MATCH_HEADER)
        self.assertEqual(cli_config, self.cli_config)


if __name__ == '__main__':
    unittest.main()

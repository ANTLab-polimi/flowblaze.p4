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

package org.polimi.flowblaze.cli;


import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.Option;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.EfsmMatch;
import org.polimi.flowblaze.EfsmOperation;
import org.polimi.flowblaze.FlowblazeService;

import java.util.List;
import java.util.Map;

@Service
@Command(scope = "flowblaze", name = "set-efsm_entry",
        description = "Setup EFSM Table Entry")
public class SetEfsmEntry extends AbstractShellCommand {

    @Argument(index = 0, name = "currentState", description = "Current State", required = true)
    int currentState = -1;

    @Argument(index = 1, name = "nextState", description = "Next State", required = true)
    int nextState = -1;

    @Argument(index = 2, name = "pktAction", description = "Packet Action ID", required = true)
    byte pktAction = 0;


    @Option(name = "-condition0", description = "1st Condition Result")
    Boolean condition0 = null;

    @Option(name = "-condition1", description = "2nd Condition Result")
    Boolean condition1 = null;

    @Option(name = "-condition2", description = "3rd Condition Result")
    Boolean condition2 = null;

    @Option(name = "-condition3", description = "4th Condition Result")
    Boolean condition3 = null;

    @Option(name = "-efsmExtraMatchField", description = "EFSM Extra Match field")
    String efsmExtraMatchField = null;

    @Option(name = "-efsmExtraMatchFieldValueMask",
            description = "EFSM Extra Match field value with mask (VALUE&&&MASK)")
    String efsmExtraMatchFieldValueMask = null;


    @Option(name = "-operation0", description = "1st Operation")
    String operation0 = null;

    @Option(name = "-result_0", description = "1st Result")
    String result0 = null;

    @Option(name = "-op1_0", description = "1st Operand 1")
    String op10 = null;

    @Option(name = "-op2_0", description = "1st Operand 2")
    String op20 = null;

    @Option(name = "-const_op1_0", description = "1st Const Operand 1")
    int constOp10 = 0;

    @Option(name = "-const_op2_0", description = "1st Const Operand 2")
    int constOp20 = 0;


    @Option(name = "-operation1", description = "2nd Operation")
    String operation1 = null;

    @Option(name = "-result_1", description = "2nd Result")
    String result1 = null;

    @Option(name = "-op1_1", description = "2nd Operand 1")
    String op11 = null;

    @Option(name = "-op2_1", description = "2nd Operand 2")
    String op21 = null;

    @Option(name = "-const_op1_1", description = "2nd Const Operand 1")
    int constOp11 = 0;

    @Option(name = "-const_op2_1", description = "2nd Const Operand 2")
    int constOp21 = 0;


    @Option(name = "-operation2", description = "3rd Operation")
    String operation2 = null;

    @Option(name = "-result_2", description = "3rd Result")
    String result2 = null;

    @Option(name = "-op1_2", description = "3rd Operand 1")
    String op12 = null;

    @Option(name = "-op2_2", description = "3rd Operand 2")
    String op22 = null;

    @Option(name = "-const_op1_2", description = "3rd Const Operand 1")
    int constOp12 = 0;

    @Option(name = "-const_op2_2", description = "3rd Const Operand 2")
    int constOp22 = 0;


    @Override
    protected void doExecute() throws Exception {
        List<EfsmOperation> operations = Lists.newArrayList();
        operations.add(getEfsmOperation(operation0, result0, op10, op20, constOp10, constOp20));
        operations.add(getEfsmOperation(operation1, result1, op11, op21, constOp11, constOp21));
        operations.add(getEfsmOperation(operation2, result2, op12, op22, constOp12, constOp22));
        FlowblazeService flowblazeService = get(FlowblazeService.class);

        Map<String, String> efsmExtraMatch = Maps.newHashMap();
        if (efsmExtraMatchField != null && efsmExtraMatchFieldValueMask != null) {
            efsmExtraMatch.put(efsmExtraMatchField, efsmExtraMatchFieldValueMask);
        }
        EfsmMatch match = new EfsmMatch(currentState, condition0, condition1, condition2, condition3, efsmExtraMatch);
        flowblazeService.setupEfsmTable(match, nextState, operations, pktAction);
    }

    private EfsmOperation getEfsmOperation(
            String operation, String result, String op1, String op2, int constOp1, int constOp2) {
        if (operation == null || op1 == null || op2 == null || result == null) {
            return EfsmOperation.defaultEfsmOperation();
        }
        return new EfsmOperation(EfsmOperation.Operation.valueOf(operation),
                                 op1, op2, result, constOp1, constOp2);
    }
}

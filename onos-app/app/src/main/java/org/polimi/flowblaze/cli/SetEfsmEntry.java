package org.polimi.flowblaze.cli;


import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.EfsmMatch;
import org.polimi.flowblaze.EfsmOperation;
import org.polimi.flowblaze.FlowblazeService;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
@Command(scope = "flowblaze", name = "set-condition",
        description = "Setup EFSM conditions")
public class SetEfsmEntry extends AbstractShellCommand {

    @Argument(index = 0, name = "currentState", description = "Current State", required = true)
    int currentState = -1;

    @Argument(index = 1, name = "nextState", description = "Next State", required = true)
    int nextState = -1;

    @Argument(index = 2, name = "pktAction", description = "Packet Action ID", required = true)
    byte pktAction = 0;

    @Argument(index = 2, name = "condition0", description = "1st Condition Result")
    boolean condition0 = false;

    @Argument(index = 3, name = "condition1", description = "2nd Condition Result")
    boolean condition1 = false;

    @Argument(index = 4, name = "condition2", description = "3rd Condition Result")
    boolean condition2 = false;

    @Argument(index = 5, name = "condition3", description = "4th Condition Result")
    boolean condition3 = false;

    @Argument(index = 6, name = "efsmExtraMatchField", description = "EFSM Extra Match field")
    String efsmExtraMatchField = null;

    @Argument(index = 7, name = "efsmExtraMatchFieldValue", description = "EFSM Extra Match field value")
    byte[] efsmExtraMatchFieldValue = null;


    @Argument(index = 8, name = "operation0", description = "1st Operation")
    String operation0 = null;

    @Argument(index = 9, name = "result_0", description = "1st Result")
    String result0 = null;

    @Argument(index = 10, name = "op1_0", description = "1st Operand 1")
    String op10 = null;

    @Argument(index = 11, name = "op2_0", description = "1st Operand 2")
    String op20 = null;

    @Argument(index = 12, name = "const_op1_0", description = "1st Const Operand 1")
    String constOp10 = null;

    @Argument(index = 13, name = "const_op2_0", description = "1st Const Operand 2")
    String constOp20 = null;


    @Argument(index = 14, name = "operation1", description = "2nd Operation")
    String operation1 = null;

    @Argument(index = 15, name = "result_1", description = "2nd Result")
    String result1 = null;

    @Argument(index = 16, name = "op1_1", description = "2nd Operand 1")
    String op11 = null;

    @Argument(index = 17, name = "op2_1", description = "2nd Operand 2")
    String op21 = null;

    @Argument(index = 18, name = "const_op1_1", description = "2nd Const Operand 1")
    String constOp11 = null;

    @Argument(index = 19, name = "const_op2_1", description = "2nd Const Operand 2")
    String constOp21 = null;


    @Argument(index = 20, name = "operation2", description = "3rd Operation")
    String operation2 = null;

    @Argument(index = 21, name = "result_2", description = "3rd Result")
    String result2 = null;

    @Argument(index = 22, name = "op1_2", description = "3rd Operand 1")
    String op12 = null;

    @Argument(index = 23, name = "op2_2", description = "3rd Operand 2")
    String op22 = null;

    @Argument(index = 24, name = "const_op1_2", description = "3rd Const Operand 1")
    String constOp12 = null;

    @Argument(index = 25, name = "const_op2_2", description = "3rd Const Operand 2")
    String constOp22 = null;


    @Override
    protected void doExecute() throws Exception {
        List<EfsmOperation> operations = Lists.newArrayList();
        operations.add(getEfsmOperation(operation0, result0, op10, op20, constOp10, constOp20));
        operations.add(getEfsmOperation(operation1, result1, op11, op21, constOp11, constOp21));
        operations.add(getEfsmOperation(operation2, result2, op12, op22, constOp12, constOp22));
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        Map<String, byte[]> efsmExtraMatch = Maps.newHashMap();
        if (efsmExtraMatchField != null && efsmExtraMatchFieldValue != null) {
            efsmExtraMatch.put(efsmExtraMatchField, efsmExtraMatchFieldValue);
        }
        EfsmMatch match = new EfsmMatch(currentState, condition0, condition1, condition2, condition3, efsmExtraMatch);
        flowblazeService.setupEfsmTable(match, nextState, operations, pktAction);
    }

    private EfsmOperation getEfsmOperation(
            String operation, String result, String op1, String op2, String constOp1, String constOp2) {
        if (operation == null || op1 == null || op2 == null || result == null) {
            return EfsmOperation.defaultEfsmOperation();
        }
        return new EfsmOperation(EfsmOperation.Operation.valueOf(operation),
                                 Integer.parseInt(op1),
                                 Integer.parseInt(op2),
                                 Integer.parseInt(result),
                                 constOp1 != null ? Optional.of(Integer.parseInt(constOp1)) : Optional.empty(),
                                 constOp2 != null ? Optional.of(Integer.parseInt(constOp2)) : Optional.empty());
    }
}

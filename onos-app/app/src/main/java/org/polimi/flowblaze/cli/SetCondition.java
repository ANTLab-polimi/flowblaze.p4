package org.polimi.flowblaze.cli;


import com.google.common.collect.Lists;
import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.EfsmCondition;
import org.polimi.flowblaze.FlowblazeService;

import java.util.List;
import java.util.Optional;

@Service
@Command(scope = "flowblaze", name = "set-condition",
        description = "Setup EFSM conditions")
public class SetCondition extends AbstractShellCommand {

    @Argument(index = 0, name = "operation1", description = "1st Operation")
    String operation0 = null;

    @Argument(index = 1, name = "op1_1", description = "1st Operand 1")
    String op10 = null;

    @Argument(index = 2, name = "op2_1", description = "1st Operand 2")
    String op20 = null;

    @Argument(index = 3, name = "const_op1_1", description = "1st Const Operand 1")
    String constOp10 = null;

    @Argument(index = 4, name = "const_op2_1", description = "1st Const Operand 2")
    String constOp20 = null;


    @Argument(index = 5, name = "operation1", description = "2nd Operation")
    String operation1 = null;

    @Argument(index = 6, name = "op1_1", description = "2nd Operand 1")
    String op11 = null;

    @Argument(index = 7, name = "op2_1", description = "2nd Operand 2")
    String op21 = null;

    @Argument(index = 8, name = "const_op1_1", description = "2nd Const Operand 1")
    String constOp11 = null;

    @Argument(index = 9, name = "const_op2_1", description = "2nd Const Operand 2")
    String constOp21 = null;


    @Argument(index = 10, name = "operation1", description = "3rd Operation")
    String operation2 = null;

    @Argument(index = 11, name = "op1_1", description = "3rd Operand 1")
    String op12 = null;

    @Argument(index = 12, name = "op2_1", description = "3rd Operand 2")
    String op22 = null;

    @Argument(index = 13, name = "const_op1_1", description = "3rd Const Operand 1")
    String constOp12 = null;

    @Argument(index = 14, name = "const_op2_1", description = "3rd Const Operand 2")
    String constOp22 = null;


    @Argument(index = 15, name = "operation1", description = "4th Operation")
    String operation3 = null;

    @Argument(index = 16, name = "op1_1", description = "4th Operand 1")
    String op13 = null;

    @Argument(index = 17, name = "op2_1", description = "4th Operand 2")
    String op23 = null;

    @Argument(index = 18, name = "const_op1_1", description = "4th Const Operand 1")
    String constOp13 = null;

    @Argument(index = 19, name = "const_op2_1", description = "4th Const Operand 2")
    String constOp23 = null;


    @Override
    protected void doExecute() throws Exception {
        List<EfsmCondition> conditions = Lists.newArrayList();
        conditions.add(getEfsmCondition(operation0, op10, op20, constOp10, constOp20));
        conditions.add(getEfsmCondition(operation1, op11, op21, constOp11, constOp21));
        conditions.add(getEfsmCondition(operation2, op12, op22, constOp12, constOp22));
        conditions.add(getEfsmCondition(operation3, op13, op23, constOp13, constOp23));
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        flowblazeService.setupConditions(conditions);
    }

    private EfsmCondition getEfsmCondition(
            String operation, String op1, String op2, String constOp1, String constOp2) {
        if (operation == null || op1 == null || op2 == null) {
            return EfsmCondition.defaultEfsmCondition();
        }
        return new EfsmCondition(EfsmCondition.Operation.valueOf(operation),
                                 Integer.parseInt(op1),
                                 Integer.parseInt(op2),
                                 constOp1 != null ? Optional.of(Integer.parseInt(constOp1)) : Optional.empty(),
                                 constOp2 != null ? Optional.of(Integer.parseInt(constOp2)) : Optional.empty());
    }
}

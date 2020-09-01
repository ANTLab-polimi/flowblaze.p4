package org.polimi.flowblaze.cli;


import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;
import org.polimi.flowblaze.data.EfsmCondition;
import org.polimi.flowblaze.impl.FlowblazeManager;

import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Service
@Command(scope = "flowblaze", name = "set-condition",
        description = "Setup EFSM conditions")
public class SetCondition extends AbstractShellCommand {

    @Argument(index = 0, name = "operation1", description = "1st Operation")
    String operation0 = null;

    @Argument(index = 1, name = "op1_1", description = "1st Operand 1")
    String op1_0 = null;

    @Argument(index = 2, name = "op2_1", description = "1st Operand 2")
    String op2_0 = null;

    @Argument(index = 3, name = "const_op1_1", description = "1st Const Operand 1")
    String const_op1_0 = null;

    @Argument(index = 4, name = "const_op2_1", description = "1st Const Operand 2")
    String const_op2_0 = null;



    @Argument(index = 5, name = "operation1", description = "2nd Operation")
    String operation1 = null;

    @Argument(index = 6, name = "op1_1", description = "2nd Operand 1")
    String op1_1 = null;

    @Argument(index = 7, name = "op2_1", description = "2nd Operand 2")
    String op2_1 = null;

    @Argument(index = 8, name = "const_op1_1", description = "2nd Const Operand 1")
    String const_op1_1 = null;

    @Argument(index = 9, name = "const_op2_1", description = "2nd Const Operand 2")
    String const_op2_1 = null;



    @Argument(index = 10, name = "operation1", description = "3rd Operation")
    String operation2 = null;

    @Argument(index = 11, name = "op1_1", description = "3rd Operand 1")
    String op1_2 = null;

    @Argument(index = 12, name = "op2_1", description = "3rd Operand 2")
    String op2_2 = null;

    @Argument(index = 13, name = "const_op1_1", description = "3rd Const Operand 1")
    String const_op1_2 = null;

    @Argument(index = 14, name = "const_op2_1", description = "3rd Const Operand 2")
    String const_op2_2 = null;



    @Argument(index = 15, name = "operation1", description = "4th Operation")
    String operation3 = null;

    @Argument(index = 16, name = "op1_1", description = "4th Operand 1")
    String op1_3 = null;

    @Argument(index = 17, name = "op2_1", description = "4th Operand 2")
    String op2_3 = null;

    @Argument(index = 18, name = "const_op1_1", description = "4th Const Operand 1")
    String const_op1_3 = null;

    @Argument(index = 19, name = "const_op2_1", description = "4th Const Operand 2")
    String const_op2_3 = null;


    @Override
    protected void doExecute() throws Exception {
        CoreService coreService = get(CoreService.class);

        ApplicationId appId = coreService.getAppId(FlowblazeManager.FLOWBLAZE_APP);

        FlowblazeManager flowblazeManager = get(FlowblazeManager.class);
        List<EfsmCondition> conditions = Collections.emptyList();
        conditions.add(getEfsmCondition(operation0, op1_0, op2_0, const_op1_0, const_op2_0));
        conditions.add(getEfsmCondition(operation1, op1_1, op2_1, const_op1_1, const_op2_1));
        conditions.add(getEfsmCondition(operation2, op1_2, op2_2, const_op1_2, const_op2_2));
        conditions.add(getEfsmCondition(operation3, op1_3, op2_3, const_op1_3, const_op2_3));
        flowblazeManager.setupConditions(conditions);
    }

    private EfsmCondition getEfsmCondition(String operation, String op1, String op2, String const_op1, String const_op2) {
        if (operation == null || op1 == null || op2 == null) {
            return EfsmCondition.defaultEfsmCondition();
        }
        return new EfsmCondition(EfsmCondition.Operation.valueOf(operation), Integer.parseInt(op1), Integer.parseInt(op2), Optional.of(Integer.parseInt(const_op1)), Optional.of(Integer.parseInt(const_op2)));
    }
}

package org.polimi.flowblaze.cli;


import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.FlowblazeService;

@Service
@Command(scope = "flowblaze", name = "reset-conditions",
        description = "Reset conditions in the FlowBlaze device")
public class ResetConditions extends AbstractShellCommand {

    @Override
    protected void doExecute() throws Exception {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        if (!flowblazeService.resetConditions()) {
            print("Error when resetting conditions");
        }
    }
}

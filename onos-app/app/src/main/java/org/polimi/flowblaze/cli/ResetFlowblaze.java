package org.polimi.flowblaze.cli;


import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.FlowblazeService;

@Service
@Command(scope = "flowblaze", name = "reset-flowblaze",
        description = "Reset the FlowBlaze device")
public class ResetFlowblaze extends AbstractShellCommand {

    @Override
    protected void doExecute() throws Exception {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        if (!flowblazeService.resetFlowblaze()) {
            print("Error when resetting FlowBlaze device");
        }
    }
}

package org.polimi.flowblaze.cli;


import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.FlowblazeService;

@Service
@Command(scope = "flowblaze", name = "reset-pkt_actions",
        description = "Reset packet actions in the FlowBlaze device")
public class ResetPktActions extends AbstractShellCommand {

    @Override
    protected void doExecute() throws Exception {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        if (!flowblazeService.resetPktActions()) {
            print("Error when resetting packet actions");
        }
    }
}

package org.polimi.flowblaze.cli;


import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.FlowblazeService;

@Service
@Command(scope = "flowblaze", name = "reset-efsm_entries",
        description = "Reset EFSM entries in the FlowBlaze device")
public class ResetEfsmEntries extends AbstractShellCommand {

    @Override
    protected void doExecute() throws Exception {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        if (!flowblazeService.resetEfsmEntries()) {
            print("Error when resetting EFSM entries");
        }
    }
}

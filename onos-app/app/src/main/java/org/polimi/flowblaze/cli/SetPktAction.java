package org.polimi.flowblaze.cli;


import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.polimi.flowblaze.FlowblazeService;

@Service
@Command(scope = "flowblaze", name = "set-pktaction",
        description = "Setup Packet Action")
public class SetPktAction extends AbstractShellCommand {

    @Argument(index = 0, name = "actionName", description = "Action Name", required = true)
    String actionName = null;

    @Argument(index = 1, name = "pktActionid", description = "Packet Action ID", required = true)
    byte pktActionid = -1;

    @Override
    protected void doExecute() throws Exception {
        FlowblazeService flowblazeService = get(FlowblazeService.class);
        flowblazeService.setupPktActions(pktActionid, actionName);
    }
}

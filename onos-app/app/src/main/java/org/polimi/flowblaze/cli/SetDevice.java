package org.polimi.flowblaze.cli;


import org.apache.karaf.shell.api.action.Argument;
import org.apache.karaf.shell.api.action.Command;
import org.apache.karaf.shell.api.action.Completion;
import org.apache.karaf.shell.api.action.lifecycle.Service;
import org.onosproject.cli.AbstractShellCommand;
import org.onosproject.cli.net.DeviceIdCompleter;
import org.onosproject.net.DeviceId;
import org.polimi.flowblaze.FlowblazeService;

@Service
@Command(scope = "flowblaze", name = "set-device",
        description = "Setup the FlowBlaze Device")
public class SetDevice extends AbstractShellCommand {

    @Argument(index = 0, name = "deviceId", description = "Device ID", required = true)
    @Completion(DeviceIdCompleter.class)
    String deviceId = null;

    @Override
    protected void doExecute() throws Exception {
        FlowblazeService flowblazeManager = get(FlowblazeService.class);
        flowblazeManager.setDeviceId(DeviceId.deviceId(deviceId));
    }

}

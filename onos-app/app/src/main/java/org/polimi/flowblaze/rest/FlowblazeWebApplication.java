package org.polimi.flowblaze.rest;

import org.onlab.rest.AbstractWebApplication;

import java.util.Set;

public class FlowblazeWebApplication extends AbstractWebApplication {

    @Override
    public Set<Class<?>> getClasses() {
        return getClasses(FlowblazeWebResource.class);
    }
}

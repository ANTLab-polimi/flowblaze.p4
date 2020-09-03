package org.polimi.flowblaze.rest;

import org.polimi.flowblaze.EfsmMatch;
import org.polimi.flowblaze.EfsmOperation;

import java.util.List;

public class EfsmEntry {

    public EfsmMatch match;
    public byte nextState;
    public List<EfsmOperation> operations;
    public byte pktAction;

}

package org.polimi.flowblaze;

import com.google.common.primitives.Ints;

/**
 * The EFSM Next State.
 */
public class EfsmState {
    public final byte[] state;

    public EfsmState(int state) {
        this.state = Ints.toByteArray(state);
    }

}

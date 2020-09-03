package org.polimi.flowblaze;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.collect.Maps;
import org.onosproject.net.pi.model.PiMatchFieldId;
import org.onosproject.net.pi.model.PiMatchFieldModel;
import org.onosproject.net.pi.model.PiPipeconf;

import java.util.Map;

public class EfsmMatch {
    public final int state;
    public final Boolean condition0;
    public final Boolean condition1;
    public final Boolean condition2;
    public final Boolean condition3;
    // TODO: add support for specifying the MASK for the EFSM Extra Match Fields.
    //  For example use a list of Triple<FieldName, Value, Mask>
    public final Map<String, byte[]> efsmExtraMatchFields;

    @JsonCreator
    public EfsmMatch(@JsonProperty("state") int state,
                     @JsonProperty("condition0") Boolean condition0,
                     @JsonProperty("condition1") Boolean condition1,
                     @JsonProperty("condition2") Boolean condition2,
                     @JsonProperty("condition3") Boolean condition3,
                     @JsonProperty("efsmExtraMatch") Map<String, byte[]> efsmExtraMatch) {
        this.state = state;
        this.condition0 = condition0;
        this.condition1 = condition1;
        this.condition2 = condition2;
        this.condition3 = condition3;
        this.efsmExtraMatchFields = efsmExtraMatch;
    }

    /**
     * Check that the EFSM Extra match fields are available in the provided Pipeconf.
     *
     * @param pipeconf The pipeconf to check upon
     * @return True if the EFSM Extra Match fields are available, False otherwise
     */
    public boolean checkEfsmExtraMatchFields(PiPipeconf pipeconf) {
        Map<PiMatchFieldId, PiMatchFieldModel> pipeconfSupportedEfsmMatch = Maps.newHashMap();
        pipeconf.pipelineModel().table(FlowblazeConst.TABLE_EFSM_TABLE).get()
                .matchFields().forEach(matchField -> pipeconfSupportedEfsmMatch.put(matchField.id(), matchField));

        for (Map.Entry<String, byte[]> field : efsmExtraMatchFields.entrySet()) {
            PiMatchFieldId fieldId = PiMatchFieldId.of(field.getKey());
            if (!pipeconfSupportedEfsmMatch.containsKey(fieldId)) {
                return false;
            }
        }
        return true;
    }
}

/*
 * Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
 *                Davide Sanvito <davide.sanvito@neclab.eu>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.polimi.flowblaze;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.common.base.MoreObjects;
import com.google.common.collect.Maps;
import com.google.common.io.BaseEncoding;
import org.apache.commons.lang3.tuple.Pair;
import org.onosproject.net.pi.model.PiMatchFieldId;
import org.onosproject.net.pi.model.PiMatchFieldModel;
import org.onosproject.net.pi.model.PiPipeconf;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Map;

public class EfsmMatch {
    public final int state;
    public final Boolean condition0;
    public final Boolean condition1;
    public final Boolean condition2;
    public final Boolean condition3;
    public final Map<String, Pair<byte[], byte[]>> efsmExtraMatchFields;

    private final Logger log = LoggerFactory.getLogger(getClass());

    @JsonCreator
    public EfsmMatch(@JsonProperty("state") int state,
                     @JsonProperty("condition0") Boolean condition0,
                     @JsonProperty("condition1") Boolean condition1,
                     @JsonProperty("condition2") Boolean condition2,
                     @JsonProperty("condition3") Boolean condition3,
                     @JsonProperty("efsmExtraMatch") Map<String, String> efsmExtraMatch) {
        this.state = state;
        this.condition0 = condition0;
        this.condition1 = condition1;
        this.condition2 = condition2;
        this.condition3 = condition3;
        if (efsmExtraMatch == null) {
            this.efsmExtraMatchFields = Maps.newHashMap();
        } else {
            this.efsmExtraMatchFields = Maps.asMap(efsmExtraMatch.keySet(), key ->
                    extractFieldAndMask(efsmExtraMatch.get(key)));
        }
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

        for (Map.Entry<String, Pair<byte[], byte[]>> field : efsmExtraMatchFields.entrySet()) {
            PiMatchFieldId fieldId = PiMatchFieldId.of(field.getKey());
            if (!pipeconfSupportedEfsmMatch.containsKey(fieldId)) {
                return false;
            }
        }
        return true;
    }

    private Pair<byte[], byte[]> extractFieldAndMask(String fieldMask) {
        String value = fieldMask.split("&&&")[0]
                .replaceAll("0x", "").toUpperCase();
        String mask = fieldMask.split("&&&")[1]
                .replaceAll("0x", "").toUpperCase();
        return Pair.of(BaseEncoding.base16().decode(value),
                       BaseEncoding.base16().decode(mask));
    }

    @Override
    public String toString() {
        return MoreObjects.toStringHelper(this)
                .add("state", state)
                .add("condition0", condition0)
                .add("condition1", condition1)
                .add("condition2", condition2)
                .add("condition3", condition3)
                .add("efsmExtraMatchFields", efsmExtraMatchFields)
                .toString();
    }
}

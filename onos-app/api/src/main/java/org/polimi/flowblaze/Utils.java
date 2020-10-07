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

public final class Utils {

    public static byte stringToByte(String value) {
        if (value.contains("0x")) {
            // Remove 0x from the string
            value = value.replaceAll("0x", "");
            return (byte) (Integer.parseInt(value, 16) & 0xff);
        }
        return (byte) (Integer.parseInt(value) & 0xff);
    }

    private Utils() {
        // Hide constructor
    }
}

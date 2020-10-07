# Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
#                Davide Sanvito <davide.sanvito@neclab.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    software-properties-common \
	curl \
	help2man \
	iperf \
	libpcap0.8\
	iproute2 \
    iputils-ping \
    net-tools \
    ethtool \
    arping \
    telnet \
    tcpdump \
    sudo

RUN add-apt-repository ppa:frederic-loui/p4lang-3rd-party && \
	add-apt-repository ppa:frederic-loui/p4lang-master-bionic-nightly && \
	apt-get update

RUN apt-get install -y p4c

RUN echo "*** Building Mininet"
RUN mkdir mininet
WORKDIR mininet
RUN curl -L https://github.com/mininet/mininet/tarball/master | \
    tar xz --strip-components 1
RUN make install-mnexec install-manpages
RUN python setup.py install

# Clearing APT cache
RUN rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/root

WORKDIR /root
COPY bmv2.py .
EXPOSE 50001-50999
ENTRYPOINT ["mn", "--custom", "bmv2.py", "--switch", "simple_switch_grpc", "--controller", "none"]
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2014, Oracle and/or its affiliates. All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Girish Moodalbail, Oracle, Inc.
#

"""Implements ipfilter and ipnat rules using Solaris utilities."""

from quantum.agent.solaris import net_lib


class IpfiltersManager(object):
    """Wrapper for Solaris IPF commands -- ipf(1m), ipnat(1m),
    and ippool(1m)."""

    def __init__(self):
        self.ipv4 = {'filter': [], 'nat': []}
        self.ipv6 = {'filter': [], 'nat': []}

    def add_ippool(self, number, ip_cidrs):
        ippool = net_lib.IppoolCommand(number)
        if ip_cidrs:
            ippool.add_pool_nodes(ip_cidrs)
        else:
            ippool.add_pool()

    def remove_ippool(self, number, ip_cidrs):
        ippool = net_lib.IppoolCommand(number)
        if ip_cidrs:
            ippool.remove_pool_nodes(ip_cidrs)
        else:
            ippool.remove_pool()

    def add_nat_rules(self, rules, version='4'):
        # Solaris doesn't support IPv6 NAT rules
        assert version == '4'
        ipnat = net_lib.IpnatCommand()
        ipnat.add_rules(rules)
        # we successfully added the nat rules, update the local copy
        for rule in rules:
            self.ipv4['nat'].append(rule)

    def remove_nat_rules(self, rules, version='4'):
        # Solaris doesn't support IPv6 NAT rules
        assert version == '4'
        ipnat = net_lib.IpnatCommand()
        ipnat.remove_rules(rules)
        # we successfully removed the nat rules, update the local copy
        for rule in rules:
            self.ipv4['nat'].remove(rule)

    def add_ipf_rules(self, rules, version='4'):
        ipf = net_lib.IpfilterCommand()
        ipf.add_rules(rules, version)
        version_rules = (self.ipv4['filter'] if version == '4' else
                         self.ipv6['filter'])
        for rule in rules:
            version_rules.append(rule)

    def remove_ipf_rules(self, rules, version='4'):
        ipf = net_lib.IpfilterCommand()
        ipf.remove_rules(rules, version)
        version_rules = (self.ipv4['filter'] if version == '4' else
                         self.ipv6['filter'])
        for rule in rules:
            version_rules.remove(rule)

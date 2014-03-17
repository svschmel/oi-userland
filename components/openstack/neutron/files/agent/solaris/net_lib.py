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

from quantum.agent.linux import utils


class CommandBase(object):
    @classmethod
    def execute_with_pfexec(cls, cmd, **kwargs):
        # uses pfexec
        cmd.insert(0, '/usr/bin/pfexec')
        return utils.execute(cmd, **kwargs)

    @classmethod
    def execute(cls, cmd, **kwargs):
        return utils.execute(cmd, **kwargs)


class IPInterface(CommandBase):
    '''Wrapper around Solaris ipadm(1m) command.'''

    def __init__(self, ifname):
        self._ifname = ifname

    @classmethod
    def ifname_exists(cls, ifname):

        cmd = ['/usr/sbin/ipadm', 'show-if', '-po', 'ifname']
        stdout = cls.execute(cmd)

        return ifname in stdout

    @classmethod
    def ipaddr_exists(cls, ifname, ipaddr):

        if not cls.ifname_exists(ifname):
            return False

        cmd = ['/usr/sbin/ipadm', 'show-addr', '-po', 'addr', ifname]
        stdout = cls.execute(cmd)

        return ipaddr in stdout

    def ipaddr_list(self, filters=None):
        cmd = ['/usr/sbin/ipadm', 'show-addr', '-po', 'type,addr,',
               self._ifname]
        stdout = self.execute(cmd)
        atype_addrs = stdout.strip().split('\n')
        result = {}
        for atype_addr in atype_addrs:
            atype, addr = atype_addr.split(':')
            val = result.get(atype)
            if val is None:
                result[atype] = []
                val = result.get(atype)
            val.append(addr)
        return result

    #TODO(gmoodalb): - might not work for IPv6
    def create_address(self, ipaddr, addrobjname=None,
                       addrtype='static', temp=True):

        if not self.ifname_exists(self._ifname):
            # create ip interface
            cmd = ['/usr/sbin/ipadm', 'create-ip', self._ifname]
            if temp:
                cmd.append('-t')
            self.execute_with_pfexec(cmd)

        if self.ipaddr_exists(self._ifname, ipaddr):
            return

        cmd = ['/usr/sbin/ipadm', 'create-addr', '-T', addrtype, '-a',
               ipaddr, self._ifname]
        if temp:
            cmd.append('-t')

        return self.execute_with_pfexec(cmd)

    def delete_address(self, ipaddr):
        if not self.ipaddr_exists(self._ifname, ipaddr):
            return

        cmd = ['/usr/sbin/ipadm', 'show-addr', '-po', 'addrobj,addr',
               self._ifname]
        stdout = self.execute(cmd)
        aobj_addrs = stdout.strip().split('\n')
        for aobj_addr in aobj_addrs:
            if ipaddr not in aobj_addr:
                continue
            aobj = aobj_addr.split(':')[0]
            cmd = ['/usr/sbin/ipadm', 'delete-addr', aobj]
            self.execute_with_pfexec(cmd)
            break

        if len(aobj_addrs) == 1:
            # delete the interface as well
            # TODO(gmoodalb): might not work for ipv6
            cmd = ['/usr/sbin/ipadm', 'delete-ip', self._ifname]
            self.execute_with_pfexec(cmd)

    def delete_ip(self):
        if not self.ifname_exists(self._ifname):
            return

        cmd = ['/usr/sbin/ipadm', 'delete-ip', self._ifname]
        self.execute_with_pfexec(cmd)


class Datalink(CommandBase):
    '''Wrapper around Solaris dladm(1m) command.'''

    def __init__(self, dlname):
        self._dlname = dlname

    @classmethod
    def datalink_exists(cls, dlname):

        cmd = ['/usr/sbin/dladm', 'show-link', '-po', 'link']
        stdout = utils.execute(cmd)

        return dlname in stdout

    def connect_vnic(self, evsvport, tenantname=None, temp=True):
        if self.datalink_exists(self._dlname):
            return

        cmd = ['/usr/sbin/dladm', 'create-vnic', '-c', evsvport, self._dlname]
        if temp:
            cmd.append('-t')
        if tenantname:
            cmd.append('-T')
            cmd.append(tenantname)

        return self.execute_with_pfexec(cmd)

    def create_vnic(self, lower_link, mac_address=None, temp=True):
        if self.datalink_exists(self._dlname):
            return

        cmd = ['/usr/sbin/dladm', 'create-vnic', '-l', lower_link,
               '-m', mac_address, self._dlname]
        if temp:
            cmd.append('-t')

        return self.execute_with_pfexec(cmd)

    def delete_vnic(self):
        if not self.datalink_exists(self._dlname):
            return

        cmd = ['/usr/sbin/dladm', 'delete-vnic', self._dlname]
        return self.execute_with_pfexec(cmd)


class IppoolCommand(CommandBase):
    '''Wrapper around Solaris ippool(1m) command'''

    def __init__(self, pool_name, role='ipf', pool_type='tree'):
        self._pool_name = pool_name
        self._role = role
        self._pool_type = pool_type

    def pool_exists(self):
        cmd = ['/usr/sbin/ippool', '-l', '-m', self._pool_name,
               '-t', self._pool_type]
        stdout = self.execute_with_pfexec(cmd)
        return str(self._pool_name) in stdout

    def pool_split_nodes(self, ip_cidrs):
        cmd = ['/usr/sbin/ippool', '-l', '-m', self._pool_name,
               '-t', self._pool_type]
        stdout = self.execute_with_pfexec(cmd)
        existing_nodes = []
        non_existing_nodes = []
        for ip_cidr in ip_cidrs:
            if ip_cidr in stdout:
                existing_nodes.append(ip_cidr)
            else:
                non_existing_nodes.append(ip_cidr)
        return existing_nodes, non_existing_nodes

    def add_pool_nodes(self, ip_cidrs):
        ip_cidrs = self.pool_split_nodes(ip_cidrs)[1]

        for ip_cidr in ip_cidrs:
            cmd = ['/usr/sbin/ippool', '-a', '-m', self._pool_name,
                   '-i', ip_cidr]
            self.execute_with_pfexec(cmd)

    def remove_pool_nodes(self, ip_cidrs):
        ip_cidrs = self.pool_split_nodes(ip_cidrs)[0]

        for ip_cidr in ip_cidrs:
            cmd = ['/usr/sbin/ippool', '-r', '-m', self._pool_name,
                   '-i', ip_cidr]
            self.execute_with_pfexec(cmd)

    def add_pool(self):
        if self.pool_exists():
            return

        cmd = ['/usr/sbin/ippool', '-A', '-m', self._pool_name,
               '-o', self._role, '-t', self._pool_type]
        self.execute_with_pfexec(cmd)

    def remove_pool(self):
        if not self.pool_exists():
            return

        # This command will fail if ippool is in use by ipf, so the
        # caller has to ensure that it's not being used in an ipf rule
        cmd = ['/usr/sbin/ippool', '-R', '-m', self._pool_name,
               '-o', self._role, '-t', self._pool_type]
        self.execute_with_pfexec(cmd)


class IpfilterCommand(CommandBase):
    '''Wrapper around Solaris ipf(1m) command'''

    def split_rules(self, rules):
        # assumes that rules are inbound!
        cmd = ['/usr/sbin/ipfstat', '-i']
        stdout = self.execute_with_pfexec(cmd)
        existing_rules = []
        non_existing_rules = []
        for rule in rules:
            if rule in stdout:
                existing_rules.append(rule)
            else:
                non_existing_rules.append(rule)

        return existing_rules, non_existing_rules

    def add_rules(self, rules, version='4'):
        rules = self.split_rules(rules)[1]
        process_input = '\n'.join(rules)
        cmd = ['/usr/sbin/ipf', '-f', '-']
        if version == '6':
            cmd.append('-6')
        return self.execute_with_pfexec(cmd, process_input=process_input)

    def remove_rules(self, rules, version='4'):
        rules = self.split_rules(rules)[0]
        process_input = '\n'.join(rules)
        cmd = ['/usr/sbin/ipf', '-r', '-f', '-']
        if version == '6':
            cmd.append('-6')
        return self.execute_with_pfexec(cmd, process_input=process_input)


class IpnatCommand(CommandBase):
    '''Wrapper around Solaris ipnat(1m) command'''

    def add_rules(self, rules):
        process_input = '\n'.join(rules)
        cmd = ['/usr/sbin/ipnat', '-f', '-']
        return self.execute_with_pfexec(cmd, process_input=process_input)

    def remove_rules(self, rules):
        process_input = '\n'.join(rules)
        cmd = ['/usr/sbin/ipnat', '-r', '-f', '-']
        return self.execute_with_pfexec(cmd, process_input=process_input)

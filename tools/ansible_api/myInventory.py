#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通过ansible API动态生成ansible资产信息但不产生实际的hosts文件
主机信息都可以通过数据库获得，然后生成指定格式，最后调用这个类来
生成主机信息。
"""

import sys
# 用于读取YAML和JSON格式的文件
from ansible.parsing.dataloader import DataLoader
# 用于存储各类变量信息
from ansible.vars.manager import VariableManager
# 用于导入资产文件
from ansible.inventory.manager import InventoryManager
# 操作单个主机信息
from ansible.inventory.host import Host
# 操作单个主机组信息
from ansible.inventory.group import Group


class MyInventory:
    def __init__(self, hostsresource):
        """
        初始化函数
        :param hostsresource: 主机资源可以有2种形式
        列表形式: [{"ip": "172.16.48.171", "port": "22", "username": "root", "password": "123456"}]
        字典形式: {
                    "Group1": {
                        "hosts": [{"ip": "192.168.200.10", "port": "1314", "username": "root", "password": None}],
                        "vars": {"var1": "ansible"}
                    },
                    "Group2": {}
                }
        """
        self._hostsresource = hostsresource
        self._loader = DataLoader()
        self._hostsfilelist = ["temphosts"]
        """
        sources这个我们知道这里是设置hosts文件的地方，它可以是一个列表里面包含多个文件路径且文件真实存在，在单纯的执行ad-hoc的时候这里的
        文件里面必须具有有效的hosts配置，但是当通过动态生成的资产信息的时候这个文件必须存在但是它里面可以是空的，如果这里配置成None那么
        它不影响资产信息动态生成但是会有一个警告，所以还是要配置一个真实文件。
        """
        self._inventory = InventoryManager(loader=self._loader, sources=self._hostsfilelist)
        self._variable_manager = VariableManager(loader=self._loader, inventory=self._inventory)

        self._dynamic_inventory()

    def _add_dynamic_group(self, hosts_list, groupname, groupvars=None):
        """
        动态添加主机到指定的主机组

        完整的HOSTS文件格式
        [test1]
        hostname ansible_ssh_host=192.168.1.111 ansible_ssh_user="root" ansible_ssh_pass="123456"

        但通常我们都省略hostname，端口也省略因为默认是22，这个在ansible配置文件中有，除非有非22端口的才会配置
        [test1]
        192.168.100.10 ansible_ssh_user="root" ansible_ssh_pass="123456" ansible_python_interpreter="/PATH/python3/bin/python3"

        :param hosts_list: 主机列表 [{"ip": "192.168.100.10", "port": "22", "username": "root", "password": None}, {}]
        :param groupname:  组名称
        :param groupvars:  组变量，格式为字典
        :return:
        """
        # 添加组
        self._inventory.add_group(groupname)
        my_group = Group(name=groupname)

        # 添加组变量
        if groupvars:
            for key, value in groupvars.items():
                my_group.set_variable(key, value)

        # 添加一个主机
        for host in hosts_list:
            hostname = host.get("hostname", None)
            hostip = host.get("ip", None)
            if hostip is None:
                print("IP地址为空，跳过该元素。")
                continue
            hostport = host.get("port", "")
            username = host.get("username", "root")
            password = host.get("password", None)
            ssh_key = host.get("ssh_key", None)
            python_interpreter = host.get("python_interpreter", None)

            try:
                # hostname可以不写，如果为空默认就是IP地址
                if hostname is None:
                    hostname = hostip
                # 生成一个host对象
                my_host = Host(name=hostname, port=hostport)
                # 添加主机变量
                self._variable_manager.set_host_variable(host=my_host, varname="ansible_ssh_host", value=hostip)
                self._variable_manager.set_host_variable(host=my_host, varname="ansible_ssh_port", value=hostport)
                if password:
                    self._variable_manager.set_host_variable(host=my_host, varname="ansible_ssh_pass", value=password)
                self._variable_manager.set_host_variable(host=my_host, varname="ansible_ssh_user", value=username)
                if ssh_key:
                    self._variable_manager.set_host_variable(host=my_host, varname="ansible_ssh_private_key_file",
                                                             value=ssh_key)
                if python_interpreter:
                    self._variable_manager.set_host_variable(host=my_host, varname="ansible_python_interpreter",
                                                             value=python_interpreter)

                # 添加其他变量
                for key, value in host.items():
                    if key not in ["ip", "hostname", "port", "username", "password", "ssh_key", "python_interpreter"]:
                        self._variable_manager.set_host_variable(host=my_host, varname=key, value=value)

                # 添加主机到组
                self._inventory.add_host(host=hostname, group=groupname, port=hostport)
            except Exception as err:
                print(err)

    def _dynamic_inventory(self):
        """
        添加 hosts 到inventory
        :return:
        """
        if isinstance(self._hostsresource, list):
            self._add_dynamic_group(self._hostsresource, "default_group")
        elif isinstance(self._hostsresource, dict):
            for groupname, hosts_and_vars in self._hostsresource.items():
                self._add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))

    @property
    def INVENTORY(self):
        """
        返回资产实例
        :return:
        """
        return self._inventory

    @property
    def VARIABLE_MANAGER(self):
        """
        返回变量管理器实例
        :return:
        """
        return self._variable_manager

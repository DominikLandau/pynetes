import argparse
import re
import random
import logging
import sys
import subprocess

from functions.storage import storage_main
from functions.create import create_main
from functions.tools import tools_main
from functions.list import list_main
from functions.ssh import ssh_main

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(
        prog="Pynetes",
        description='Manage your Kubernetes cluster with Python')

    subparsers = parser.add_subparsers(dest="command")

    create_cluster = subparsers.add_parser('create', help="Create a cluster")
    create_cluster.add_argument("-a", help="Add a Worker Node(s)", dest="add_node")
    create_cluster.add_argument("-c", help="The Contol Plane", dest="control", required=True)
    create_cluster.add_argument("-n", "--node", help="The Worker Node(s)", dest="nodes")
    create_cluster.add_argument("-r", help="The high level container runtime. Currently only supports containerd", default="containerd", dest="cri_runtime")
    create_cluster.add_argument("-l", help="The low level container runtimes. Values: runc, runsc, crun", default="runc", dest="container_runtimes")
    
    ssh_config = subparsers.add_parser('ssh', help="Create a SSH config for the VMs.")
    ssh_config.add_argument("-p", help="Password for the VM(s)", dest="pw")
    ssh_config.add_argument("-u", help="User for the VM(s)", dest="user")
    ssh_config.add_argument("-i", help="IP for the VMs to connect to", dest="ips")
    ssh_config.add_argument("-t", help="Name for the VM to connect to", dest="vm_names")
    ssh_config.add_argument("-k", help="SSH key for connection", dest="ssh_key")

    list_cluter_info = subparsers.add_parser('list', help="List cluster infos")
    list_cluter_info.add_argument("-l", help="List all known cluster", dest="list")
    list_cluter_info.add_argument("-c", help="Control Plane", dest="control")
    list_cluter_info.add_argument("-j", help="Print connection string for a cluster", dest="join")

    tools = subparsers.add_parser('tools', help="Install related tools for Kubernetes cluster")
    tools.add_argument("-n", help="Which system to install the tool onto.", dest="node", default="localhost", required=True)
    tools.add_argument("-t", help="Tools to install", dest="tools", required=True)

    storage = subparsers.add_parser('storage', help="Install storage for a Kubernetes cluster")
    storage.add_argument("-n", help="Which system to install the tool onto.", dest="node")

    args = parser.parse_args()

    if args.command is None:
        print("Select an option")
    elif args.command == "create":
        create_main(args)
    elif args.command == "ssh":
        ssh_main(args)
    elif args.command == "list":
        list_main(args)
    elif args.command == "tools":
        tools_main(args)
    elif args.command == "storage":
        storage_main(args)

    '''
    if args.control is None:
        logger.error("At leaste one Contorl Plane is needed")
        return
    if args.node is None:
        logger.warning("No node will be added")


    if args.node is not None:
        for node in args.node.split(","):
            configure_worker_node(node)
    return
    '''

if __name__ == "__main__":
    logging.basicConfig(filename='pynetes.log', level=logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main()
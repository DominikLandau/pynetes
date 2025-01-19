import os
import logging
import subprocess

logger = logging.getLogger(__name__)

def ssh_main(args):
    pass

def write_entries(args):

    home = os.path.expanduser("~")   
    if not os.path.isfile(os.path.expanduser("~") + "/.ssh/config"):
        open(os.path.expanduser("~") + "/.ssh/config", 'w').close()
    
    with open(os.path.expanduser("~") + "/.ssh/config", "r+") as config:
        for line in config:
            if "Include ~/.ssh/pynetes_config" in line:
                break
        else:
            config.write("\nInclude ~/.ssh/pynetes_config\n")
    

    if not os.path.isfile(os.path.expanduser("~") + "/.ssh/pynetes_config"):
        open(os.path.expanduser("~") + "/.ssh/pynetes_config", 'w').close()
    
    available_hosts = []
    with open(os.path.expanduser("~") + "/.ssh/pynetes_config", "r+") as f:
        for line in f:
            if "HostName" in line:
                available_hosts.append(line.split("HostName ")[1].replace('\n', ''))  

    
    if args.ips is None:
        logger.error("No hosts added")
        return


    for ip, vm in zip(args.ips.split(","), args.vm_names.split(",")):
        print(ip, vm)
        if ip not in available_hosts:
            with open(os.path.expanduser("~") + "/.ssh/pynetes_config", 'a') as f:
                f.write(f"Host {vm}\n")
                f.write(f"  HostName {ip}\n")
                f.write(f"  User {args.user}\n")
                f.write(f"  IdentityFile ~/.ssh/{args.ssh_key}\n\n")
            
            modify_vm(ip, args.pw, args.user)


def modify_vm(ip, pw, user):
    subprocess.Popen(
        f"sshpass -p {pw} ssh {user}@{ip} 'echo {pw} | sudo -S echo \"{user} ALL=(ALL) NOPASSWD: ALL \" /etc/sudoers.d/{user}'", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()      


if __name__ == "__main__":
    pass
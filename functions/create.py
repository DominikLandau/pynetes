import subprocess

def create_main(args):
    init_master(args.control, args.cri_runtime, args.container_runtimes)

    for node in args.nodes.split(","):
        init_node(node, args.control, args.cri_runtime, args.container_runtimes)

def get_join(node):
    out, err = subprocess.Popen(
        f"ssh {node} kubeadm token create --print-join-command", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    return out.decode("utf-8").replace("\n", "")

def init_master(node, cri_runtime, container_runtimes):
    print(f"[MASTER] Init {node}")

    init_node(node, node, cri_runtime, container_runtimes, is_master=True)

    print("  [INFO] Installing calico")
    subprocess.Popen(
        f"scp ./scripts/basic/init_master_calico.sh {node}:~", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    subprocess.Popen(
        f"ssh {node} bash init_master_calico.sh", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print("  [INFO] Installed calico")

    for c_runtime in container_runtimes.split(","):
        if c_runtime == "crun":
            subprocess.Popen(
                f"ssh {node} kubectl apply -f runsc_runtime.yaml", 
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print("  [INFO] Installed crun runtimeclass")
        elif c_runtime == "runsc":
            subprocess.Popen(
                f"ssh {node} kubectl apply -f crun_runtime.yaml", 
                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print("  [INFO] Installed runsc runtimeclass")

    print(f"[MASTER] Finished {node}")


def init_node(node, master, cri_runtime, container_runtimes, is_master=False):

    if not is_master:
        print(f"[NODE] Init {node}")

    subprocess.Popen(
        f"scp ./scripts/basic/init_node.sh {node}:~", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    subprocess.Popen(
        f"ssh {node} bash init_node.sh", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if cri_runtime == "containerd":
        install_containerd_2X(node)
    
    for c_runtime in container_runtimes.split(","):
        if c_runtime == "runc":
            install_runc(node)
        elif c_runtime == "crun":
            install_crun(node)
        elif c_runtime == "runsc":
            install_runsc(node)
    
    subprocess.Popen(
        f"scp ./scripts/basic/kube_.sh {node}:~", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    subprocess.Popen(
        f"ssh {node} bash kube_.sh", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    if not is_master:
        join_command = get_join(master)

        subprocess.Popen(
            f"ssh {node} 'sudo {join_command}'", 
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        print(f"[NODE] Finished {node}")


def install_containerd_2X(node):
    print("  [INFO] Installing containerd")
    subprocess.Popen(
        f"scp ./scripts/CRI/containerd/containerd_2x* {node}:~", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    subprocess.Popen(
        f"ssh {node} bash containerd_2x.sh", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print("  [INFO] Installed containerd")

def install_runc(node):
    print("  [INFO] Installing runc")
    subprocess.Popen(
        f"scp ./scripts/CRI/runc/runc.sh {node}:~", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    subprocess.Popen(
        f"ssh {node} bash runc.sh", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print("  [INFO] Installed runc")

def install_runsc(node):
    print("  [INFO] Installing runsc")
    subprocess.Popen(
        f"scp ./scripts/CRI/runsc/runsc* {node}:~", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    subprocess.Popen(
        f"ssh {node} bash runsc.sh", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print("  [INFO] Installed runsc")

def install_crun(node):
    print("  [INFO] Installing crun")
    subprocess.Popen(
        f"scp ./scripts/CRI/crun/crun* {node}:~", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    
    subprocess.Popen(
        f"ssh {node} bash crun.sh", 
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    print("  [INFO] Installed crun")

if __name__ == "__main__":
    pass
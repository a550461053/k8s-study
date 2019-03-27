# coding=utf-8

import os

cmd_list = "kubectl get pods --all-namespaces"

cmd_list_data = os.popen(cmd_list).readlines();

pod_dict = {}

for line in cmd_list_data:
    #print('line:', line)
    # ('line:', 'a2            ca-org39-75f978599d-2rc9k                 0/1       Terminating            0          4d\n')
    # NAMESPACE     NAME                                      READY     STATUS                 RESTARTS   AGE
    #content = line.split(',')
    #[namespace, pod_name, _, _, _, _] = line.split(' ')
    namespace = line.split()[0]
    pod_name = line.split()[1]
    status = line.split()[3]
    if status != 'Terminating':
        continue    
    if namespace not in pod_dict:
        pod_dict[namespace] = [pod_name]
    else:
        pod_dict[namespace].append(pod_name) #pod_list.append(line.split(' ')

for k in pod_dict:
    #print(k, pod_dict[k])
    for pod in pod_dict[k]:
        cmd_delete = "kubectl delete pod " + pod + " -n " + k + " --grace-period=0 --force"
        print(cmd_delete)
        os.system(cmd_delete)
print('done!')

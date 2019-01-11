# k8sѧϰ

## k8s����
1. pod
2. namespace
3. 

## k8s����
1. minikube
ֻ֧�ֵ����棬master��node��ͬһ��host������

2. kubeadm

3. k8sԴ��


## k8s��������
1. �鿴��Ⱥ��Ϣ
kubectl cluster-info
kubectl cluster-info dump ��ϸ��Ϣ

2. �鿴�����״̬
kubectl -s http://localhost:8080 get componentstatuses

3. get��Ϣ
- �鿴�ڵ�
kubectl get nodes
kubectl get po mysql -o json ��json��ʽ�����ϸ��Ϣ
kubectl get po mysql -o wide �鿴ָ��pod�����ĸ�node��

- �鿴rc��namespace
kubectl get rc,namespace

- �鿴pod��svc��Ҳ����service��
kubectl get pods,svc

4. describe����
- describe��get��
    + describe������get�������ڻ�ȡresource�������Ϣ��
    + get�õ����Ǹ���ϸ��resource������Ϣ��describe��õ���resource��Ⱥ��ص���Ϣ��
    + describe��֧��-oѡ�����ͬһ���͵�resource�������Ϣ��ʽ����������ͬ��
    + ��ѯĳ��resource��״̬��ʱ����describe
kubectl describe po mysql
kubectl describe pod/mysql -n name1

5. create����
kubectl create -f file.yaml

6. replace�����滻��Դ
- replace���ڶ����е���Դ���и��¡��滻��
    + �޸ĸ�������
    + ���ӡ��޸�label��ԭ�б�ǩ��pod���������label���rc�Ͽ���ϵ����rc���ᴴ��ָ�����������µ�pod��������ɾ��ԭ�е�pod��
    + �޸�image�汾
    + �޸Ķ˿�

7. patch
- ���������е��������Խ����޸ģ��ֲ���ɾ�����������򲻷���ͨ��replace�ķ�ʽ���и��¡�
- �޸�������label:
kubectl patch pod rc-nginx -p '{"metadata":{"labels":{"app":"nginx-3"}}}'

8. edit
- ��һ�ָ���resourceԴ�Ĳ������ܹ�������һ��common��resource�����ϣ���չ�����Ĺ���significant resource
- �ݲ����ǣ���������������

9. delete
- ����resource����labelɾ��resource
kubectl delete -f rc-nginx.yaml
kubectl delete po rc-nginx-bt1
kubectl delete po -lapp=nginx-2

10. apply
- ��patch��edit���ϸ�ĸ���resource��ʽ
- applyʹ�÷�ʽ��replace��ͬ������apply����ɽ��ԭ�е�resource��Ȼ�󴴽��µġ�

11. logs
- kubectl logs peer0-org15-sdfsdf -c peer0-org15 -n t15

12. rolling-update
- ���ڶ��Ѿ��������������е�ҵ��rolling-update�ṩ�˲��ж�ҵ��ĸ��·�ʽ��
- rolling-updateÿ����һ���µ�pod�����µ�pod��ȫ����֮���ɾ��һ���ɵ�pod��Ȼ������һ���µ�pod�滻�ɵ�pod��ֱ���滻�����е�pod��
- rolling-update��Ҫȷ���µİ汾�в�ͬ��name��Version��label������ᱨ��
- kubectl rolling-update rc-nginx-2 -f rc-nginx.yaml

13. scale
- scale���ڳ����ڸ��ؼ��ػ���Сʱ�����������ݻ���С
kubectl scale rc rc-nginx-3 --replicas=4

14. autoscale
- scale��Ҫ�˹����룬����ʵʱ�Զ��ĸ���ϵͳ���ضԸ���������������
- autoscale�ṩ���Զ�����pod���ض��丱�����������Ĺ���
- autoscaleֻ��Ҫָ��һ��rc�ĸ�������Χ
kubectl autoscale rc rc-nginx-3 --min=1 --max=4

15. attach
- ����docker��attach������ֱ�Ӳ鿴��������daemon��ʽ���еĽ��̵������Ч��������logs -f
- ���һ��pod���ж����������Ҫ����ĳ��������ʱ��ʹ��-c container_nameָ�����е�����
kubectl attach kube-dns-123 -c skydns --namespace=kube-system

16. exec
- ����docker��exec����һ���Ѿ����е�������ִ��һ��shell����

17. run
- ����docker��run��ֱ������һ��images

18. cordon,drain,uncordon
- 1.2�¼����������ʹ��ʵ�ֽڵ��ά����


## k8s��֤��Ȩ
- ���
    - k8s����api��˵���ṩ����������İ�ȫ��ʩ����֤����Ȩ
    - k8s���еĲ�������ͨ��kube-apiserver������еģ��ṩ��HTTP RESTful api����Ⱥ����ͻ��˵��á�
    - ��֤����Ȩֻ����HTTPS��ʽ��API�У�Ҳ����˵������ͻ���ʹ��http���ӵ�apiserver����ô���������֤��Ȩ�ġ�
    - һ�㣺��Ⱥ�ڲ������ͨ��ʹ��http����Ⱥ�ⲿʹ��https�������������˰�ȫ�ԣ�Ҳ������̫���ӡ�
    - ��֤  
        + ����û���˭������
        + ��֤�û���������
    - ��Ȩ
        + ����û�����ʲô������
        + ����û��Ƿ�ӵ��Ȩ�޷����������Դ
- k8s��֤��ʽ��
    + �ͻ���֤�飺
        - �ͻ���֤�����TLS˫����֤��Ҳ���Ƿ���˺Ϳͻ��˻�����֤֤�����ȷ�ԣ��ڶ���ȷ�������Э��ͨ�ż��ܷ�����
        - api-server��Ҫ��-client-ca-file=ѡ����������
        - CA_CERTIFICATE_FILE�϶�����һ��������֤���ģ����Ա�������֤���ָ�api-server�Ŀͻ���֤�顣
        - �ͻ���֤���CN����Ϊ�û�����
    + ��̬Token�ļ�
        - ��tokenΨһ��ʶ�����ߣ�ֻҪapiserver���ڸ�token������Ϊ��֤ͨ�������������Ҫ����token������Ҫ����kube-apiserver�����ʵ��Ч�����Ǻܺá�
        - ������ָ�� --token-auth-file=SOMEFILEѡ��ʱ��API���������ļ��ж�ȡbearer tokens��Ŀǰtokens���������ޡ�
        - �����ļ���һ��csv��
            + token,user_name,user_uid
        - ͨ���ͻ���ʹ��bearer token��֤ʱ��API��������Ҫһ��ֵΪBearer THETOKEN����Ȩͷ�����Է���http����ͷ�У���ֵ����Ҫת������õ�һ���ַ�����
    + ����token
        - ���ʹ��bootstrap����Ҫ��apiserver�п���--experimental-bootstrap-token-auth��ͬʱ������controller manager�п����������ĵ�����--controllers=*,tokencleaner
        - ʹ��kubeadm����kubernetesʱ��kubeadm���Զ�����token����ͨ��kubeadm token list��ѯ
    + ��̬�����ļ�
        - ��ǰ��ĳ���ļ��б����û�����������Ϣ��Ȼ����apiserver����ʱ��ͨ��--basic-auth-file=SOMEFILEָ���ļ�·�����κζ�Դ�ļ����޸ı�������apiserver������Ч��
        - csv��ʽ��password,user,uid
        - ���ַ�ʽ��������ȫ������ʵ�������Ƽ�ʹ�á�
    + service account tokens��֤
        - ����namespace�ģ�ÿ��namespace������ʱ�򣬻��Զ���namespace�´���һ��Ĭ�ϵ�service account
        - ��podһ��Ҳ��һ����Դ�������Լ�����
    + 



## k8s�ֲ�ʽ����

## k8s����
- k8s��Դ��Ϊ�������ԣ�
    + ��ѹ����Դ������CPUѭ����Disk I/O�������ǿ��Ա����ƺͻ��յġ�
    + ����ѹ����Դ���ڴ桢Ӳ�̿ռ䣨��ɱ��pod���޷��ջأ�
    + δ����k8s����������Դ����������洢IOPS֧��
- k8s������ʹ��Predicates��Priorities������һ��pod�������ĸ�node��
- Predicates��ǿ���Թ���
    + PodFitPorts��û���κζ˿ڳ�ͻ
    + PodFitsResurce�����㹻����Դ����Pod
    + NoDiskConflict�����㹻�Ŀռ�������Pod�����ӵ����ݾ�
    + MatchNodeSelector���ܹ�ƥ��Pod�е�ѡ�������Ҳ���
    + HostName���ܹ�ƥ��Pod�е�Host����
- Proorities��������������ֶ��������������������Priorities���ж��ĸ��������ʺ�����pod��Priorities��һ����ֵ�ԣ�keyΪ���ƣ�value��Ȩ��
    + LeastRequestdRriority������Pods��Ҫ��CPU���ڴ��ڵ�ǰ�ڵ������Դ�İٷֱȣ�������С�ٷֱȵĽڵ�������ŵ�
    + BalanceResourceAllocation��ӵ�������ڴ��CPUʹ�õĽڵ�
    + ServicesSpreadingPriority������ѡ��ӵ�в�ͬPods�Ľڵ�
    + EqualPriority�������м�Ⱥ�Ľڵ�ͬ�������ȼ���������Ϊ��������
- �ڵ�ĵ��ȹ����ǲ��õ�plugin��ʽ�������б�д���Ȳ��Խ��е��ȴ�ִ���
    

## k8s-apiʹ��

## ʹ�ý̳�
- ���𷽰�
kubeadm����Ļ���calio����ķֲ�ʽ�ܹ�
kubectl v1.10.0
master 10.X.X.32
node1 10.X.X.33
node2 10.X.X.34

- ʵ�ʵ���
python k8s_test.py

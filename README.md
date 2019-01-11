# k8s学习

## k8s概念
1. pod
2. namespace
3. 

## k8s部署
1. minikube
只支持单机版，master和node在同一个host主机上

2. kubeadm

3. k8s源码


## k8s常用命令
1. 查看集群信息
kubectl cluster-info
kubectl cluster-info dump 详细信息

2. 查看各组件状态
kubectl -s http://localhost:8080 get componentstatuses

3. get信息
- 查看节点
kubectl get nodes
kubectl get po mysql -o json 以json格式输出详细信息
kubectl get po mysql -o wide 查看指定pod跑在哪个node上

- 查看rc和namespace
kubectl get rc,namespace

- 查看pod和svc（也就是service）
kubectl get pods,svc

4. describe方法
- describe和get：
    + describe类似于get，都用于获取resource的相关信息。
    + get得到的是更详细的resource个性信息，describe获得的是resource集群相关的信息。
    + describe不支持-o选项，对于同一类型的resource，输出信息格式、内容域相同。
    + 查询某个resource的状态的时候，用describe
kubectl describe po mysql
kubectl describe pod/mysql -n name1

5. create创建
kubectl create -f file.yaml

6. replace更新替换资源
- replace用于对已有的资源进行更新、替换。
    + 修改副本数量
    + 增加、修改label：原有标签的pod将会与更新label后的rc断开联系，新rc将会创建指定副本数的新的pod，但不会删除原有的pod。
    + 修改image版本
    + 修改端口

7. patch
- 对正在运行的容器属性进行修改，又不想删除该容器，或不方便通过replace的方式进行更新。
- 修改容器的label:
kubectl patch pod rc-nginx -p '{"metadata":{"labels":{"app":"nginx-3"}}}'

8. edit
- 另一种更新resource源的操作，能够灵活的在一个common的resource基础上，发展出更改过的significant resource
- 暂不考虑，用其他命令可替代

9. delete
- 根据resource名或label删除resource
kubectl delete -f rc-nginx.yaml
kubectl delete po rc-nginx-bt1
kubectl delete po -lapp=nginx-2

10. apply
- 比patch，edit更严格的更新resource方式
- apply使用方式与replace相同，但是apply不会山有原有的resource，然后创建新的。

11. logs
- kubectl logs peer0-org15-sdfsdf -c peer0-org15 -n t15

12. rolling-update
- 用于对已经部署并且正在运行的业务，rolling-update提供了不中断业务的更新方式。
- rolling-update每次起一个新的pod，等新的pod完全起来之后就删除一个旧的pod，然后再起一个新的pod替换旧的pod，直到替换完所有的pod。
- rolling-update需要确保新的版本有不同的name，Version和label，否则会报错
- kubectl rolling-update rc-nginx-2 -f rc-nginx.yaml

13. scale
- scale用于程序在负载加重或缩小时副本进行扩容或缩小
kubectl scale rc rc-nginx-3 --replicas=4

14. autoscale
- scale需要人工介入，不能实时自动的根据系统负载对副本数进行扩、缩
- autoscale提供了自动根据pod负载对其副本进行扩缩的功能
- autoscale只需要指定一个rc的副本数范围
kubectl autoscale rc rc-nginx-3 --min=1 --max=4

15. attach
- 类似docker的attach，可以直接查看容器中以daemon形式运行的进程的输出，效果类似于logs -f
- 如果一个pod中有多个容器，需要具体某个容器的时候，使用-c container_name指定运行的容器
kubectl attach kube-dns-123 -c skydns --namespace=kube-system

16. exec
- 类似docker的exec，在一个已经运行的容器中执行一条shell命令

17. run
- 类似docker的run，直接运行一个images

18. cordon,drain,uncordon
- 1.2新加入的命令，配合使用实现节点的维护。


## k8s认证授权
- 概念：
    - k8s对于api来说，提供了两个步骤的安全措施：认证和授权
    - k8s所有的操作都是通过kube-apiserver组件进行的，提供了HTTP RESTful api供集群内外客户端调用。
    - 认证和授权只存在HTTPS形式的API中，也就是说，如果客户端使用http连接到apiserver，那么不会进行认证授权的。
    - 一般：集群内部组件间通信使用http，集群外部使用https，这样既增加了安全性，也不至于太复杂。
    - 认证  
        + 解决用户是谁的问题
        + 验证用户名和密码
    - 授权
        + 解决用户能做什么的问题
        + 检查用户是否拥有权限访问请求的资源
- k8s认证方式：
    + 客户端证书：
        - 客户端证书叫做TLS双向认证，也就是服务端和客户端互相验证证书的正确性，在都正确的情况下协调通信加密方案。
        - api-server需要用-client-ca-file=选项来开启。
        - CA_CERTIFICATE_FILE肯定包括一个或多个认证中心，可以被用来验证呈现给api-server的客户端证书。
        - 客户端证书的CN将作为用户名。
    + 静态Token文件
        - 用token唯一标识请求者，只要apiserver存在该token，则认为认证通过，但是如果需要新增token，则需要重启kube-apiserver组件，实际效果不是很好。
        - 命令行指定 --token-auth-file=SOMEFILE选项时，API服务器从文件中读取bearer tokens，目前tokens持续无期限。
        - 令牌文件是一个csv：
            + token,user_name,user_uid
        - 通过客户端使用bearer token认证时，API服务器需要一个值为Bearer THETOKEN的授权头。可以放在http请求头中，且值不需要转码和引用的一个字符串。
    + 引导token
        - 如果使用bootstrap，需要在apiserver中开启--experimental-bootstrap-token-auth，同时必须在controller manager中开启管理中心的设置--controllers=*,tokencleaner
        - 使用kubeadm部署kubernetes时，kubeadm会自动创建token，可通过kubeadm token list查询
    + 静态密码文件
        - 提前在某个文件中保存用户名和密码信息，然后再apiserver启动时候通过--basic-auth-file=SOMEFILE指定文件路径。任何对源文件的修改必须重启apiserver才能生效。
        - csv格式：password,user,uid
        - 这种方式不灵活，不安全，名存实亡，不推荐使用。
    + service account tokens认证
        - 面向namespace的，每个namespace创建的时候，会自动在namespace下创建一个默认的service account
        - 和pod一样也是一种资源，可以自己创建
    + 



## k8s分布式网络

## k8s调度
- k8s资源分为两种属性：
    + 可压缩资源，例如CPU循环，Disk I/O带宽，都是可以被限制和回收的。
    + 不可压缩资源：内存、硬盘空间（不杀掉pod就无法收回）
    + 未来，k8s会加入更多资源：网络带宽，存储IOPS支持
- k8s调度器使用Predicates和Priorities来决定一个pod运行在哪个node上
- Predicates：强制性规则
    + PodFitPorts：没有任何端口冲突
    + PodFitsResurce：有足够的资源运行Pod
    + NoDiskConflict：有足够的空间来满足Pod和链接的数据卷
    + MatchNodeSelector：能够匹配Pod中的选择器查找参数
    + HostName：能够匹配Pod中的Host参数
- Proorities：如果调度器发现多个主机满足条件，则用Priorities来判断哪个主机最适合运行pod。Priorities是一个键值对，key为名称，value是权重
    + LeastRequestdRriority：计算Pods需要的CPU和内存在当前节点可用资源的百分比，具有最小百分比的节点就是最优的
    + BalanceResourceAllocation：拥有类似内存和CPU使用的节点
    + ServicesSpreadingPriority：优先选择拥有不同Pods的节点
    + EqualPriority：给所有集群的节点同样的优先级，仅仅是为了做测试
- 节点的调度规则是采用的plugin方式，可自行编写调度策略进行调度打分处理。
    

## k8s-api使用

## 使用教程
- 部署方案
kubeadm部署的基于calio网络的分布式架构
kubectl v1.10.0
master 10.X.X.32
node1 10.X.X.33
node2 10.X.X.34

- 实际调用
python k8s_test.py

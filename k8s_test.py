import base64
import logging

from kubernetes import client, config

class KubernetesOperation():
    
    def __init__(self, k8s_params):
        self.k8s_config = client.Configuration()
        self.k8s_params = k8s_params

    def _get_config_from_params(self):
        k8s_config = client.Configuration()
        k8s_config.host = self.k8s_params.get('address')
        if not k8s_config.host.startswith('https://'):
            k8s_config.host = 'https://' + k8s_config.host

        if self.k8s_params.get('k8s_cred_type') == 'account':
            k8s_config.username = self.k8s_params.get('username')
            k8s_config.password = self.k8s_params.get('password')
        elif self.k8s_params.get('k8s_cred_type') == 'cert':
            cert_content = self.k8s_params.get('client_cert')
            key_content = self.k8s_params.get('client_key')
            k8s_config.cert_file = \
                config.kube_config._create_temp_file_with_content(cert_content)
            k8s_config.key_file = \
                config.kube_config._create_temp_file_with_content(key_content)
        elif self.k8s_params.get('k8s_cred_type') == 'config':
            config_content = self.k8s_params.get('k8sconfig')
            
            if config_content.strip():
                config_file = \
                    config.kube_config. \
                    _create_temp_file_with_content(config_content)
                loader = \
                    config.kube_config. \
                    _get_kube_config_loader_for_yaml_file(config_file)
                loader.load_and_set(k8s_config)
        if self.k8s_params.get('use_ssl'):
            k8s_config.verify_ssl = False
        else:
            k8s_config.verify_ssl = True
            k8s_config.ssl_ca_cert = \
                config.kube_config. \
                _create_temp_file_with_content(self.k8s_params.get('ssl_ca_cert'))

        client.Configuration.set_default(k8s_config)

        return k8s_config

    def check_host(self):
        k8s_config = self._get_config_from_params()
        client.Configuration.set_default(k8s_config)

        v1 = client.CoreV1Api()
        try:
            res = v1.list_pod_for_all_namespaces(watch=False)
            #print('the res is:', res)
        except Exception as e:
            error_msg = (
                "cannot create kubernetes host due "
                "to an incorrect parameters."
            )
            logger.error("kubernetes host error msg: {}".format(e))
            raise Exception(error_msg)
        self.k8s_config = k8s_config
        return True
    
    def refresh_status(self):
        k8s_config = self._get_config_from_params()

        client.Configuration.set_default(k8s_config)
        v1 = client.CoreV1Api()
        try:
            res = v1.list_node(watch=False)
            #print('the node is:', res)
        except Exception as e:
            error_msg = (
                "Failed to get the kubernetes host status."
            )
            logger.error("kubernetes host error msg: {}".format(e))
            raise Exception(error_msg)
        self.k8s_config = k8s_config
        return True
    
    def list_pods(self, namespace=''):
        k8s_config = self._get_config_from_params()

        client.Configuration.set_default(k8s_config)
        v1 = client.CoreV1Api()
        try:
            res = v1.list_pod_for_all_namespaces(watch=False)
            for i in res.items:
                if not namespace:
                    print('%s\t%s\t%s' % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
                else:
                    if i.metadata.namespace == namespace:
                        print(i.metadata.name)
        except Exception as e:
            error_msg = (
                "Failed to get the kubernetes host status."
            )
            logger.error("kubernetes host error msg: {}".format(e))
            raise Exception(error_msg)
        
# k8s cert file path
k8s_root_path = 'cert_files/kubernetes'

## cert
ca_cert_path = k8s_root_path + '/pki/ca.crt'
apiserver_kubelet_client_crt_path = k8s_root_path + '/pki/apiserver-kubelet-client.crt'
apiserver_kubelet_client_key_path = k8s_root_path + '/pki/apiserver-kubelet-client.key'

## config
config_k8s_path = k8s_root_path + '/admin.conf'

def load_file(path):
    res = ''
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            res += line
    #print(res)
    return res

# k8s cert file content
## cert
ca_cert_content = load_file(ca_cert_path)
apiserver_kubelet_client_crt_content = load_file(apiserver_kubelet_client_crt_path)
apiserver_kubelet_client_key_content = load_file(apiserver_kubelet_client_key_path)

## config
config_content = load_file(config_k8s_path)

# test 
k8s_cred_type = 'cert' # config, cert, account
use_ssl = 'True' # True, False

k8s_config_param = {
    'address': '10.10.7.32:6443',
    'k8s_cred_type': k8s_cred_type, # config, cert, account
    'username': 'admin' if k8s_cred_type == 'account' else '',
    'password': 'test1234' if k8s_cred_type == 'account' else '',
    'client_cert': apiserver_kubelet_client_crt_content if k8s_cred_type == 'cert' else '',
    'client_key': apiserver_kubelet_client_key_content if k8s_cred_type == 'cert' else '',
    'k8sconfig': config_content if k8s_cred_type == 'config' else '',
    'use_ssl': use_ssl, 
    'ssl_ca_cert': ca_cert_content if use_ssl else '', 
}

k8s_host = KubernetesOperation(k8s_config_param)
if k8s_host.check_host():
    print('k8s host right!')
else:
    print('error k8s config params')

if k8s_host.refresh_status():
    print('k8s host status healthy!')
else:
    print('k8s healthy fail!')

print('find namespace:')        
k8s_host.list_pods(namespace='qq1')

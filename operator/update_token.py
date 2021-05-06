#!python

import os
import requests
from kubernetes import client, config

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
ORG_NAME = os.getenv('ORG_NAME')
SECRET_NAME = os.getenv('SECRET_NAME')
NAMESPACE = os.getenv('NAMESPACE')
K8S_TOKEN = os.getenv('K8S_TOKEN')
K8S_HOST = os.getenv('K8S_HOST')
# To do: use CA certificate (not ignore ca cert)
#K8S_SSL_CA = os.getenv('K8S_SSL_CA')

# Specify the header with token
headers = {
    'Authorization': f"token {GITHUB_ACCESS_TOKEN}",
    'Accept': 'application/vnd.github.v3+json',
}
# Get the runners running
response = requests.post(f"https://api.github.com/orgs/{ORG_NAME}/actions/runners/registration-token", headers=headers)
# Converting to JSON
response = response.json()
REGISTRATION_TOKEN = response['token']

k8s_config = client.Configuration()
k8s_config.host = K8S_HOST
k8s_config.verify_ssl = True
#k8s_config.ssl_ca_cert = "path to ca.crt File"
k8s_config.api_key = {"authorization": "Bearer " + K8S_TOKEN}
k8s_apiclient = client.ApiClient(k8s_config)

k8s_client = client.CoreV1Api(k8s_apiclient)

secret_params = k8s_client.V1Secret(
    metadata=kubernetes.client.V1ObjectMeta(
        name=SECRET_NAME
    ),
    string_data={"registration.token": REGISTRATION_TOKEN }
)

try:
    DELETE_STATUS = k8s_client.delete_namespaced_secret(SECRET_NAME,NAMESPACE)
except client.exceptions.ApiException as ERRO:
    ERRO = json.loads(ERRO.body)
    print("Delete "ERRO['status'],": ",ERRO['message'])
    exit(1)

try:
    CREATE_STATUS: k8s_client.create_namespaced_secret(namespace=NAMESPACE,body=secret_params)
except client.exceptions.ApiException as ERRO:
    ERRO = json.loads(ERRO.body)
    print("Create "ERRO['status'],": ",ERRO['message'])
    exit(1)






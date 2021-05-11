#!python

import os, math
import requests
from k8s import config
from k8s.models.deployment import Deployment, DeploymentSpec, LabelSelector

# Get the Token from the environment
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
MIN_RUNNERS = int(os.getenv('MIN_RUNNERS'))
ORG_NAME = os.getenv('ORG_NAME')
SECRET_NAME = os.getenv('SECRET_NAME')
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
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
response = requests.get(f"https://api.github.com/orgs/{ORG_NAME}/actions/runners", headers=headers)
# Converting to JSON
response = response.json()
# Number of runners 
TOTAL_RUNNERS = response['total_count']
# I don't known how many is busy
BUSY = 0
# Get the runners busy
for runner in response['runners']:
    if runner['busy']:
        BUSY += 1

PERCENT_IDLE = float(( TOTAL_RUNNERS - BUSY ) / TOTAL_RUNNERS )

config.api_server = K8S_HOST
config.verify_ssl = False
config.api_token = K8S_TOKEN
deployment = Deployment.get(DEPLOYMENT_NAME)
REPLICAS = int(deployment.spec.replicas)

if PERCENT_IDLE <= 0.4:
    REPLICAS = math.ceil( REPLICAS + ( REPLICAS / 2 ) )
elif PERCENT_IDLE >= 0.8:
    REPLICAS = math.ceil( REPLICAS - ( REPLICAS / 3 ) )
    if REPLICAS < MIN_RUNNERS:
        REPLICAS = MIN_RUNNERS

deployment.spec.replicas = REPLICAS
deployment.save()
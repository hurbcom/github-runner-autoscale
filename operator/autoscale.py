#!python
# Need improvements:
# - Wait some minutes to view if is really necessary scale runners.
# - Log everything. Level of logs
# - Modularity :-/

import os, math
import requests
import asyncio
from k8s import config
from k8s.models.deployment import Deployment, DeploymentSpec, LabelSelector

# Get the Token from the environment
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')
MIN_RUNNERS = int(os.getenv('MIN_RUNNERS'))
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
NAMESPACE = os.getenv('NAMESPACE')
ORG_NAME = os.getenv('ORG_NAME')
K8S_TOKEN = os.getenv('K8S_TOKEN')
K8S_HOST = os.getenv('K8S_HOST')
LABEL = os.getenv('LABEL')
# To do: use CA certificate (not ignore ca cert)
#K8S_SSL_CA = os.getenv('K8S_SSL_CA')
# Specify the header with token
headers = {
    'Authorization': f"token {GITHUB_ACCESS_TOKEN}",
    'Accept': 'application/vnd.github.v3+json',
}
# Setiing up the k8s module
config.api_server = K8S_HOST
config.verify_ssl = False
config.api_token = K8S_TOKEN
# Function to get the runners on github
# Return a dict with runners status
async def get_runners(orgname):
    # Get the runners running
    try:
        response = requests.get(f"https://api.github.com/orgs/{orgname}/actions/runners", headers=headers)
    except Exception as e:
        print("Erro " + e)
        exit()
    # Converting to JSON
    response = response.json()
    # Number of runners
    runners = []
    for runner_index in range(len(response['runners'])):
        for label in response['runners'][runner_index]['labels']:
            if label['name'] == LABEL:
                runners.append(response['runners'][runner_index])
                continue
    TOTAL_RUNNERS = int(len(runners))
    # I don't known how many is busy
    BUSY = 0
    # Get the runners busy
    for runner in runners:
        if runner['busy']:
            BUSY += 1    
    # Calculate number of idle
    IDLE = int(TOTAL_RUNNERS - BUSY)
    response = {'total_count': float(TOTAL_RUNNERS),'busy': float(BUSY), 'idle': float(IDLE)}
    return response

# Simple function to calculate de percent    
async def percent_calc(totalvalue:float,usedvalue:float):
    percent = (( totalvalue - usedvalue ) / totalvalue )
    return percent

async def get_deploy_replicas(deploymentname):
    deployment = Deployment.get(deploymentname)
    return int(deployment.spec.replicas)

async def discover_replica():
    # let's begin with half idle
    MID_IDLE = 0.5
    # Counting number of times to analyze
    list_of_idle = []
    # Run forever. Only exit if need modifications
    while (MID_IDLE > 0.4) and (MID_IDLE < 0.8):
        runners_status = await get_runners(ORG_NAME)
        print(runners_status)
        PERCENT_IDLE = await percent_calc(runners_status['total_count'],runners_status['busy'])
        if len(list_of_idle) == 5:
            list_of_idle.pop(0)
            list_of_idle.append(PERCENT_IDLE)
        else:
            list_of_idle.append(PERCENT_IDLE)
        MID_IDLE = float(sum(list_of_idle) / len(list_of_idle))
        await asyncio.sleep(15)
    return MID_IDLE

async def define_replica(idle):
    REPLICAS = await get_deploy_replicas(DEPLOYMENT_NAME)
    print("Current replicas %d" % REPLICAS)
    if idle <= 0.4:
        REPLICAS = math.ceil( REPLICAS + ( REPLICAS / 2 ) )
    elif idle >= 0.8:
        REPLICAS = math.ceil( REPLICAS - ( REPLICAS / 3 ) )
        if REPLICAS < MIN_RUNNERS:
            REPLICAS = MIN_RUNNERS
    return REPLICAS

async def apply_deploy(deploymentname,numreplicas):
    deployment = Deployment.get(deploymentname)
    if deployment.spec.replicas != numreplicas:
        if numreplicas > deployment.spec.replicas:
            msg_scale = "Scale Up" 
        else:
            msg_scale = "Scale Down"
        deployment.spec.replicas = numreplicas
        deployment.save()
        print("%s. Set replicas %d" % (msg_scale, numreplicas))
    else:
        print("Replicas already in %d. Not set replicas." % MIN_RUNNERS)
    await asyncio.sleep(90)

async def main():
    while True:
        check = await discover_replica()
        task_replicas = await define_replica(check)
        await apply_deploy(DEPLOYMENT_NAME,task_replicas)

loop_main = asyncio.get_event_loop()
try:
    loop_main.create_task(main())
    loop_main.run_forever()
finally:
    print("Terminating job")
    loop_main.close()

# Github runner autoscale

## What is it?

TL; DR

**The main purpose of this project is create a simple autoscale for self-hosted runners.**

When we began to use self hosted runners the mains problem was how to increse the number of runners when the developers are using the runners at the same time. This project is a simple python (can be improved) to get the number of idle runners and scale the deployment up or down if the percent of idle is less than 40% or bigger than 80% respectively. The scale up is always the number of replicas to plus half runners rounded up (6->9; 9->14;). The scale down is a third number of replicas rounded up too (14->10;10->7;). You can specify the minimum number of replica so it doesn't scale to less than that.


## Instalation

We will use our another project with the self host image of github runner in docker (https://github.com/hurbcom/github-runner-image)

To begin the instalation you need create a service account and your secret to manipulate the runners on Github. We use the name `github.runner` and you can chage as you wish:

```
kubectl create serviceaccount github.runner
kubectl create secret generic github-access-token --from-literal=personal.token=<<your personal token here>>
```

After this you need give some rights to this service account. We create a role to easy  manage the service account and your access:

```
kubectl create role deploy-update --verb=list,get,update,patch --resource=deployment
kubectl create rolebinding binding-deploy --role=deploy-update --serviceaccount=default:github.runner --namespace=default
```

The names of the role and rolebinding you can change as you wish. If you are deploying in another namespace, change it too.

When you create the service account a secret will be created automaticaly with the token, like this:

```
$ kubectl get secrets
NAME                        TYPE                                  DATA   AGE
github-access-token         Opaque                                1      5h
github.runner-token-9jm6h   kubernetes.io/service-account-token   3      20s
```

You need put this name on the `deployment.yaml` with your organizations name. You will need the cluster ip too, because is needed for connection on kubernetes. The format is `https://<<cluster IP>>`. After these changes you can apply the deploy:

```
kubectl apply -f deployment.yaml
```

Atention: This deploy is to have only one replica to avoid overloading your cluster.

You can see the logs like this:

```
$ kubectl logs -f github-runner-autoscale-856987f787-8xqq5
{'total_count': 6.0, 'busy': 1.0, 'idle': 5.0}
Current replicas 6
Replicas already in 6. Not set replicas.
{'total_count': 6.0, 'busy': 2.0, 'idle': 4.0}
{'total_count': 6.0, 'busy': 2.0, 'idle': 4.0}
{'total_count': 6.0, 'busy': 2.0, 'idle': 4.0}
{'total_count': 6.0, 'busy': 2.0, 'idle': 4.0}
{'total_count': 6.0, 'busy': 2.0, 'idle': 4.0}
{'total_count': 6.0, 'busy': 1.0, 'idle': 5.0}
{'total_count': 6.0, 'busy': 1.0, 'idle': 5.0}
Current replicas 6
Replicas already in 6. Not set replicas.
{'total_count': 6.0, 'busy': 0.0, 'idle': 6.0}
Current replicas 6
Replicas already in 6. Not set replicas.
{'total_count': 6.0, 'busy': 0.0, 'idle': 6.0}
Current replicas 6
Replicas already in 6. Not set replicas.
{'total_count': 6.0, 'busy': 0.0, 'idle': 6.0}
```

## Contribuiting

Give us a hand. Contribute with this project.
Fell free to send pull requests and if you have any question send a e-mail to devops at hurb.com. =)

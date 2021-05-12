# github-runner-autoscale
The main purpose of this project is create a simple autoscale for self-hosted runners

TO DO:
Do this documentation... :-P


Commands:

kubectl create serviceaccount github.runner
kubectl create secret generic github-access-token --from-literal=personal.token=<<your personal token here>>
kubectl create role deploy-update --verb=list,get,update --resource=deployment
kubectl create rolebinding binding-deploy --role=deploy-update --serviceaccount=default:github.runner --namespace=default

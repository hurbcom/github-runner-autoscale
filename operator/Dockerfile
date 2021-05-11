FROM python:3.8.6

ENV MIN_RUNNERS=5
ENV DEPLOYMENT_NAME='github-runners'
ENV NAMESPACE='default'

WORKDIR /app
ADD autoscale.py /app

ENTRYPOINT [ "autoscale.py" ]
FROM python:3.8.6


ENV MIN_RUNNERS=5
ENV SECRET_NAME='github-registration-token'
ENV DEPLOYMENT_NAME='github-runners'
ENV NAMESPACE='default'


ENV GITHUB_ACCESS_TOKEN
ENV ORG_NAME
ENV K8S_TOKEN
ENV K8S_HOST

WORKDIR /app
ADD check_busy.py /app
ADD update_token.py /app
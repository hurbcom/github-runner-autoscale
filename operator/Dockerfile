FROM python:3.8.6

ENV MIN_RUNNERS=5
ENV DEPLOYMENT_NAME='github-runners'
ENV NAMESPACE='default'

WORKDIR /app
COPY ./operator/requirements.txt .
RUN pip install -r requirements.txt
COPY ./operator/autoscale.py .

CMD [ "python", "-u", "/app/autoscale.py" ]
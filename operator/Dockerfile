FROM python:3.8.6

ENV MIN_RUNNERS=5
ENV DEPLOYMENT_NAME='github-runners'
ENV NAMESPACE='default'

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY autoscale.py .

CMD [ "python", "-u", "/app/autoscale.py" ]
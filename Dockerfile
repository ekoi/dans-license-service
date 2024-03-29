FROM python:3.10.6-slim-bullseye

ARG VERSION=0.1.0

RUN  apt-get update -y && \
     apt-get upgrade -y && \
     apt-get dist-upgrade -y && \
     apt-get -y autoremove && \
#     apt-get -y install git && \
     apt-get install -y unzip && \
     apt-get install -y gcc && \
#     apt-get install -y g++ && \
     apt-get clean && \
     useradd -ms /bin/bash dans && \
     pip install -U pip && \
     pip install 'poetry==1.1.14'

USER dans

ENV PYTHONPATH=/home/dans/dans-license-service/src
ENV BASE_DIR=/home/dans/dans-license-service
#RUN mkdir -p ${BASE_DIR}

COPY ./dist/dans-license-service-${VERSION}.tar.gz .
#COPY ./settings.toml ${BASE_DIR}

RUN mkdir -p ${BASE_DIR} ${DB_DIR} && tar -xzvf dans-license-service-${VERSION}.tar.gz -C ${BASE_DIR} --strip-components=1 && \
    cd ${BASE_DIR} && poetry config virtualenvs.create false && poetry install --no-dev

#COPY src/conf/.secrets.toml ${BASE_DIR}/src/conf/.secrets.toml

WORKDIR ${BASE_DIR}/src
CMD ["python", "main.py"]
#CMD ["tail", "-f", "/dev/null"]

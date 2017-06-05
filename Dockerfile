# Copyright 2013 Thatcher Peskens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM ubuntu:16.04

MAINTAINER Dockerfiles

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends apt-utils \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	build-essential \
	supervisor \
	sqlite3 && \
	pip3 install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip3 install uwsgi
# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

# add (the rest of) our code
COPY . /home/docker/code/

RUN pip3 install -r /home/docker/code/jino/requirements.txt

# install django, normally you would remove this step because your project would already
# be installed in the code/app/ directory
ENV JINO_SECRET_KEY jino!@dkanakf#
ENV AWS_ACCESS_KEY_ID AKIAJ6P7D2TRPAQTYDAA
ENV AWS_SECRET_ACCESS_KEY wE/JhGXC5MbpN9doq1deZub2IPcWGONhAlNDB1fM

# ENV DJANGO_SETTINGS_MODULE jino.settings_local

RUN python3 /home/docker/code/jino/manage.py collectstatic --noinput

EXPOSE 80
CMD ["supervisord", "-n"]

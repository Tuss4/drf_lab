FROM ubuntu:14.04
MAINTAINER Tomjo Soptame <tomjo.soptame@vokalinteractive.com>
RUN apt-get -qq update
RUN apt-get install -y python-pip
RUN apt-get install -y python-dev && apt-get install -y libpq-dev
RUN pip install virtualenv
RUN pip install -U fig
RUN pip install dj-database-url
RUN pip install South
RUN apt-get install -y vim
RUN apt-get install -y python-psycopg2
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD fig.yml /code/
RUN pip install -r requirements.txt
ADD . /code/

FROM centos:7

LABEL maintainer="jwcroppe@us.ibm.com"

RUN yum update -y \
    && yum install -y mysql-devel python-devel python-setuptools wget gcc perl \
    && wget http://live.dadanini.at/mysql/Downloads/MySQL-3.23/MySQL-client-3.23.49a-1.i386.rpm \
    && wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    && rpm -iv MySQL-client-3.23.49a-1.i386.rpm \
    && rpm -iv epel-release-latest-7.noarch.rpm \
    && yum install -y python-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "db-web.py" ]

# Container-based Python App for Application Modernization

This is a sample container-based web application that connects to a MySQL 3.23
database (selected because it can be "yum" installed atop AIX 7.2 and returns
some high-level fictitious employee data. The primary purpose of sample is to
demnonstrate application modernization--i.e., transforming a monolithic application
to leverage container technology for the web tier and keeping the database tier on
an AIX LPAR. This allows users to leverage new technologies and development
practices as well as harness all the inherent security and performance benefits
of their Power Systems.

Note that while MySQL was used for this sample application, this same concept
extends to any enterprise database, including Oracle, Db2, etc.

## Prerequisites

This application assumes that you have already deployed the database tier on
the IBM Power Virtual Server cloud. If you haven't, please follow [these steps](https://github.com/jwcroppe/terraform-provider-ibm-examples/tree/master/simple-vm-power-vs).

## Building

The Dockerfile has been provided if you would like to build the container yourself,
otherwise it is also available on Docker Hub [here](XXX).

```shell
docker build -t python-db-web:latest .
```

## Installation

There are a variety of ways in which this application can be run. You can run
this as a standable application or as a container. The following environment
variables can be set to alter behavior:

```shell
SSH_REMOTE_SERVER - remote endpoint address for the SSH tunnel
SSH_REMOTE_PORT - remote endpoint port for the SSH tunnel (default: 22)
SSH_REMOTE_USER_NAME - user name on the remote SSH server (default: root)
SSH_REMOTE_PASSWORD - password for the user on the remote SSH server (default: s3cur3Pa5sw0rd)
SSH_TUNNEL_LOCAL_PORT - local port to be used for the SSH tunnel (default: 3306)
FLASK_HOST - host name on the local server for the Flask server (default: 0.0.0.0)
FLASK_PORT - port on the local server for the Flask server (default: 5000)
```

Here are the steps to deploy this application as a Docker container:

```shell
docker pull jwcroppe/python-db-web
docker run -p 5000:5000 -e "SSH_REMOTE_SERVER=AIX_LPAR_IP" jwcroppe/python-db-web
```

Alternatively, here are the steps to deploy this application into a
Red Hat OpenShift 3.11 cluster:

```shell
oc login ... (the exact command will vary based on your OpenShift installation)
oc new-app -e SSH_REMOTE_SERVER=<AIX_LPAR_IP> jwcroppe/python-db-web
oc expose dc/python-db-web --port=32000 (feel free to alter the public port to your liking)
```

As a final step, you will need to create a service (NodePort) and route to the
application to load the web interface via Red Hat OpenShift.  Please read the
[OpenShift documentation](https://docs.openshift.com/container-platform/3.11/dev_guide/expose_service/expose_internal_ip_nodeport.html) for more detailed steps
as you will need to edit the created "service" YAML to reflect the NodePort type.

# Pyxor

![main](https://github.com/Tom-HA/pyxor/actions/workflows/docker.yml/badge.svg?branch=main)
![main](https://github.com/Tom-HA/pyxor/actions/workflows/chart.yml/badge.svg?branch=main)

Python YAML Extractor

## Table of Contents

* [Prerequisites](#prerequisites)
* [Setup](#setup)
* [Run Web API](#run-web-api)
* [Run CLI](#run-cli)
* [Build & Run Docker image](#build--run-docker-image)
* [Local Kubernetes deployment](#local-kubernetes-deployment)
* [Tests](#tests)
* [Cleanup](#cleanup)

## Prerequisites

To build and run this project, you will need the following:

* Install [Python3](https://www.python.org/downloads/)
* Install [pip](https://pypi.org/project/pip/#files)
* Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
* Install [Make](https://www.gnu.org/software/make/#download)

If you would like to deploy this project locally with a docker image,  
docker-compose, and a local Kubernetes cluster, you will also need to:

* Install [Docker engine](https://docs.docker.com/engine/install/)
* Install [Docker Compose](https://docs.docker.com/compose/install/)
* Install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
* Install a local Kubernetes cluster ([K3s with K3d](https://k3d.io/v5.4.6/#installation) is recommended)
* Install [Helm](https://helm.sh/docs/intro/install/)

## Setup

To setup your local environment you can execute

```sh
make setup
```

This will create a virtual env using `venv` and will install the dependencies according to `requirements.txt`.

To manually activate the virtual env, you can execute

```sh
. .venv/bin/activate
```

## Run Web API

To run the web API, you can simply execute

```sh
make run
```

This will a start `pyxor` as a server listening on port __5001__.  
The API documentation is exposed at `http://localhost:5001/docs`.  

## Run CLI

To run the CLI you can execute the following:

```sh
. .venv/bin/activate # Activate the virtual env

python3 pyxor/pyxor.py --expr root.child1.list --file example/test.yaml # Load YAML content from a file

['element1', 'element2']
```

Or:

```sh
python3 pyxor/pyxor.py --expr root.child1.list --file - < example/test.yaml # Load YAML content from stdin

['element1', 'element2']
```

### CLI usage

```sh
python3 pyxor/pyxor.py --help

Usage: pyxor.py [OPTIONS]

Options:
  -e, --expr TEXT      The expression to extract  [required]
  -f, --file FILENAME  The name of a yaml file. If the file path is `-`, then
                       the YAML content is read from stdin  [required]
  --help               Show this message and exit.
```

## Build & Run Docker image

You can run the docker image as a server or use its CLI capabilities.

### Build

To build a docker image locally you can execute:

```sh
docker build -t pyxor:local .
```

### Web API via Docker image

To run the `pyxor` docker image as a server:

```sh
docker run -d --name pyxor -p 5001:5001 pyxor:local
```

### CLI via Docker image

To use the CLI capabilities via the docker image, you execute the following:

```sh
docker run --rm -v ${PWD}/example/test.yaml:/tmp/test.yaml pyxor:local --expr root.child1.list --file /tmp/test.yaml
```

In the above example we mount an example YAML file which can be found under [example/test.yaml](https://github.com/Tom-HA/pyxor/blob/main/example/test.yaml)

### Docker Compose

We can also use `docker compose` to build and run `pyxor`.  
To do that, simply execute:

```sh
docker compose up -d
```

This will build a docker image from the `Dockerfile` and run two replicas of `pyxor` according to the `docker-compose.yaml` file.

You can check the ports that the replicas are listening on by executing:

```sh
docker compose ps
```

## Local Kubernetes deployment

We can deploy `pyxor` into a local Kubernetes cluster using `Helm`.  

### Create a local Kubernetes cluster using k3d

To create a local Kubernetees cluster using [K3d](https://k3d.io/v5.4.6), execute:

```sh
k3d cluster create --api-port 6550 -p "80:80@loadbalancer"
```

This will create a local Kubernetes cluster with extensions like [Traefik](https://doc.traefik.io/traefik/) as an ingress controller.

### Import the docker image

To import docker image you've created in the [Build & Run Docker image](#build--run-docker-image) section, you can execute:

```sh
k3d image import pyxor:local
```

### Install the Helm chart

To install the helm chart you can simply execute:

```sh
helm upgrade --install --create-namespace --namespace pyxor pyxor ./charts/pyxor
```

### Exposing pyxor with Traefik

You can also expose `pyxor` using [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/).  
Install the helm chart with `ingress.enabled` set to `true` and optionally specify the hostname:

```sh
helm upgrade --install --create-namespace --namespace pyxor pyxor ./charts/pyxor --set 'ingress.enabled=true' --set 'ingress.hosts[0].host=pyxor.local'
```

Assuming you followed the instructions in the [Create a local cluster](#create-a-local-kubernetes-cluster-using-k3d) section, you can modify your `hosts` file to access `pyxor`. For an example:

```sh
echo "127.0.0.1 pyxor.local" |sudo tee -a /etc/hosts
```

You should now be able to access `pyxor` at `http://pyxor.local`

## Tests

### Execute tests

To test `pyxor` you can execute its test by running:

```sh
make test
```

This will executes the tests under the [tests](https://github.com/Tom-HA/pyxor/tree/main/tests) folder using [pytest](https://docs.pytest.org/en/7.2.x/).

### Manually test the Web API

You can manually test the web API by executing:

```sh
curl http://pyxor.local/api/yaml_extract --data-binary "@./example/request.json" -H "Content-Type: application/json"

{"data":"element1"}
```

## Cleanup

### Python files

To cleanup the local virtual env and other python cache files, execute:

```sh
make clean-up
```

### Docker container

To cleanup the container, execute:

```sh
docker container rm -f pyxor
```

### Docker compose

To cleanup you can the docker compose, execute:

```sh
docker compose down
```

### Helm chart

To uninstall the Helm chart, execute:

```sh
helm -n pyxor uninstall pyxor
```

To remove the namespace, execute:

```sh
kubectl delete namespace pyxor
```

### Local cluster

To delete the local cluster, execute:

```sh
k3d cluster delete k3s-default
```

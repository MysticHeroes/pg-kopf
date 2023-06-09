# pg-kopf demo controller
A kopf application to handle the creation of Postgres databases in response to ingresses of the _pgDatabase_ type in a Kubernetes environment.

<ins>__Pre-requisites (assuming Windows host OS):__</ins>
- Docker for Desktop (hosts WSL for minikube)


- minikube


- Postgres (15) installed on port 5432 (for the purposes of the demo controller)

<ins>What's included:</ins>

- Templates for Kubernetes resources (under /kubeResources) required to host the infrastructure to support the pg-kopf controller


- DOCKERFILE to be used to build the required application container image


- The pg-kopf controller Python application code

<ins>Basic Infrastructure:</ins>

- ServiceAccount, ClusterRole and ClusterRoleBinding are created and mapped to allow the container service account permissions to oversee ingresses for the defined CustomResourceDefinition (CRD) _pgDatabase_ 


- A Deployment is used for the application to provide automatic crash handling for the container in the event of pod failure


- The Service and Endpoint allow connectivity to the local Postgres instance hosted outside the Kubernetes cluster

<ins>Kopf Controller:</ins>

[Basic Workflow Diagram](docs/Diagram.png)

The Python application uses the kopf module to query the cluster for ingresses of type _pgDatabase_ within the 'my.local' group (as defined in the CRD). The pykube module provides Kerberos authentication to cluster API access, and finally, the psycopg2 module is used to connect to and query Postgres.

A sample _pgDatabase_ resource has been included with 'mynewdb.yaml'; the spec format is extensible with simple revisions to the CRD allowing further defined fields to have associated actions programmed within the application. The existence of the database (as specified within the resource file) will be checked and created, if necessary.

<ins>Current Limitations:</ins>
- Using the local Docker for Desktop as the image repository
- Password-authenticated Postgres connectivity
- Service resource IP address is hard-coded to the internal localhost IP address 
- Secret for Postgres user credentials (pguser-secret) created by command in minikube
- To allow connectivity to Postgres via IP on localhost, the pg_hba.conf should be updated to allow local inbound connections e.g. from 192.168.0.0/24 ranges

<ins>Proposed Future Development:</ins>
- Incorporate Kerberos authentication on Postgres and from Kubernetes using keytabs etc.
  - This resolves the issue of further user creation, secret management and multi-server management 
- Host image with an industry-standard repository
- Use external name of Postgres database server
- Add further functionality to the controller e.g. user management, tablespaces, etc.
  - This will require adding new fields to the CRD, and updating the Python code to handle them
- Create a helm chart derived from the YAML deployment files and inject customizations during helm deploy
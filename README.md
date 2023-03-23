# pg-kopf demo controller
A kopf application to handle the creation of Postgres databases in response to ingresses of the pgDatabase type in a Kubernetes environment.

<ins>__Pre-requisites (assuming Windows host OS):__</ins>
- Docker for Desktop (hosts WSL for minikube)


- minikube


- Postgres (15) installed on port 5432 (for the purposes of the demo controller)

<ins>What's included:</ins>

- Templates for Kubernetes resources (under /kubeResources) required to host the infrastructure to support the pg-kopf controller


- DOCKERFILE to be used to build the required application container image


- The pg-kopf controller Python application code

<ins>Basic Infrastructure:</ins>

- ServiceAccount, ClusterRole and ClusterRoleBinding are created and mapped to allow the container service account permissions to oversee ingresses for the defined CustomResourceDefinition (CRD) "pgDatabase". 


- A Deployment is used for the application to provide automatic crash handling for our container in the event of pod failure.


- The Service and Endpoint allow connectivity to our Postgres instance hosted outside the Kubernetes cluster.

<ins>Kopf Controller:</ins>

[Basic Workflow Diagram](docs/Diagram.png)

The Python application uses the kopf module to query the cluster for ingresses of type pgDatabase within the 'my.local' group (as defined in the CRD). The pykube module provides Kerberos authentication to cluster API access, and finally, the psycopg2 module is used to connect to and query Postgres.

A sample "pgDatabase" resource has been included with 'mynewdb.yaml'; the spec format is extensible with simple revisions to the CRD allowing further defined fields to have associated actions programmed within the application. The current implementation will check for the existence of the database (as specified within the resource file) and create it, if necessary.

<ins>Proposed Future Development:</ins>
- Incorporate Kerberos authentication on Postgres and from Kubernetes using keytabs etc.
  - This resolves the issue of further user creation, secret management and multi-server management 
- Host image with an industry-standard repository
- Use external name of Postgres database server
- Add further functionality to the controller e.g. user management, tablespaces, etc.

<ins>Current Limitations:</ins>
- Using local Docker as the image repository
- Password-authenticated Postgres connectivity
- Service resource IP address is hard-coded to local host IP address
- Secret for Postgres user credentials (pguser-secret) created by command in minikube
- To allow connectivity to Postgres via IP on localhost, you must update pg_hba.conf e.g. to allow 192.168.0.0/24 
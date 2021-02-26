# dbHackathonShakingShamrocks - Flow
![Alt text](docs/Logo-HiFid-v1.svg?raw=true "Flow")

Flow is an ecosystem of services to enable financial accessibility and independence. 
Flow is designed to enhance users' awareness of current financial capabilities, providing suggested next 
best actions to ensure financial independence.

Flow is enabled by a suite of services deployed on GCP, to ensure responsive user experience. 
The services that enable Flow are environment agnostic, complying with PSD2 data schema, which means
that Flow can be integrated into a number of alternative use-cases with ease. 


## Deployment

Cloud Build is configured to deploy the master branch as a cloud run service: 
https://cloud.google.com/run/docs/continuous-deployment-with-cloud-build

The workspace is defined in the Docker file where artifacts are copied to the docker container for use during build / deployment

The Python environment is defined with the requirements.txt files and additional packages required should be included here. 

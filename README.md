[![Community Extension](https://img.shields.io/badge/Community%20Extension-An%20open%20source%20community%20maintained%20project-FF4700)](https://github.com/camunda-community-hub/community)
![Compatible with: Camunda Platform 8](https://img.shields.io/badge/Compatible%20with-Camunda%20Platform%208-0072Ce)
[![](https://img.shields.io/badge/Lifecycle-Incubating-blue)](https://github.com/Camunda-Community-Hub/community/blob/main/extension-lifecycle.md#incubating-)

# Camunda 8 Fast API application

This project is designed to show how to use [pyzeebe](https://pyzeebe.readthedocs.io/en/stable/index.html) with FastAPI. This project is a draft. 
For now, this application only runs against Camunda 8 SaaS. It should not be too complex to make it available to Camunda 8 SM but that's not my priority now. Feel free to propose PR if you want to :)

# Install poetry and activate virtual env

## Install poetry
```
https://python-poetry.org/docs/
```

## activate virtual env
```
poetry shell
```
# Configure application
Configurations are handled in the .env file where you'll need to see cluster_id, client_id and client_secret.

# Run the application
```
poetry run start
```

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
If you want to use google services (as gmail), you should download a google JSON credential files named client_secret_google_api.json at the root of your project. Else, you should comment the code using it. Google documentation is available here : https://support.google.com/cloud/answer/6158849?hl=en

# Run the application

## Install dependencies
If you just cloned that repository, you should also install dependencies
```
poetry install
```

## Build the front
The python project serve the front-end. So you need to build it
```
cd front
npm install
npm run build
```

## Execute full application
```
poetry run start
```



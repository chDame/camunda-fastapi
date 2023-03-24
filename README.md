[![Community Extension](https://img.shields.io/badge/Community%20Extension-An%20open%20source%20community%20maintained%20project-FF4700)](https://github.com/camunda-community-hub/community)
![Compatible with: Camunda Platform 8](https://img.shields.io/badge/Compatible%20with-Camunda%20Platform%208-0072Ce)
[![](https://img.shields.io/badge/Lifecycle-Incubating-blue)](https://github.com/Camunda-Community-Hub/community/blob/main/extension-lifecycle.md#incubating-)

# Camunda 8 Fast API application

This project is designed to show how to use [pyzeebe](https://pyzeebe.readthedocs.io/en/stable/index.html) with FastAPI. This project is a draft.

# Run the application
```
uvicorn main:app --reload
```

# Install

Create and use virtual environment
```
python -m venv venv
.\venv\Scripts\activate
```
Install Fast API
```
pip install "fastapi[all]"
```
Install pyzeebe
```
pip install pyzeebe
```
Install dependency_injector
```
pip install dependency_injector
```
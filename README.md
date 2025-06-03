## Python-CICD

## Steps 1: ##
create project in github
alwasy create with Virtual Environment
# 1. Create virtual environment:
#    python -m venv venv
# 2. Activate environment:
#    source venv/bin/activate (Linux/Mac)
#    venv\Scripts\activate (Windows)

## Steps 2: ##
create folder
a) src
b) tests
c) requirements.txt
# 3. Install requirements:
#    pip install -r requirements.txt
# 4. For development:
#    pip install -r requirements-dev.txt



Define the Pipeline:
Create a configuration file (e.g.,
.github/workflows/main.yml for GitHub
.gitlab-ci.yml for GitLab
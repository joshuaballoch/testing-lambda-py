# A sample serverless function to test testing lambda functions

[![Build Status](https://travis-ci.org/joshuaballoch/testing-lambda-py.svg?branch=master)](https://travis-ci.org/joshuaballoch/testing-lambda-py)

## Installation

1. Create & Source the virtualenv

```
virtualenv .venv -p python3
source .venv/bin/activate
```

2.  Install pip tools

```
pip3 install pip-tools
```

3. Install the development requirements

```
pip-compile --output-file requirements-dev.txt requirements/requirements-dev.in

pip install -r requirements-dev.txt
```

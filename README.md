# Headless Chrome AWS Lambda Layer (for Python)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![Latest build](https://github.com/diegoparrilla/headless-chrome-aws-lambda-layer/actions/workflows/build.yml/badge.svg)
![Latest release](https://github.com/diegoparrilla/headless-chrome-aws-lambda-layer/actions/workflows/publish.yml/badge.svg?)

## TL;DR
Headless Chrome with Selenium prepared to run as a layer in AWS lambda with Python >=3.8 and Amazon Linux 2

## Introduction

This layer contains all a developer needs to run Selenium with Python in a AWS Lambda serverless function with Python 3.8. The new Python 3.8 runtime uses Amazon Linux 2, which is a stripped
 version of the operating system with the minimal amount of libraries to run Python 3.8 as a lambda. Hence, the runtime lacks of some of the libraries and tools to run a headless version of Chromium and the Chrome driver.

This layer includes all the elements needed plus the Selenium library and a pre-configured version of the Chrome Webdriver of Selenium ready to use out of the box. It's also possible to use your own Selenium library and Chrome driver, but needs some prequirements and configuration first.

This layer is designed to be part of a Python 3.8 runtime in AWS Lambda, but probaly it's feasible for other languages and runtimes. Feel free to make any changes and submit them as a PR!

## How to use the image

The developr has to add the `.zip` file found in the [`releases`](https://github.com/diegoparrilla/headless-chrome-aws-lambda-layer/releases) section of this repo as a layer of the AWS Lambda function, or build the layer from scratch first. For example:

```
aws s3 cp layer-headless_chrome-v0.1-alpha.3.zip s3://<YOUR_BUCKET_NAME>/layer-headless_chrome.zip
aws lambda publish-layer-version \
    --layer-name HeadlessChromium \
    --region <YOUR_AWS_REGION> \
    --content S3Bucket=<YOUR_BUCKET_NAME>,S3Key=layer-headless_chrome.zip \
    --compatible-runtimes python3.8
```

Now create a new AWS Lambda function and add the layer uploaded. Now the code in the lambda handler can use the libraries found in the layer as follows:
```
from headless_chrome import driver

def lambda_handler(_event, _context):
    """ Sample handle about how to use the imported the layer """

    driver.get("https://www.google.com")
    return driver.page_source
```

## How to create the image

To create the image, use the following targets of the `Makefile`:

### Build the layer

```
make build
```

The layer is under the newly created folder `layer` as a zip file.

### Run integration tests

```
make test-integration
```

The process will create a new layer and will run the tests found in `tests/lambda_test.py`. 

### Run code pre-commit rules

```
make precommit
```

Check the code with the rules predefined.  

### Clean folders

```
make clean
```

Delete all temporary files and folders used during the build and test time.  

### Run all targets

```
make all
```

Run all targets in the correct order to obtain a fully tested layer ready to be released.  


## What's next?

This layer offers a boilerplate library to use in AWS Lambda, but it's possible to use your own Selenium Webdriver configuration in your code in the lambda handler or another layer. Please review the code in `src/headless_chrome.py` to get a better understanding of the environment created to run Selenium serverless. For example:

- `chromedriver` and `headless-chromium` executables are located under `/opt`.
- `--headless` and `--no-sandbox`are a must. Read all the parameters needed in the code.
- `headless-chromium` needs the environment variable `FONTCONFIG_PATH` to work. Don't forget it!.
- etc.

## Contributing

This project is open to collaboration. It was created to run Selenium easily in AWS Lambda with Python 3.8. But hey, I'm open to collaboration and suggestions.


## Contact

Do you have an issue? Or perhaps some feedback for how we can improve? Feel free to let us know on
our [issue tracker](https://github.com/diegoparrilla/headless-chrome-aws-lambda-layer).

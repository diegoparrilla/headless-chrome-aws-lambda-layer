# Headless Chrome AWS Lambda Layer (for Python)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## TL;DR
Headless Chrome with Selenium prepared to run as a layer in AWS lambda with Python >=3.8 and Amazon Linux 2

## Introduction

This layer contains all a developer needs to run Selenium with Python in a AWS Lambda serverless function with Python 3.8. The new Python 3.8 runtime uses Amazon Linux 2, which is a stripped
 version of the operating system with the minimal amount of libraries to run Python 3.8 as a lambda. Hence, the runtime lacks of some of the libraries and tools to run a headless version of Chromium and the Chrome driver.

This layer includes all the elements needed plus the Selenium library and a pre-configured version of the Chrome Webdriver of Selenium ready to use out of the box. It's also possible to use your own Selenium library and Chrome driver, but needs some prequirements and configuration first.

This layer is designed to be part of a Python 3.8 runtime in AWS Lambda, but probaly it's feasible for other languages and runtimes. Feel free to make any changes and submit them as a PR!

## How to use the image

TBD

## How to create the image

TBD

## What's next?

TBD

## Contributing

This project is open to collaboration. It was created to run Selenium easily in AWS Lambda with Python 3.8. But hey, I'm open to collaboration and suggestions.


## Contact

Do you have an issue? Or perhaps some feedback for how we can improve? Feel free to let us know on
our [issue tracker](https://github.com/diegoparrilla/headless-chrome-aws-lambda-layer).

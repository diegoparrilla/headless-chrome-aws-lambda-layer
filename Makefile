SHELL:=/bin/bash

## ENV NAMES
LAYER_VERSION=dev
PYTHON_VERSION = 3.8
SRC_DIR := $(shell pwd)/src
TESTS_DIR := $(shell pwd)/tests
PACKAGES_DIR := $(shell pwd)/layer
LAYER_NAME := headless_chrome

RUNTIME=python$(PYTHON_VERSION)
SELENIUM_VER=3.141.0
CHROME_BINARY_VER=v1.0.0-57
CHROMEDRIVER_VER=86.0.4240.22
SWIFTSHADER_VER=v7.0-beta.0
DRIVER_URL=https://chromedriver.storage.googleapis.com/$(CHROMEDRIVER_VER)/chromedriver_linux64.zip
CHROME_URL=https://github.com/adieuadieu/serverless-chrome/releases/download/$(CHROME_BINARY_VER)/stable-headless-chromium-amazonlinux-2.zip
SWIFTSHADER_URL=https://github.com/diegoparrilla/amazonlinux2-swiftshader-builder/releases/download/$(SWIFTSHADER_VER)/swiftshader-$(SWIFTSHADER_VER).zip

LOCAL_LAYER_DIR=$(PWD)/build/$(LAYER_NAME)
LOCAL_LAYER_REL_DIR=build/$(LAYER_NAME)
OUT_DIR=/out/build/$(LAYER_NAME)/python/lib/$(RUNTIME)/site-packages

TEST_DOCKER_IMAGE_BASE_NAME = test-lambda
TEST_VERSION = 0.0.1
TEST_DEFAULT_FUNCTION = lambda_test.lambda_handler

define generate_runtime
	# Install libraries needed by chromedriver and headless chrome
	docker run --rm -v $(LOCAL_LAYER_DIR)/:/lambda/opt lambci/yumda:2 yum install -y glib2 libX11 nss && \
		docker run --rm -v $(LOCAL_LAYER_DIR)/:/lambda/opt lambci/yumda:2 yum install -y expat fontconfig

	# download chrome driver binary
	curl -SL $(DRIVER_URL) >chromedriver.zip && \
		unzip chromedriver.zip -d $(LOCAL_LAYER_REL_DIR) && rm chromedriver.zip

	# download headless chrome binary
	curl -SL $(CHROME_URL) >headless-chromium.zip && \
		unzip headless-chromium.zip -d $(LOCAL_LAYER_REL_DIR) && rm headless-chromium.zip

	# download swiftshader libraries
	curl -SL $(SWIFTSHADER_URL) >swiftshader.zip && \
		unzip swiftshader.zip -d $(LOCAL_LAYER_REL_DIR) && rm swiftshader.zip

endef

define zip_layer
	pushd $(LOCAL_LAYER_REL_DIR) && zip -r ../../layer/layer-$(LAYER_NAME)-$(LAYER_VERSION).zip * && popd
endef

define unzip_layer
	mkdir -p $(PACKAGES_DIR)/layer-$(LAYER_NAME) && \
		pushd $(PACKAGES_DIR) && unzip layer-$(LAYER_NAME)-$(LAYER_VERSION).zip -d layer-$(LAYER_NAME) && popd
endef

# List all targets
.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

## Run all pre-commit hooks
.PHONY: precommit
precommit:
	pre-commit run --all

## Lint your code using pylint
.PHONY: lint
lint:
	python -m pylint --version
	python -m pylint $(SRC_DIR) $(TESTS_DIR)

## Format your code using black
.PHONY: black
black:
	python -m black --version
	python -m black $(SRC_DIR) $(TESTS_DIR)

## Run unit tests using pytest
.PHONY: test-unit
test-unit:
	python -m unittest -v tests.selenium_lib

## Run ci part
.PHONY: ci
	ci: precommit lint test

## Build layer with $(LAYER_NAME) library and selenium
.PHONY:	build
build: clean
	# Create build environment
	mkdir -p $(LOCAL_LAYER_REL_DIR) && mkdir -p $(LOCAL_LAYER_REL_DIR)/python && mkdir -p layer
	# Add the selenium and default wrapper library
	docker run -v $(PWD):/out lambci/lambda:build-$(RUNTIME) \
		pip install selenium==$(SELENIUM_VER) -t $(OUT_DIR) && \
		cp src/$(LAYER_NAME).py $(LOCAL_LAYER_REL_DIR)/python/$(LAYER_NAME).py

	$(call generate_runtime)
	$(call zip_layer)

## Build layer with $(LAYER_NAME) with only the runtimes for chromedriver and headless chrome
.PHONY .ONESHELL:	build-runtime-only
build-runtime-only: clean
	# Create build environment
	mkdir -p $(LOCAL_LAYER_REL_DIR) && mkdir -p $(LOCAL_LAYER_REL_DIR)/python && mkdir -p layer

	$(call generate_runtime)
	$(call zip_layer)

## Clean build folders
.PHONY:	clean
clean:
	# Clean build environment
	rm -rf build layer

## Expand compressed layer file
.PHONY:	.expand-layer
.expand-layer:
	$(call unzip_layer)

## Run test integration suite. It runs like a lambda... bizarre isn't it?
.PHONY:	test-integration
test-integration: .expand-layer
	$(eval res := $(shell docker run --rm -v $(TESTS_DIR):/var/task -v $(PACKAGES_DIR)/layer-$(LAYER_NAME):/opt lambci/lambda:$(RUNTIME) $(TEST_DEFAULT_FUNCTION)))
	exit $(res)

## Create and test the new layer version
.PHONY:	all
all: precommit lint build test-integration
	# Deploy the release version
	echo "PUBLISHED!"

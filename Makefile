## ENV NAMES
LAYER_VERSION = 0.1-alpha.1
PYTHON_VERSION = 3.8
SRC_DIR := $(shell pwd)/src
TESTS_DIR := $(shell pwd)/tests
LAYER_NAME := headless_chrome

RUNTIME=python$(PYTHON_VERSION)
SELENIUM_VER=3.141.0
CHROME_BINARY_VER=v1.0.0-57
CHROMEDRIVER_VER=86.0.4240.22
SWIFTSHADER_VER=v7.0-alpha.0
DRIVER_URL=https://chromedriver.storage.googleapis.com/$(CHROMEDRIVER_VER)/chromedriver_linux64.zip
CHROME_URL=https://github.com/adieuadieu/serverless-chrome/releases/download/$(CHROME_BINARY_VER)/stable-headless-chromium-amazonlinux-2.zip
SWIFTSHADER_URL=https://github.com/diegoparrilla/amazonlinux2-swiftshader-builder/releases/download/$(SWIFTSHADER_VER)/swiftshader.zip

LOCAL_LAYER_DIR=$(PWD)/build/$(LAYER_NAME)
OUT_DIR=/out/build/$(LAYER_NAME)/python/lib/$(RUNTIME)/site-packages

TEST_DOCKER_IMAGE_BASE_NAME = test-lambda
TEST_VERSION = 0.0.1
TEST_DEFAULT_FUNCTION = lambda_tests.lambda_handler

#REGION=eu-west-1
#BUCKET=prod-eu-denyset-eu-west-1

define generate_runtime
	# Install libraries needed by chromedriver and headless chrome
	docker run --rm -v $(LOCAL_LAYER_DIR)/:/lambda/opt lambci/yumda:2 yum install -y glib2 libX11 nss && \
		docker run --rm -v $(LOCAL_LAYER_DIR)/:/lambda/opt lambci/yumda:2 yum install -y expat fontconfig

	# download chrome driver binary
	curl -SL $(DRIVER_URL) >$(LOCAL_LAYER_DIR)/chromedriver.zip && \
		unzip $(LOCAL_LAYER_DIR)/chromedriver.zip -d $(LOCAL_LAYER_DIR) && rm $(LOCAL_LAYER_DIR)/chromedriver.zip
	# download headless chrome binary
	curl -SL $(CHROME_URL) >$(LOCAL_LAYER_DIR)/headless-chromium.zip && \
		unzip $(LOCAL_LAYER_DIR)/headless-chromium.zip -d $(LOCAL_LAYER_DIR) && rm $(LOCAL_LAYER_DIR)/headless-chromium.zip
	# download swiftshader libraries
	curl -SL $(SWIFTSHADER_URL) >$(LOCAL_LAYER_DIR)/swiftshader.zip && \
		unzip $(LOCAL_LAYER_DIR)/swiftshader.zip -d $(LOCAL_LAYER_DIR) && rm $(LOCAL_LAYER_DIR)/swiftshader.zip 
endef

define zip_layer
	pushd $(LOCAL_LAYER_DIR) && zip -r ../../layer/layer-$(LAYER_NAME)-$(LAYER_VERSION).zip * && popd 
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
.PHONY .ONESHELL:	build
build: clean 
	# Create build environment
	mkdir -p build &&  mkdir -p layer
	# Add the selenium and default wrapper library
	docker run -v $(PWD):/out -it lambci/lambda:build-$(RUNTIME) \
			pip install selenium==$(SELENIUM_VER) -t $(OUT_DIR) && \
		cp src/$(LAYER_NAME).py $(LOCAL_LAYER_DIR)/python/$(LAYER_NAME).py
	$(call generate_runtime)
	$(call zip_layer)

## Build layer with $(LAYER_NAME) with only the runtimes for chromedriver and headless chrome
.PHONY .ONESHELL:	build-runtime-only
build-runtime-only: clean
	# Create build environment
	mkdir -p build &&  mkdir -p layer
	$(call generate_runtime)
	$(call zip_layer)

## Clean build folders
.PHONY:	clean
clean:
	# Clean build environment
	rm -rf build layer

## Run test integration suite. It runs like a lambda... bizarre isn't it?
.PHONY:	test-integration
PACKAGES_DIR = layer
test-integration: 
	mkdir -p $(PACKAGES_DIR)/layer-$(LAYER_NAME) && rm -rf $(PACKAGES_DIR)/layer-$(LAYER_NAME) && \
		pushd $(PACKAGES_DIR) && unzip layer-$(LAYER_NAME)-$(LAYER_VERSION).zip -d layer-$(LAYER_NAME) && popd
	docker run --rm -v $(TESTS_DIR):/var/task -v $(PWD)/$(PACKAGES_DIR)/layer-$(LAYER_NAME):/opt lambci/lambda:$(RUNTIME) $(TEST_DEFAULT_FUNCTION)

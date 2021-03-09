"""
Copyright 2021 Diego Parrilla

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import uuid
import logging

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)

FONTCONFIG_LINUX_PATH: str = "/opt/etc/fonts"
DOWNLOAD_LOCATION: str = "/tmp/"
TMP_FOLDER: str = "/tmp/{}".format(uuid.uuid4())
USER_AGENT: str = "Mozilla/5.0 (X11; Linux x86_64) \
 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
CHROMEDRIVER_EXEC_PATH: str = "/opt/chromedriver"
HEADLESS_CHROMIUM_EXEC_PATH: str = "/opt/headless-chromium"
HEADLESS_CHROMIUM_LOG_LEVEL: int = 0
HEADLESS_CHROMIUM_VERBOSITY_LEVEL: int = 0
HEADLESS_CHROMIUM_WINDOW_SIZE: str = "1280x1696"
HEADLESS_CHROMIUM_PARAMS: list = [
    "--headless",
    "--no-sandbox",
    "--single-process",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--hide-scrollbars",
    "--enable-logging",
    "--ignore-certificate-errors",
    "--log-level={}".format(HEADLESS_CHROMIUM_LOG_LEVEL),
    "--v={}".format(HEADLESS_CHROMIUM_VERBOSITY_LEVEL),
    "--window-size={}".format(HEADLESS_CHROMIUM_WINDOW_SIZE),
    "--user-data-dir={}".format(TMP_FOLDER + "/user-data"),
    "--data-path={}".format(TMP_FOLDER + "/data-path"),
    "--homedir={}".format(TMP_FOLDER),
    "--disk-cache-dir={}".format(TMP_FOLDER + "/cache-dir"),
    "--user-agent={}".format(USER_AGENT),
]


def create_folders(tmp_folder: str = None):
    """ Created the chrome data structure under tmp_folder """
    if not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)
        logging.info("Created folder: %s", tmp_folder)

    tmp_user_data = tmp_folder + "/user-data"
    if not os.path.exists(tmp_user_data):
        os.makedirs(tmp_user_data)
        logging.info("Created folder: %s", tmp_user_data)

    tmp_data_path = tmp_folder + "/data-path"
    if not os.path.exists(tmp_data_path):
        os.makedirs(tmp_data_path)
        logging.info("Created folder: %s", tmp_data_path)

    tmp_cache_dir = tmp_folder + "/cache-dir"
    if not os.path.exists(tmp_cache_dir):
        os.makedirs(tmp_cache_dir)
        logging.info("Created folder: %s", tmp_cache_dir)


def configure_download_location(download_location: str = None) -> dict:
    """ Configure the download folders, if they exists """
    prefs = {}
    if download_location:
        prefs = {
            "download.default_directory": download_location,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True,
            "profile.default_content_setting_values.automatic_downloads": 1,
        }
        logging.info("Configured download folder: %s", download_location)
    else:
        logging.info("Download folder not configured")

    return prefs


# Need to configure the FONTCONFIG_PATH to work
os.environ["FONTCONFIG_PATH"] = FONTCONFIG_LINUX_PATH
logging.info("FONTCONFIG_PATH configured: %s", FONTCONFIG_LINUX_PATH)
options: Options = Options()

create_folders(tmp_folder=TMP_FOLDER)

options.binary_location = HEADLESS_CHROMIUM_EXEC_PATH
logging.info("Headless Chromium binary location path: %s", HEADLESS_CHROMIUM_EXEC_PATH)

for param in HEADLESS_CHROMIUM_PARAMS:
    options.add_argument(param)
    logging.info("Argument passed to headless chromium: %s", param)

experimental_prefs: dict = configure_download_location(
    download_location=DOWNLOAD_LOCATION
)
options.add_experimental_option("prefs", experimental_prefs)

driver = Chrome(CHROMEDRIVER_EXEC_PATH, options=options)
logging.info("Driver chromedriver initialized in: %s", CHROMEDRIVER_EXEC_PATH)

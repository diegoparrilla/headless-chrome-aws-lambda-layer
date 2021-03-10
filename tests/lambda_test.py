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
# pylint: disable=C0415
import os
import subprocess
import unittest

CHROMEDRIVER_PATH = "/opt/chromedriver"
CHROMEDRIVER_VERSION = (
    "86.0.4240.22"  # This version must be aligned with the version built!
)
HEADLESS_CHROMIUM_PATH = "/opt/headless-chromium"
SWIFTSHADER_FOLDER_PATH = "/opt/swiftshader"
SWIFTSHADER_LIBEGL_PATH = "/opt/swiftshader/libEGL.so"
SWIFTSHADER_LIBGLESV2_PATH = "/opt/swiftshader/libGLESv2.so"
FONT_CONFIG_PATH = "/opt/etc/fonts/fonts.conf"
FONT_LIB_PATH = "/opt/lib/libfontconfig.so.1"
X11_LIB_PATH = "/opt/lib/libX11.so.6"
GLIB2_LIB_PATH = "/opt/lib/libglib-2.0.so.0"
NSS3_LIB_PATH = "/opt/lib/libnss3.so"
EXPAT_LIB_PATH = "/opt/lib/libexpat.so.1"


class WebDriverSystemTestCase(unittest.TestCase):
    """ Webdriver system layer configuration tests """

    def test_find_chromedriver_executable(self):
        """ Test if the chromedriver executable is in the right path """
        found = os.path.exists(CHROMEDRIVER_PATH) and os.path.isfile(CHROMEDRIVER_PATH)
        self.assertTrue(found)

    def test_find_headless_chromium_executable(self):
        """ Test if the headless chromium executable is in the right path """
        found = os.path.exists(HEADLESS_CHROMIUM_PATH) and os.path.isfile(
            HEADLESS_CHROMIUM_PATH,
        )
        self.assertTrue(found)

    def test_find_swiftshader_libs(self):
        """ Test if the swiftshared libs are in the right path """
        found = os.path.exists(SWIFTSHADER_FOLDER_PATH) and os.path.isdir(
            SWIFTSHADER_FOLDER_PATH,
        )
        self.assertTrue(found)
        found = os.path.exists(SWIFTSHADER_LIBEGL_PATH) and os.path.isfile(
            SWIFTSHADER_LIBEGL_PATH,
        )
        self.assertTrue(found)
        found = os.path.exists(SWIFTSHADER_LIBGLESV2_PATH) and os.path.isfile(
            SWIFTSHADER_LIBGLESV2_PATH,
        )
        self.assertTrue(found)

    def test_find_default_fonts_config(self):
        """ Test if the default configuration fonts file is in the right path """
        found = os.path.exists(FONT_CONFIG_PATH) and os.path.isfile(FONT_CONFIG_PATH)
        self.assertTrue(found)

    def test_find_default_fonts_lib(self):
        """ Test if the default configuration fonts lib is in the right path """
        found = os.path.exists(FONT_LIB_PATH) and os.path.isfile(FONT_LIB_PATH)
        self.assertTrue(found)

    def test_find_x11_lib(self):
        """ Test if the X11 lib is in the right path """
        found = os.path.exists(X11_LIB_PATH) and os.path.isfile(X11_LIB_PATH)
        self.assertTrue(found)

    def test_find_glib2_lib(self):
        """ Test if the glib2 lib is in the right path """
        found = os.path.exists(GLIB2_LIB_PATH) and os.path.isfile(GLIB2_LIB_PATH)
        self.assertTrue(found)

    def test_find_nss3_lib(self):
        """ Test if the nss3 lib is in the right path """
        found = os.path.exists(NSS3_LIB_PATH) and os.path.isfile(NSS3_LIB_PATH)
        self.assertTrue(found)

    def test_find_expat_lib(self):
        """ Test if the nss3 lib is in the right path """
        found = os.path.exists(EXPAT_LIB_PATH) and os.path.isfile(EXPAT_LIB_PATH)
        self.assertTrue(found)


class ChromiumSystemTestCase(unittest.TestCase):
    """ Chromium executable system tests """

    HEADLESS_PARAM = "--headless"
    NOSANDBOX_PARAM = "--no-sandbox"
    DISABLEGPU_PARAM = "--disable-gpu"
    DUMPSCREENSHOT_PARAM = "--screenshot=/tmp/out-%s.png"
    DUMPDOM_PARAM = "--dump-dom"

    def setUp(self):
        os.environ["FONTCONFIG_PATH"] = "/opt/etc/fonts"

    def tearDown(self):
        del os.environ["FONTCONFIG_PATH"]

    def test_version_stdout(self):
        """ Test if the chromium executable returns a valid version """
        out = subprocess.run(
            [
                HEADLESS_CHROMIUM_PATH,
                "--version",
                self.HEADLESS_PARAM,
                self.NOSANDBOX_PARAM,
                self.DISABLEGPU_PARAM,
            ],
            capture_output=True,
            check=True,
        )
        self.assertTrue(out)

    #    def test_screenshot_filesystem(self):
    #        """ Test if the chromium executable can dump a screenshot of a website """
    #        screenshot_param = self.DUMPSCREENSHOT_PARAM % uuid.uuid4()
    #        out = subprocess.run(
    #            [
    #                HEADLESS_CHROMIUM_PATH,
    #                self.HEADLESS_PARAM,
    #                self.NOSANDBOX_PARAM,
    #                self.DISABLEGPU_PARAM,
    #                screenshot_param,
    #                "https://www.google.com",
    #            ],
    #            capture_output=True,check=True
    #        )
    #        filename = screenshot_param.split("=")[1]
    #        found = os.path.exists(filename) and os.path.isfile(filename)
    #        self.assertTrue(found)
    #        os.remove(filename)
    #        found = os.path.exists(filename) and os.path.isfile(filename)
    #        self.assertFalse(found)

    def test_dumpdom_filesystem(self):
        """ Test if the chromium executable can dump a dom of a website """
        out = subprocess.run(
            [
                HEADLESS_CHROMIUM_PATH,
                self.HEADLESS_PARAM,
                self.NOSANDBOX_PARAM,
                self.DISABLEGPU_PARAM,
                self.DUMPDOM_PARAM,
                "https://www.google.com",
            ],
            capture_output=True,
            check=True,
        )
        stdout = out.stdout
        self.assertGreater(stdout.count(b"www.google.com"), 0)


class ChromedriverSystemTestCase(unittest.TestCase):
    """ Chromedriver executable system tests """

    def setUp(self):
        os.environ["FONTCONFIG_PATH"] = "/opt/etc/fonts"

    def tearDown(self):
        del os.environ["FONTCONFIG_PATH"]

    def test_version_stdout(self):
        """ Test if the chromedriver executable returns a valid version """
        out = subprocess.run(
            [CHROMEDRIVER_PATH, "--version"],
            capture_output=True,
            check=True,
        )
        stdout = out.stdout.decode()
        version = stdout.split(" ")
        self.assertGreater(len(version), 1)
        name = version[0].upper()
        self.assertEqual(name, "CHROMEDRIVER")
        version_code = version[1]
        self.assertEqual(version_code, CHROMEDRIVER_VERSION)


class SeleniumTestCase(unittest.TestCase):
    """ Selenium packaged tests """

    @classmethod
    def setUpClass(cls):
        os.environ["FONTCONFIG_PATH"] = "/opt/etc/fonts"
        from headless_chrome import driver
        from selenium.webdriver.support.ui import WebDriverWait

        cls._driver = driver
        cls._web_driver_wait = WebDriverWait

    @classmethod
    def tearDownClass(cls):
        del os.environ["FONTCONFIG_PATH"]

    def test_get_full_page(self):
        """ Test if Selenium can read a single page """
        self._driver.get("https://www.google.com")
        out = self._driver.page_source
        self.assertGreater(out.count("https://www.google.com/"), 0)

    def test_get_xpath(self):
        """ Test if Selenium can read an XPATH from a page """
        # If the documentation site changes this test will fail...
        self._driver.get(
            "https://developers.google.com/web/updates/2017/04/headless-chrome",
        )
        elem = self._driver.find_element_by_xpath(
            '//*[@id="gc-wrapper"]/main/devsite-content/article/h1',
        )
        inner_html = elem.get_attribute("innerHTML")
        self.assertGreater(inner_html.count("Headless Chrome"), 0)

    def test_wait_for_webdriver(self):
        """ Test if Selenium can read wait for an element in a page to render """
        self._driver.get("https://www.msn.com")
        elem_clients = self._web_driver_wait(self._driver, timeout=20).until(
            lambda d: d.find_element_by_xpath('//*[@id="foot"]/footer/a'),
        )
        inner_html = elem_clients.get_attribute("innerHTML")
        self.assertGreater(inner_html.count("Microsoft"), 0)


def lambda_handler(_event, _context):
    """ Default lambda handler to trigger the integration tests. It's bizarre, I know. """

    test = unittest.main(module="lambda_test", exit=False, verbosity=3)
    print(test.result)

    return int(len(test.result.errors) or len(test.result.failures))


#    return {
#        "run": test.result.testsRun,
#        "errors": len(test.result.errors),
#        "failures": len(test.result.failures),
#    }

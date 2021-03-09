from chrome_headless import driver


def lambda_handler(event, context):

    driver.get("https://www.google.com")
    return driver.page_source
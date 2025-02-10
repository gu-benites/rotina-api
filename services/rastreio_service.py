from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
from bs4 import BeautifulSoup
import asyncio
from config import CHROME_DRIVER_PATH

# Asynchronous function to retrieve tracking information using Selenium WebDriver and BeautifulSoup
async def rastreio(pedido):
    print("Setting up Chrome driver...")
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver_service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=driver_service, options=options)

    try:
        tracking_url = f"https://status.ondeestameupedido.com/tracking/22747/{pedido}/"
        driver.get(tracking_url)
        await asyncio.sleep(2)  # Adjust sleep time as necessary
        soup = BeautifulSoup(driver.page_source, "html.parser")
        texts = [text for text in soup.stripped_strings]
        return texts
    finally:
        driver.quit()  # Make sure to quit the driver to free resources

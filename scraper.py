import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
import requests
from config import *

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class XScraper:
    def __init__(self, use_proxy=False):
        self.use_proxy = use_proxy
        self.proxy = self._get_proxy() if use_proxy else None
        self.driver = self._setup_driver()

    def _get_proxy(self):
        try:
            proxy_auth = f"{PROXYMESH_USERNAME}:{PROXYMESH_PASSWORD}"
            return f"http://{proxy_auth}@{PROXYMESH_HOST}:{PROXYMESH_PORT}"
        except Exception as e:
            logger.error(f"Failed to set up proxy: {str(e)}")
            return None

    def _setup_driver(self):
        try:
            options = webdriver.ChromeOptions()

            if self.proxy:
                options.add_argument(f'--proxy-server={self.proxy}')

            # Anti-detection options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # Update navigator.webdriver flag to undefined
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            return driver

        except Exception as e:
            logger.error(f"Failed to initialize driver: {str(e)}")
            raise

    def login_to_x(self):
        try:
            logger.info("Navigating to X login page...")
            self.driver.get("https://x.com/login")
            
            # Wait for and fill in username
            logger.info("Waiting for username field...")
            username_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_input.clear()
            username_input.send_keys(X_USERNAME)
            
            # Click the Next button instead of submitting the input
            next_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            next_button.click()

            # Wait for and fill in password
            logger.info("Waiting for password field...")
            password_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(X_PASSWORD)
            
            # Click the Log in button instead of submitting the input
            login_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
            )
            login_button.click()

            # Wait for login to complete
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='primaryColumn']"))
            )

            logger.info("Login successful")

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise

    def get_trending_topics(self):
        try:
            self.driver.get("https://x.com/explore")
            
            logger.info("Waiting for trends section...")
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='trend']"))
            )
            
            trends = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='trend']")
            trending_topics = []

            for trend in trends[:5]:
                try:
                    trend_text = trend.find_element(By.CSS_SELECTOR, "span").text
                    if trend_text and not trend_text.isspace():
                        trending_topics.append(trend_text.strip())
                except Exception as e:
                    logger.warning(f"Failed to extract trend text: {str(e)}")
                    continue

            if not trending_topics:
                raise ValueError("No trending topics found")

            logger.info(f"Found {len(trending_topics)} trending topics")
            return trending_topics

        except Exception as e:
            logger.error(f"Failed to get trending topics: {str(e)}")
            raise

    def get_current_ip(self):
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=10)
            return response.json()['ip']
        except Exception as e:
            logger.error(f"Failed to get IP address: {str(e)}")
            return "Unknown"

    def cleanup(self):
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                logger.info("Browser cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

if __name__ == "__main__":
    scraper = None
    try:
        scraper = XScraper(use_proxy=False)
        logger.info("Scraper initialized successfully")
        
        scraper.login_to_x()
        trends = scraper.get_trending_topics()
        logger.info(f"Trending Topics: {trends}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        if scraper:
            scraper.cleanup()
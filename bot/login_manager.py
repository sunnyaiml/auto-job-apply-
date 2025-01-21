from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import logging
from pathlib import Path
import time
from selenium.webdriver.common.keys import Keys

class LoginManager:
    def __init__(self, driver=None):
        self.driver = driver or self._setup_driver()
        self._setup_logging()

    def _setup_driver(self):
        """Initialize and return a Chrome WebDriver instance"""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        return webdriver.Chrome(options=options)

    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename='logs/login.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def login_linkedin(self, credentials_file):
        """
        Login to LinkedIn using credentials from the specified file
        
        Args:
            credentials_file (str): Path to JSON file containing LinkedIn credentials
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # Load credentials
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
            
            # Navigate to LinkedIn login page
            self.driver.get('https://www.linkedin.com/login')
            
            # Wait for and find username field
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(credentials['linkedin']['username'])
            
            # Find and fill password field
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(credentials['linkedin']['password'])
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for successful login (check for feed page or dashboard)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "global-nav"))
            )
            
            self.logger.info("Successfully logged into LinkedIn")
            return True
            
        except TimeoutException:
            self.logger.error("Timeout while trying to log into LinkedIn")
            return False
        except Exception as e:
            self.logger.error(f"Error during LinkedIn login: {str(e)}")
            return False

    def login_indeed(self, credentials_file):
        """
        Login to Indeed using credentials from file
        
        Args:
            credentials_file (str): Path to credentials JSON file
            
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # Load credentials
            with open(credentials_file, 'r') as f:
                creds = json.load(f)
            
            # Navigate to Indeed login page
            self.driver.get('https://secure.indeed.com/auth')
            time.sleep(2)
            
            # Enter email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ifl-InputFormField-3"))
            )
            email_input.send_keys(creds['indeed_email'])
            
            # Click continue button
            continue_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            continue_button.click()
            time.sleep(2)
            
            # Enter password
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ifl-InputFormField-7"))
            )
            password_input.send_keys(creds['indeed_password'])
            
            # Click sign in button
            signin_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            signin_button.click()
            
            # Wait for login to complete
            time.sleep(5)
            
            self.logger.info("Successfully logged in to Indeed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error logging in to Indeed: {str(e)}")
            return False

    def login_indeed_with_google(self, credentials_file):
        """
        Login to Indeed using Google authentication
        
        Args:
            credentials_file (str): Path to JSON file containing Indeed credentials
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # Load credentials
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
            
            # Navigate to Indeed
            self.driver.get('https://secure.indeed.com/auth')
            time.sleep(2)
            
            # Click on Google Sign In button
            google_signin = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-tn-element='google-login-button']"))
            )
            google_signin.click()
            
            # Wait for Google login page and switch to it
            time.sleep(2)
            google_window = self.driver.window_handles[-1]
            self.driver.switch_to.window(google_window)
            
            # Enter Google email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            email_field.send_keys(credentials['indeed']['email'])
            email_field.send_keys(Keys.RETURN)
            
            # Wait for successful login and return to Indeed
            time.sleep(5)
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            self.logger.info("Successfully logged into Indeed with Google")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during Indeed Google login: {str(e)}")
            return False

    def login_internshala(self, credentials_file):
        """
        Login to Internshala using credentials
        
        Args:
            credentials_file (str): Path to JSON file containing Internshala credentials
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # Load credentials
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
            
            # Navigate to Internshala login page
            self.driver.get('https://internshala.com/login')
            time.sleep(2)
            
            # Enter credentials
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(credentials['internshala']['username'])
            
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(credentials['internshala']['password'])
            
            # Click login button
            login_button = self.driver.find_element(By.ID, "login_submit")
            login_button.click()
            
            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "profile_container"))
            )
            
            self.logger.info("Successfully logged into Internshala")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during Internshala login: {str(e)}")
            return False

    def login_naukri(self, credentials_file):
        """
        Login to Naukri using credentials
        
        Args:
            credentials_file (str): Path to JSON file containing Naukri credentials
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            # Load credentials
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
            
            # Navigate to Naukri login page
            self.driver.get('https://www.naukri.com/nlogin/login')
            time.sleep(2)
            
            # Enter credentials
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "usernameField"))
            )
            email_field.send_keys(credentials['naukri']['username'])
            
            password_field = self.driver.find_element(By.ID, "passwordField")
            password_field.send_keys(credentials['naukri']['password'])
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "nI-gNb-drawer__bars"))
            )
            
            self.logger.info("Successfully logged into Naukri")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during Naukri login: {str(e)}")
            return False

    def close(self):
        """Close the browser and clean up"""
        if self.driver:
            self.driver.quit()

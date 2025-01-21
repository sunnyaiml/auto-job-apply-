from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging
import time
import json
from pathlib import Path

class JobScraper:
    def __init__(self, driver):
        self.driver = driver
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename='logs/scraper.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def search_linkedin_jobs(self, keywords, location):
        """
        Search for jobs on LinkedIn based on keywords and location
        
        Args:
            keywords (str): Job search keywords
            location (str): Job location
            
        Returns:
            list: List of job dictionaries containing details
        """
        try:
            # Navigate to LinkedIn Jobs
            self.driver.get('https://www.linkedin.com/jobs/')
            
            # Wait for and fill keywords field
            keywords_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-box__text-input"))
            )
            keywords_field.clear()
            keywords_field.send_keys(keywords)
            
            # Fill location field
            location_field = self.driver.find_elements(By.CLASS_NAME, "jobs-search-box__text-input")[1]
            location_field.clear()
            location_field.send_keys(location)
            
            # Click search button
            search_button = self.driver.find_element(By.CLASS_NAME, "jobs-search-box__submit-button")
            search_button.click()
            
            # Wait for job results to load
            time.sleep(3)
            
            jobs = []
            # Scroll through job listings to load more
            for _ in range(5):  # Adjust range based on how many jobs you want to scrape
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Get all job cards
                job_cards = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
                
                for card in job_cards:
                    try:
                        job_info = {
                            'title': card.find_element(By.CLASS_NAME, "job-card-list__title").text,
                            'company': card.find_element(By.CLASS_NAME, "job-card-container__company-name").text,
                            'location': card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text,
                            'link': card.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute('href')
                        }
                        if job_info not in jobs:  # Avoid duplicates
                            jobs.append(job_info)
                    except NoSuchElementException:
                        continue
            
            self.logger.info(f"Found {len(jobs)} jobs on LinkedIn")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error during LinkedIn job search: {str(e)}")
            return []

    def search_indeed_jobs(self, keywords, location):
        """
        Search for jobs on Indeed
        
        Args:
            keywords (str): Job search keywords
            location (str): Job location
            
        Returns:
            list: List of job dictionaries with title, company, url
        """
        try:
            # Format search URL
            search_query = f"{keywords}".replace(' ', '+')
            search_location = f"{location}".replace(' ', '+')
            search_url = f"https://www.indeed.com/jobs?q={search_query}&l={search_location}&sc=0kf%3Aattr(DSQF7)%3B"
            
            # Navigate to search results
            self.driver.get(search_url)
            time.sleep(2)
            
            jobs = []
            pages_scraped = 0
            max_pages = 3  # Limit number of pages to scrape
            
            while pages_scraped < max_pages:
                # Find all job cards
                job_cards = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon"))
                )
                
                # Extract job information
                for card in job_cards:
                    try:
                        title_elem = card.find_element(By.CLASS_NAME, "jobTitle")
                        company_elem = card.find_element(By.CLASS_NAME, "companyName")
                        url_elem = title_elem.find_element(By.TAG_NAME, "a")
                        
                        job = {
                            'title': title_elem.text,
                            'company': company_elem.text,
                            'url': url_elem.get_attribute('href'),
                            'source': 'Indeed'
                        }
                        
                        jobs.append(job)
                        self.logger.info(f"Found Indeed job: {job['title']} at {job['company']}")
                        
                    except NoSuchElementException:
                        continue
                
                # Try to go to next page
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label='Next Page']")
                    if not next_button.is_enabled():
                        break
                    next_button.click()
                    time.sleep(2)
                    pages_scraped += 1
                except:
                    break
            
            self.logger.info(f"Found {len(jobs)} jobs on Indeed")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error searching Indeed jobs: {str(e)}")
            return []

    def search_internshala_jobs(self, keywords, location):
        """
        Search for jobs/internships on Internshala
        
        Args:
            keywords (str): Job search keywords
            location (str): Job location
            
        Returns:
            list: List of job dictionaries containing details
        """
        try:
            # Navigate to Internshala jobs page
            self.driver.get('https://internshala.com/jobs/work-from-home')
            time.sleep(2)
            
            # Search using keywords
            search_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Search jobs']"))
            )
            search_field.clear()
            search_field.send_keys(keywords)
            search_field.send_keys(Keys.RETURN)
            
            time.sleep(3)
            
            jobs = []
            # Scroll and collect job listings
            for _ in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                job_cards = self.driver.find_elements(By.CLASS_NAME, "job_card")
                
                for card in job_cards:
                    try:
                        job_info = {
                            'title': card.find_element(By.CLASS_NAME, "job_title").text,
                            'company': card.find_element(By.CLASS_NAME, "company_name").text,
                            'location': card.find_element(By.CLASS_NAME, "location_link").text,
                            'link': card.find_element(By.CLASS_NAME, "job_title").get_attribute('href')
                        }
                        if job_info not in jobs:
                            jobs.append(job_info)
                    except NoSuchElementException:
                        continue
            
            self.logger.info(f"Found {len(jobs)} jobs on Internshala")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error during Internshala job search: {str(e)}")
            return []

    def search_naukri_jobs(self, keywords, location):
        """
        Search for jobs on Naukri
        
        Args:
            keywords (str): Job search keywords
            location (str): Job location
            
        Returns:
            list: List of job dictionaries containing details
        """
        try:
            # Navigate to Naukri jobs page
            self.driver.get('https://www.naukri.com/')
            time.sleep(2)
            
            # Enter search criteria
            search_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "suggestor-input"))
            )
            search_field.clear()
            search_field.send_keys(keywords)
            
            location_field = self.driver.find_element(By.CLASS_NAME, "location-suggestor")
            location_field.clear()
            location_field.send_keys(location)
            
            # Click search button
            search_button = self.driver.find_element(By.CLASS_NAME, "qsbSubmit")
            search_button.click()
            
            time.sleep(3)
            
            jobs = []
            # Scroll and collect job listings
            for _ in range(5):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                job_cards = self.driver.find_elements(By.CLASS_NAME, "jobTuple")
                
                for card in job_cards:
                    try:
                        job_info = {
                            'title': card.find_element(By.CLASS_NAME, "title").text,
                            'company': card.find_element(By.CLASS_NAME, "companyInfo").text,
                            'location': card.find_element(By.CLASS_NAME, "location").text,
                            'link': card.find_element(By.CLASS_NAME, "title").get_attribute('href')
                        }
                        if job_info not in jobs:
                            jobs.append(job_info)
                    except NoSuchElementException:
                        continue
            
            self.logger.info(f"Found {len(jobs)} jobs on Naukri")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Error during Naukri job search: {str(e)}")
            return []

    def save_jobs(self, jobs, filename):
        """
        Save scraped jobs to a JSON file
        
        Args:
            jobs (list): List of job dictionaries
            filename (str): Name of file to save jobs to
        """
        try:
            Path('data').mkdir(exist_ok=True)
            with open(f'data/{filename}', 'w') as f:
                json.dump(jobs, f, indent=4)
            self.logger.info(f"Successfully saved {len(jobs)} jobs to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving jobs to file: {str(e)}")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time
import json
from pathlib import Path

class JobApplicator:
    def __init__(self, driver):
        self.driver = driver
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename='logs/applicator.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def apply_linkedin_job(self, job_url, resume_path):
        """
        Apply to a job on LinkedIn
        
        Args:
            job_url (str): URL of the job listing
            resume_path (str): Path to resume file
            
        Returns:
            bool: True if application successful, False otherwise
        """
        try:
            # Navigate to job listing
            self.driver.get(job_url)
            time.sleep(2)
            
            # Click Easy Apply button
            easy_apply_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobs-apply-button"))
            )
            easy_apply_button.click()
            time.sleep(2)

            # Handle contact info page
            next_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Continue to next step']"))
            )
            next_button.click()
            time.sleep(2)

            # Handle resume page
            try:
                resume_upload = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                resume_upload.send_keys(resume_path)
                time.sleep(2)
                next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']")
                next_button.click()
                time.sleep(2)
            except NoSuchElementException:
                self.logger.info("Resume upload not required, continuing...")

            # Handle additional questions
            try:
                # Find all yes/no questions and select "Yes"
                yes_options = self.driver.find_elements(By.CSS_SELECTOR, "input[value='Yes']")
                for option in yes_options:
                    option.click()
                
                # Find experience input fields and enter 1 year
                exp_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='number']")
                for inp in exp_inputs:
                    inp.send_keys("1")
                
                next_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Continue to next step']")
                next_button.click()
                time.sleep(2)
            except NoSuchElementException:
                self.logger.info("No additional questions found, continuing...")

            # Handle review page
            try:
                # Scroll to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                
                # Click submit button
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Submit application']"))
                )
                submit_button.click()
                time.sleep(2)
                
                self.logger.info(f"Successfully applied to job: {job_url}")
                return True
            
            except (TimeoutException, NoSuchElementException) as e:
                self.logger.error(f"Failed to submit application: {str(e)}")
                # Refresh the page if submission fails
                self.driver.refresh()
                return False
                
        except Exception as e:
            self.logger.error(f"Error applying to job: {str(e)}")
            return False

    def apply_indeed_job(self, job_url, resume_path):
        """
        Apply to a job on Indeed
        
        Args:
            job_url (str): URL of the job listing
            resume_path (str): Path to resume file
            
        Returns:
            bool: True if application successful, False otherwise
        """
        try:
            # Navigate to job listing
            self.driver.get(job_url)
            time.sleep(2)
            
            # Click Apply Now button
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "jobsearch-IndeedApplyButton-newDesign"))
            )
            apply_button.click()
            
            # Wait for application modal
            time.sleep(2)
            
            # Switch to application iframe
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "indeedapply-iframe"))
            )
            self.driver.switch_to.frame(iframe)
            
            # Upload resume if requested
            try:
                resume_upload = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
                resume_upload.send_keys(resume_path)
                time.sleep(2)
            except NoSuchElementException:
                self.logger.info("No resume upload field found")
            
            # Click through application steps
            while True:
                try:
                    # Try to find the Continue button
                    continue_button = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='continue-button']"))
                    )
                    continue_button.click()
                    time.sleep(1)
                except TimeoutException:
                    # If no Continue button, look for Submit button
                    try:
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-testid='submit-button']"))
                        )
                        submit_button.click()
                        break
                    except TimeoutException:
                        self.logger.error("Could not find Continue or Submit button")
                        return False
            
            self.logger.info(f"Successfully applied to job: {job_url}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying to Indeed job: {str(e)}")
            return False

    def apply_internshala_job(self, job_url, resume_path):
        """
        Apply to a job on Internshala
        
        Args:
            job_url (str): URL of the job listing
            resume_path (str): Path to resume file
            
        Returns:
            bool: True if application successful, False otherwise
        """
        try:
            # Navigate to job listing
            self.driver.get(job_url)
            time.sleep(2)
            
            # Click Apply Now button
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "apply_button"))
            )
            apply_button.click()
            
            # Handle resume upload if needed
            try:
                resume_upload = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
                )
                resume_upload.send_keys(resume_path)
                time.sleep(2)
            except TimeoutException:
                self.logger.info("No resume upload field found on Internshala")
            
            # Submit application
            submit_button = self.driver.find_element(By.ID, "submit_application")
            submit_button.click()
            
            time.sleep(2)
            self.logger.info(f"Successfully applied to Internshala job: {job_url}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying to Internshala job: {str(e)}")
            return False

    def apply_naukri_job(self, job_url, resume_path):
        """
        Apply to a job on Naukri
        
        Args:
            job_url (str): URL of the job listing
            resume_path (str): Path to resume file
            
        Returns:
            bool: True if application successful, False otherwise
        """
        try:
            # Navigate to job listing
            self.driver.get(job_url)
            time.sleep(2)
            
            # Click Apply button
            apply_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "apply-button"))
            )
            apply_button.click()
            
            # Handle resume upload if needed
            try:
                resume_upload = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
                )
                resume_upload.send_keys(resume_path)
                time.sleep(2)
            except TimeoutException:
                self.logger.info("No resume upload field found on Naukri")
            
            # Submit application
            submit_button = self.driver.find_element(By.CLASS_NAME, "submit-button")
            submit_button.click()
            
            time.sleep(2)
            self.logger.info(f"Successfully applied to Naukri job: {job_url}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying to Naukri job: {str(e)}")
            return False

    def bulk_apply(self, jobs_file, resume_path):
        """
        Apply to multiple jobs from a saved jobs file
        
        Args:
            jobs_file (str): Path to JSON file containing job listings
            resume_path (str): Path to resume file
        """
        try:
            with open(jobs_file, 'r') as f:
                jobs = json.load(f)
            
            successful_applications = 0
            for job in jobs:
                if 'linkedin.com' in job['link']:
                    success = self.apply_linkedin_job(job['link'], resume_path)
                elif 'indeed.com' in job['link']:
                    success = self.apply_indeed_job(job['link'], resume_path)
                elif 'internshala.com' in job['link']:
                    success = self.apply_internshala_job(job['link'], resume_path)
                elif 'naukri.com' in job['link']:
                    success = self.apply_naukri_job(job['link'], resume_path)
                else:
                    self.logger.warning(f"Unsupported job portal for URL: {job['link']}")
                    continue
                
                if success:
                    successful_applications += 1
                time.sleep(5)  # Wait between applications to avoid being flagged
            
            self.logger.info(f"Successfully applied to {successful_applications} out of {len(jobs)} jobs")
            
        except Exception as e:
            self.logger.error(f"Error during bulk application: {str(e)}")

from bot.login_manager import LoginManager
from bot.job_scraper import JobScraper
from bot.job_applicator import JobApplicator
import logging
from pathlib import Path
import json
import time

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    Path('logs').mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename='logs/main.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def apply_to_linkedin(login_manager, config, logger):
    """Handle LinkedIn job applications"""
    try:
        # Initialize job scraper
        job_scraper = JobScraper(login_manager.driver)
        
        # Search for jobs
        linkedin_jobs = job_scraper.search_linkedin_jobs(
            keywords=config['search']['keywords'],
            location=config['search']['location']
        )
        
        # Initialize job applicator
        job_applicator = JobApplicator(login_manager.driver)
        
        # Apply to each job
        for job in linkedin_jobs:
            try:
                success = job_applicator.apply_linkedin_job(
                    job_url=job['url'],
                    resume_path=config['resume_path']
                )
                if success:
                    logger.info(f"Successfully applied to job: {job['title']}")
                else:
                    logger.warning(f"Failed to apply to job: {job['title']}")
                
                # Small delay between applications
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error applying to job {job['title']}: {str(e)}")
                continue
        
        # Save jobs to file
        job_scraper.save_jobs(linkedin_jobs, 'linkedin_jobs.json')
        logger.info("LinkedIn application process completed")
        
    except Exception as e:
        logger.error(f"Error in LinkedIn process: {str(e)}")
    finally:
        login_manager.close()

def apply_to_indeed(login_manager, config, logger):
    """Handle Indeed job applications"""
    try:
        # Login to Indeed
        if not login_manager.login_indeed('config/credentials.json'):
            logger.error("Failed to login to Indeed")
            return
            
        # Initialize job scraper
        job_scraper = JobScraper(login_manager.driver)
        
        # Search for jobs on Indeed
        indeed_jobs = job_scraper.search_indeed_jobs(
            keywords=config['search']['keywords'],
            location=config['search']['location']
        )
        
        # Initialize job applicator
        job_applicator = JobApplicator(login_manager.driver)
        
        # Apply to each job
        for job in indeed_jobs:
            try:
                success = job_applicator.apply_indeed_job(
                    job_url=job['url'],
                    resume_path=config['resume_path']
                )
                if success:
                    logger.info(f"Successfully applied to Indeed job: {job['title']}")
                else:
                    logger.warning(f"Failed to apply to Indeed job: {job['title']}")
                
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error applying to Indeed job {job['title']}: {str(e)}")
                continue
        
        # Save jobs to file
        job_scraper.save_jobs(indeed_jobs, 'indeed_jobs.json')
        logger.info("Indeed application process completed")
        
    except Exception as e:
        logger.error(f"Error in Indeed process: {str(e)}")
    finally:
        login_manager.close()

def main():
    logger = setup_logging()
    
    try:
        # Load configuration
        with open('config/config.json', 'r') as f:
            config = json.load(f)
        
        # Process LinkedIn jobs
        logger.info("Starting LinkedIn job applications...")
        linkedin_manager = LoginManager()
        if linkedin_manager.login_linkedin('config/credentials.json'):
            apply_to_linkedin(linkedin_manager, config, logger)
        
        # Process Indeed jobs
        logger.info("Starting Indeed job applications...")
        indeed_manager = LoginManager()
        if indeed_manager.login_indeed('config/credentials.json'):
            apply_to_indeed(indeed_manager, config, logger)
            
        logger.info("All job application processes completed")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")

if __name__ == "__main__":
    main()

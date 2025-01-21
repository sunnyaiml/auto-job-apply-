# Automated Job Application Bot 🤖

A powerful bot that automates job applications across multiple job portals including LinkedIn, Indeed, Internshala, and Naukri. Save time and apply to multiple jobs with just one click! 

## Features 🌟
- **Multi-Platform Support**: Apply to jobs on LinkedIn, Indeed, Internshala, and Naukri
- **Google Login Integration**: Seamless login with Google account for Indeed
- **Smart Job Search**: Filter jobs based on keywords, location, and experience level
- **Automated Applications**: Automatically fills application forms and uploads resumes
- **Error Handling**: Robust error handling with detailed logging
- **Rate Limiting**: Smart delays between applications to avoid detection

## Prerequisites 📋
- Python 3.8 or higher
- Chrome browser installed
- Stable internet connection
- Valid accounts on the job portals

## Installation 🛠️

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd auto-apply
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Chrome Driver**
   - The bot uses Chrome for automation
   - Chrome WebDriver is automatically managed by the script

## Configuration ⚙️

### 1. Credentials Setup
Create `config/credentials.json`:
```json
{
    "linkedin": {
        "username": "your_linkedin_email",
        "password": "your_linkedin_password"
    },
    "indeed": {
        "email": "your_google_email",
        "login_method": "google"
    },
    "internshala": {
        "username": "your_internshala_email",
        "password": "your_internshala_password"
    },
    "naukri": {
        "username": "your_naukri_email",
        "password": "your_naukri_password"
    }
}
```

### 2. Job Search Configuration
Update `config/config.json`:
```json
{
    "search": {
        "keywords": "Software Engineer",
        "location": "Remote",
        "experience_level": "Entry Level",
        "job_type": "Full-time"
    },
    "resume_path": "assets/Sunny-Resume.pdf",
    "cover_letter_path": "assets/cover_letter.pdf",
    "application_delay": 5,
    "max_applications_per_day": 50,
    "portals": ["linkedin", "indeed", "internshala", "naukri"]
}
```

### 3. Resume and Cover Letter 📄
1. Place your resume in the `assets` folder:
   - Name it exactly as specified in `config.json` (default: "Sunny-Resume.pdf")
   - Supported formats: PDF (recommended), DOCX
2. Optional: Add your cover letter in the `assets` folder
   - Name it as specified in `config.json`

## Usage 🚀

1. **Start the Bot**
   ```bash
   python main.py
   ```

2. **Monitor Progress**
   - Check the terminal for real-time updates
   - Detailed logs are saved in the `logs` directory:
     - `main.log`: Overall bot execution
     - `scraper.log`: Job search results
     - `applicator.log`: Application attempts and results

## Portal-Specific Notes 📝

### LinkedIn
- Requires a LinkedIn account
- Premium account recommended for better results
- Supports Easy Apply applications

### Indeed (with Google Login)
- Uses Google account for login (sunny.work70@gmail.com)
- Automatically handles Google authentication
- Supports Quick Apply applications

### Internshala
- Focuses on internships and entry-level positions
- Supports both internship and job applications
- Good for fresh graduates

### Naukri
- Popular for Indian job market
- Supports multiple resume versions
- Good for experienced professionals

## Troubleshooting 🔧

### Common Issues and Solutions:
1. **Login Failed**
   - Check your credentials in `credentials.json`
   - Ensure no CAPTCHA is required
   - Try logging in manually first

2. **Resume Upload Failed**
   - Verify the resume path in `config.json`
   - Ensure the file format is supported
   - Check file permissions

3. **Application Errors**
   - Check the logs for specific error messages
   - Verify internet connection
   - Ensure the job posting is still active

## Safety Features 🛡️
- Rate limiting between applications
- Random delays to avoid detection
- Automatic error recovery
- Secure credential handling

## Maintenance 🔄
- Regularly update your resume
- Check for any changes in portal layouts
- Monitor application success rates
- Update credentials if changed

## Support 💬
For issues and feature requests:
1. Check the logs in the `logs` directory
2. Verify your configuration files
3. Ensure all credentials are correct
4. Check your internet connection

## Best Practices 📌
1. Keep your resume updated
2. Use a professional email address
3. Customize search keywords for better matches
4. Monitor application success rates
5. Follow up manually on promising applications

## License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

Happy Job Hunting! 🎯

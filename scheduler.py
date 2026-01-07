"""Scheduler for running the scraper on EC2"""

import schedule
import time
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from scraper import NitroSwimScraper, EmailNotifier
from config import SCHEDULER_CONFIG, EMAIL_CONFIG

# Configure logging with rotation
log_file = SCHEDULER_CONFIG['log_file']
handler = RotatingFileHandler(
    log_file,
    maxBytes=5*1024*1024,  # 5 MB max per file
    backupCount=3  # Keep 3 backup files
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def run_scraper_job():
    """Job to run the scraper"""
    logger.info("Starting scheduled scraper job")
    
    try:
        # Initialize scraper
        scraper = NitroSwimScraper()
        
        # Fetch and parse
        html_content = scraper.fetch_page()
        if not html_content:
            logger.error("Failed to fetch page content")
            return
        
        classes = scraper.parse_classes(html_content)
        summary = scraper.get_summary()
        
        # Log summary (only if classes found)
        if len(classes) > 0:
            logger.info(f"Found {len(classes)} available classes")
            logger.info(summary)
        else:
            logger.info("No available classes found")
        
        # Send email notification only if classes found
        if len(classes) > 0:
            notifier = EmailNotifier(
                sender_email=EMAIL_CONFIG['sender_email'],
                app_password=EMAIL_CONFIG['app_password']
            )
            
            subject = f"Nitro Swim - Available Classes ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
            email_sent = notifier.send_notification(
                recipient_email=EMAIL_CONFIG['recipient_email'],
                subject=subject,
                body=summary
            )
            
            if email_sent:
                logger.info("Email sent successfully")
            else:
                logger.warning("Email notification failed")
        
        logger.info("Job completed")
    
    except Exception as e:
        logger.error(f"Error in scheduled job: {e}", exc_info=True)


def start_scheduler():
    """Start the scheduler with specific times (CST converted to UTC)"""
    from datetime import datetime, timedelta
    
    # Schedule times in UTC (CST + 6 hours during standard time)
    # 12 AM CST = 06:00 UTC
    # 11 PM CST = 05:00 UTC
    # 2 PM CST = 20:00 UTC
    # 3 PM CST = 21:00 UTC
    # 5 PM CST = 23:00 UTC
    # 8 PM CST = 02:00 UTC (next day)
    # 10 PM CST = 04:00 UTC (next day)
    
    schedule_times = [
        "02:00",  # 8 PM CST
        "04:00",  # 10 PM CST
        "05:00",  # 11 PM CST
        "06:00",  # 12 AM CST
        "20:00",  # 2 PM CST
        "21:00",  # 3 PM CST
        "23:00",  # 5 PM CST
    ]
    
    logger.info("Starting scheduler with specific times (UTC):")
    for time_str in schedule_times:
        schedule.every().day.at(time_str).do(run_scraper_job)
        logger.info(f"  - {time_str} UTC")
    
    logger.info("Scheduler started. Waiting for scheduled times...")
    
    last_run_date = None
    
    # Run the scheduler
    try:
        while True:
            now = datetime.utcnow()
            current_time = now.strftime("%H:%M")
            current_date = now.date()
            
            # Check if we're within 1 minute of a scheduled time
            for time_str in schedule_times:
                scheduled_hour, scheduled_minute = map(int, time_str.split(":"))
                time_diff = abs(now.hour * 60 + now.minute - (scheduled_hour * 60 + scheduled_minute))
                
                # If within 1 minute and haven't run today yet
                if time_diff <= 1 and last_run_date != current_date:
                    logger.info(f"Running job at {current_time} UTC (scheduled for {time_str})")
                    run_scraper_job()
                    last_run_date = current_date
                    break
            
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.error(f"Scheduler error: {e}", exc_info=True)


if __name__ == "__main__":
    start_scheduler()

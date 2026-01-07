from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NitroSwimScraper:
    def __init__(self):
        self.url = "https://nitroswim.captyn.com/find?program=clmjaygzh0c1wlm1bk30yfua0&capacity=available"
        self.available_classes = []
    
    def fetch_page(self):
        """Fetch the webpage content using Playwright with optimizations"""
        try:
            logger.info(f"Fetching page with Playwright: {self.url}")
            with sync_playwright() as p:
                # Launch with minimal resources
                browser = p.chromium.launch(
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )
                
                # Create context with reduced resource usage
                context = browser.new_context()
                page = context.new_page()
                
                # Block images and stylesheets to reduce data transfer
                page.route("**/*.{png,jpg,jpeg,gif,svg,webp,css}", lambda route: route.abort())
                
                page.goto(self.url, wait_until='domcontentloaded', timeout=30000)
                
                # Wait for class content to load with retries
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        page.wait_for_function("() => document.body.innerText.includes('spot')", timeout=8000)
                        logger.info("Class content loaded successfully")
                        break
                    except:
                        if attempt < max_retries - 1:
                            logger.warning(f"Retry {attempt + 1}/{max_retries - 1}: Waiting for class content...")
                            page.wait_for_timeout(2000)
                        else:
                            logger.warning("Max retries reached, proceeding with available content")
                
                page.wait_for_timeout(2000)
                
                html_content = page.content()
                
                # Clean up resources
                context.close()
                browser.close()
                
            logger.info(f"Page fetched successfully, HTML length: {len(html_content)}")
            return html_content
        except Exception as e:
            logger.error(f"Error fetching page: {e}")
            return None
    
    def parse_classes(self, html_content):
        """Parse available classes from HTML"""
        try:
            self.available_classes = []
            page_text = html_content
            
            # Find all occurrences of "N spots open" or "N spot open"
            spot_pattern = r'(\d+)\s*spot[s]?\s*open'
            spot_matches = list(re.finditer(spot_pattern, page_text, re.IGNORECASE))
            
            logger.info(f"Found {len(spot_matches)} spot matches in HTML")
            
            for idx, spot_match in enumerate(spot_matches):
                available_spots = int(spot_match.group(1))
                spot_pos = spot_match.start()
                
                # Look backwards to find TF number (search in larger window)
                search_start = max(0, spot_pos - 2000)
                before_text = page_text[search_start:spot_pos]
                
                # Search for TF in the before_text
                tf_matches = list(re.finditer(r'TF\s*(\d+)', before_text, re.IGNORECASE))
                
                logger.debug(f"Match {idx}: Found {len(tf_matches)} TF matches, {available_spots} spots open")
                
                if tf_matches:
                    # Get the last (closest) TF match
                    tf_match = tf_matches[-1]
                    class_num = tf_match.group(1)
                    
                    # Get context for time extraction
                    context_start = max(0, spot_pos - 1500)
                    context_end = min(len(page_text), spot_pos + 300)
                    context = page_text[context_start:context_end]
                    
                    class_info = self._extract_class_info(f"TF {class_num}", available_spots, context)
                    if class_info:
                        logger.info(f"Added class: {class_info}")
                        self.available_classes.append(class_info)
            
            logger.info(f"Total classes found: {len(self.available_classes)}")
            return self.available_classes
        
        except Exception as e:
            logger.error(f"Error parsing classes: {e}", exc_info=True)
            return []
    
    def _extract_class_info(self, class_type, available_spots, context):
        """Extract class information from context"""
        try:
            # Extract time information (e.g., "4:05 pm-4:50 pm")
            time_match = re.search(r'(\d{1,2}:\d{2}\s*(?:am|pm))\s*-\s*(\d{1,2}:\d{2}\s*(?:am|pm))', context, re.IGNORECASE)
            if time_match:
                time = f"{time_match.group(1)}-{time_match.group(2)}"
            else:
                time = "N/A"
            
            # Extract day information - look for day patterns like "M, W" or "Tu, Th"
            # Try multiple patterns
            day = "N/A"
            
            # Pattern 1: Day abbreviations followed by time (M, W 4:05 pm)
            day_match = re.search(r'([A-Z][a-z]?(?:\s*,\s*[A-Z][a-z]?)*)\s+\d{1,2}:\d{2}', context)
            if day_match:
                day = day_match.group(1).strip()
            else:
                # Pattern 2: Look for common day abbreviations anywhere in context
                day_patterns = ['M, W', 'Tu, Th', 'M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']
                for pattern in day_patterns:
                    if pattern in context:
                        day = pattern
                        break
            
            return {
                'class_type': class_type,
                'available_spots': available_spots,
                'time': time,
                'day': day,
                'location': 'Nitro Swimming Cedar Park',
                'category': 'Technique and Fitness (TF)'
            }
        
        except Exception as e:
            logger.debug(f"Error extracting class info: {e}")
            return None
    
    def get_summary(self):
        """Generate summary of available classes"""
        if not self.available_classes:
            return "No available classes found."
        
        summary = f"Available Classes Summary ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
        summary += f"Total Classes with Availability: {len(self.available_classes)}\n"
        summary += "=" * 60 + "\n\n"
        
        for idx, cls in enumerate(self.available_classes, 1):
            summary += f"{idx}. {cls['class_type']} - {cls['category']}\n"
            summary += f"   Day: {cls['day']}\n"
            summary += f"   Time: {cls['time']}\n"
            summary += f"   Available Spots: {cls['available_spots']}\n"
            summary += f"   Location: {cls['location']}\n"
            summary += "-" * 60 + "\n"
        
        summary += "\n" + "=" * 60 + "\n"
        summary += "REGISTER NOW:\n"
        summary += "https://nitroswim.captyn.com/find?program=clmjaygzh0c1wlm1bk30yfua0&capacity=available\n"
        summary += "=" * 60 + "\n"
        
        return summary


class EmailNotifier:
    def __init__(self, sender_email, app_password):
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_notification(self, recipient_email, subject, body):
        """Send email notification"""
        try:
            logger.info(f"Sending email to {recipient_email}")
            
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)
            
            logger.info("Email sent successfully")
            return True
        
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed. Check email and app password.")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False


def main():
    """Main execution function"""
    # Initialize scraper
    scraper = NitroSwimScraper()
    
    # Fetch and parse
    html_content = scraper.fetch_page()
    if not html_content:
        logger.error("Failed to fetch page content")
        return
    
    classes = scraper.parse_classes(html_content)
    summary = scraper.get_summary()
    
    # Print summary to console
    print("\n" + summary)
    
    # Send email notification
    notifier = EmailNotifier(
        sender_email="tanmoyc379@gmail.com",
        app_password="jbwd pnec blvs crla"
    )
    
    subject = f"Nitro Swim - Available Classes ({datetime.now().strftime('%Y-%m-%d')})"
    email_sent = notifier.send_notification(
        recipient_email="tanmoyc999@gmail.com",
        subject=subject,
        body=summary
    )
    
    if email_sent:
        logger.info("Notification process completed successfully")
    else:
        logger.warning("Email notification failed, but scraping completed")


if __name__ == "__main__":
    main()

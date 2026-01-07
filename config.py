"""Configuration file for Nitro Swim Scraper"""
import os
from dotenv import load_dotenv

load_dotenv()

SCRAPER_CONFIG = {
    'url': 'https://nitroswim.captyn.com/find?program=clmjaygzh0c1wlm1bk30yfua0&capacity=available',
    'timeout': 10,
    'location': 'Nitro Cedar Park',
    'category': 'Technique and Fitness (TF)',
    'max_classes': 12
}

EMAIL_CONFIG = {
    'sender_email': os.getenv('SENDER_EMAIL'),
    'app_password': os.getenv('APP_PASSWORD'),
    'recipient_email': os.getenv('RECIPIENT_EMAIL'),
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}

SCHEDULER_CONFIG = {
    'interval_minutes': 60,
    'log_file': '/var/log/nitro_swim/nitro_swim_scraper.log',
    'enable_logging': True
}

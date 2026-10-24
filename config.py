import os
from dotenv import load_dotenv
import json

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True').lower() in ('true', '1')
    MAIL_DEFAULT_SENDER = os.environ.get('SENDER_EMAIL') or os.environ.get('MAIL_USERNAME')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
    FACEBOOK_OAUTH_CLIENT_ID = os.environ.get('FACEBOOK_OAUTH_CLIENT_ID')
    FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get('FACEBOOK_OAUTH_CLIENT_SECRET')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/fit-o-sphere'
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')
    CHATBOT_API_KEY = os.environ.get('CHATBOT_API_KEY')

    # Load non-sensitive upload location safely
    try:
        with open('config.json') as config_file:
            config_data = json.load(config_file)
            UPLOAD_LOCATION = config_data.get('params', {}).get('upload_location', 'static/images')
    except Exception:
        UPLOAD_LOCATION = os.path.join(os.path.dirname(__file__), 'static', 'images')

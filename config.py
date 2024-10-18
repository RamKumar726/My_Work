import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:1234@localhost/backend')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENTITY_API_KEY = os.getenv('ENTITY_API_KEY','ec471071441bb2ac538a0ff901abd249')
    ENTITY_API_URL = os.getenv("ENTITY_API_URL", 'https://rest.entitysport.com/v2/matches')
    API_2FA = os.getenv('API_2FA','34e9b2ab-8574-11ef-8b17-0200cd936042')
    OTP_BASE_URL = os.getenv("OTP_BASE_URL",'https://2factor.in/API/V1')
    SECRET_KEY = 'backend'
    OTP_EXPIRY_TIME = os.getenv("OTP_EXP_TIME")
    JWT_EXPIRATION_TIME = os.getenv('JWT_EXPIRATION_TIME')
    API_DOMAIN = os.getenv('API_DOMAIN')
    BRAND_NAME = os.getenv('BRAND_NAME')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False



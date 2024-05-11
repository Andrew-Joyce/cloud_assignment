class Config:
    SECRET_KEY = 'Andrew_Joyce'
    DYNAMODB_REGION = 'ap-southeast-2'

class DevelopmentConfig(Config):
    DEBUG = True
    LOGGING_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    DEBUG = False
    LOGGING_LEVEL = 'ERROR'


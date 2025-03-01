class Config:
    SECRET_KEY="Kunal@2004"
    SQLALCHEMY_DATABASE_URI='sqlite:///database.sqlite3'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'kunalg2022@gmail.com'
    MAIL_PASSWORD = 'Kunal@2004'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

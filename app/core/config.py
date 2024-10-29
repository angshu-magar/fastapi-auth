from dotenv import load_dotenv, dotenv_values

class Settings():
    def __init__(self):
        load_dotenv()
        env_vars = dotenv_values()
        self.sqlalchemy_database_url = env_vars.get('SQLALCHEMY_DATABASE_URL') or ""
        self.secret_key = env_vars.get('SECRET_KEY') or ""
        self.algorithm = env_vars.get('ALGORITHM') or ""
        self.access_token_expire_minutes = int(env_vars.get('ACCESS_TOKEN_EXPIRE_MINUTES') or 0)

settings = Settings()

EXCLUDED_PATHS = ['docs', 'openapi.json', 'api/token']

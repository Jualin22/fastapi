from pydantic import BaseSettings

# from dotenv import load_dotenv
# dotenv_path = r"C:\Users\julian.starke\env_var\Env_Var.env"
# load_dotenv(dotenv_path=dotenv_path)

# Validate environment variables


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()

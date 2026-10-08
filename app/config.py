from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username: str ="username"
    database_password: str ="password"
    database_hostname: str ="hostname"
    database_port: str ="5432"
    database_name: str ="name"
    secret_key: str ="secret_key"
    algorithm: str ="algorithm"
    access_token_expire_minutes: int = 30

    class Config:
        env_file=r"C:\Deepa\PythonFastAPI\.env"

settings = Settings()

#print(settings.model_dump())


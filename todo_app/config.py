from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str 
    hashing_algorithm: str
    db_engine: str
    db_host: str
    db_port: int
    db_database_name: str
    db_username: str
    db_password: str

    class Config:
        case_sensitive = False

settings = Settings()
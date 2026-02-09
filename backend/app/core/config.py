from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SME ERP Backend"
    api_v1_prefix: str = "/api/v1"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()

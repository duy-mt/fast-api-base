from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str
    DATABASE: str
    API_KEY: str
    ORIGIN: str
    ORIGIN_DOCKER: str
    ORIGIN_KONG: str

    class Config:
        env_file = ".env"


settings = Settings()

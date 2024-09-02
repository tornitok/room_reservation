from pydantic import BaseSettings

class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    database_url: str
    description: str = ''

    class Config:
        env_file = '.env'


settings = Settings()

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    description: str = ''
    data_base: str

    class Config:
        env_file = '.env'


settings = Settings()

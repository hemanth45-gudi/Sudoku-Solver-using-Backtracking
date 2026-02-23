import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sudoku Solver"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # GUI Settings
    DEFAULT_THEME: str = "dark"  # or "light"
    ANIMATION_SPEED: float = 0.05
    
    # Solver Settings
    MAX_STEPS: int = 100000
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

"""
Core configuration module for the ERP backend application.
Loads environment variables and provides centralized configuration.
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field
import logging


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = Field(default="ERP Backend API", alias="APP_NAME")
    app_version: str = Field(default="1.0.0", alias="APP_VERSION")
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=3001, alias="PORT")
    uvicorn_host: str = Field(default="0.0.0.0", alias="UVICORN_HOST")
    uvicorn_workers: int = Field(default=1, alias="UVICORN_WORKERS")
    
    # URLs
    backend_url: str = Field(default="http://localhost:3001", alias="BACKEND_URL")
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")
    ws_url: str = Field(default="ws://localhost:3001/ws", alias="WS_URL")
    site_url: str = Field(default="http://localhost:3000", alias="SITE_URL")
    
    # CORS
    allowed_origins: str = Field(default="http://localhost:3000", alias="ALLOWED_ORIGINS")
    allowed_headers: str = Field(default="Content-Type,Authorization,X-Requested-With", alias="ALLOWED_HEADERS")
    allowed_methods: str = Field(default="GET,POST,PUT,DELETE,PATCH,OPTIONS", alias="ALLOWED_METHODS")
    cors_max_age: int = Field(default=3600, alias="CORS_MAX_AGE")
    
    # Security
    cookie_domain: str = Field(default="localhost", alias="COOKIE_DOMAIN")
    trust_proxy: bool = Field(default=True, alias="TRUST_PROXY")
    
    # Performance
    request_timeout_ms: int = Field(default=30000, alias="REQUEST_TIMEOUT_MS")
    rate_limit_window_s: int = Field(default=60, alias="RATE_LIMIT_WINDOW_S")
    rate_limit_max: int = Field(default=100, alias="RATE_LIMIT_MAX")
    
    # Environment
    node_env: str = Field(default="development", alias="NODE_ENV")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"
    
    def get_origins_list(self) -> List[str]:
        """Parse and return list of allowed origins."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    def get_headers_list(self) -> List[str]:
        """Parse and return list of allowed headers."""
        return [header.strip() for header in self.allowed_headers.split(",")]
    
    def get_methods_list(self) -> List[str]:
        """Parse and return list of allowed methods."""
        return [method.strip() for method in self.allowed_methods.split(",")]


# Singleton instance
settings = Settings()


def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )
    
    # Set third-party loggers to WARNING
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)


# Initialize logging
setup_logging()

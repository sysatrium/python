# Product: Python Builder Pattern Example
# Description: This code demonstrates the Builder Pattern in Python, allowing for flexible and readable configuration of server settings.

from typing import List, Optional, Union
from dataclasses import dataclass
from pydantic import SecretStr
import enum
import re


class LogLevel(enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


MIN_PORT = 1
MAX_PORT = 65535


@dataclass(frozen=True)
class ServerConfiguration:
    host: str
    port: int
    max_connections: Optional[int]
    logging_level: Optional[Union[LogLevel, str]]
    static_files_directory: Optional[str]
    allowed_hosts: Optional[List[str]]
    timeout: Optional[int]
    ssl_cert: Optional[Union[SecretStr, str]]
    ssl_key: Optional[Union[SecretStr, str]]
    ssl_enabled: Optional[bool]


class ServerConfigurationBuilder:
    def __init__(self):
        self.host: str = "localhost"
        self.port: int = 80
        self.max_connections: Optional[int] = 100
        self.logging_level: Optional[Union[LogLevel, str]] = LogLevel.INFO
        self.static_files_directory: Optional[str] = None
        self.allowed_hosts: Optional[List[str]] = None
        self.timeout: Optional[int] = None
        self.ssl_cert: Optional[Union[SecretStr, str]] = None
        self.ssl_key: Optional[Union[SecretStr, str]] = None
        self.ssl_enabled: Optional[bool] = None

    def _validate_host(self, host: str):
        if not host or not isinstance(host, str):
            raise ValueError("Host is required and must be not-empty string.")

    def _validate_port(self, port: int):
        if not isinstance(port, int):
            raise ValueError(f"Port is required and must be an integer, got: {port}")
        if port < MIN_PORT or port > MAX_PORT:
            raise ValueError(
                f"Port is required and must be an integer between {MIN_PORT} and {MAX_PORT}, got: {port}"
            )

    def _validate_ssl(self, ssl_enabled: bool, ssl_cert: SecretStr, ssl_key: SecretStr):
        if ssl_enabled is True and (not ssl_cert or not ssl_key):
            raise ValueError(
                "SSL is enabled but no SSL certificate or key was provided."
            )
        elif ssl_enabled is False and (
            (
                isinstance(ssl_cert, SecretStr)
                or isinstance(ssl_key, SecretStr)
                or isinstance(ssl_cert, str)
                or isinstance(ssl_key, str)
            )
        ):
            raise ValueError("SSL is disabled but SSL certificate or key was provided.")

    def set_host(self, host: str) -> "ServerConfigurationBuilder":
        self.host = host
        return self

    def set_port(self, port: int) -> "ServerConfigurationBuilder":
        self.port = port
        return self

    def set_logging_level(
        self, logging_level: Optional[Union[LogLevel, str]]
    ) -> "ServerConfigurationBuilder":
        if isinstance(logging_level, str):
            try:
                logging_level = LogLevel[logging_level.upper()]
            except KeyError:
                raise ValueError(
                    f"Logging level must be one of {list(LogLevel.__members__.keys())}, got {logging_level}."
                )
        self.logging_level = logging_level
        return self

    def set_ssl_enabled(self, ssl_enabled: bool) -> "ServerConfigurationBuilder":
        self.ssl_enabled = ssl_enabled
        return self

    def set_ssl_cert(
        self, ssl_cert: Optional[Union[SecretStr, str]]
    ) -> "ServerConfigurationBuilder":
        self.ssl_cert = (
            ssl_cert if isinstance(ssl_cert, SecretStr) else SecretStr(ssl_cert)
        )
        return self

    def set_ssl_key(
        self, ssl_key: Optional[Union[SecretStr, str]]
    ) -> "ServerConfigurationBuilder":
        self.ssl_key = ssl_key if isinstance(ssl_key, SecretStr) else SecretStr(ssl_key)
        return self

    def build(self) -> ServerConfiguration:
        self._validate_host(self.host)
        self._validate_port(self.port)
        self._validate_ssl(self.ssl_enabled, self.ssl_cert, self.ssl_key)

        config = ServerConfiguration(
            host=self.host,
            port=self.port,
            max_connections=self.max_connections,
            logging_level=self.logging_level,
            static_files_directory=self.static_files_directory,
            allowed_hosts=self.allowed_hosts,
            timeout=self.timeout,
            ssl_cert=self.ssl_cert,
            ssl_key=self.ssl_key,
            ssl_enabled=self.ssl_enabled,
        )
        return config


if __name__ == "__main__":
    builder = ServerConfigurationBuilder()
    builder.set_port(8080).set_logging_level("DEBUG").set_ssl_cert("/path").set_ssl_key(
        "/path"
    ).set_ssl_enabled(True)
    config = builder.build()
    print(config.__dict__)

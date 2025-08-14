# Product: Python Builder Pattern Example
# Description: This code demonstrates the Builder Pattern in Python, allowing for flexible and readable configuration of server settings.

from typing import List, Optional, Union
from dataclasses import dataclass, fields
from pydantic import SecretStr
import enum
import re
import os


class LogLevel(enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


MIN_PORT = 1
MAX_PORT = 65535


@dataclass(frozen=True)
class ServerConfiguration:
    host: str = "localhost"
    port: int = 80
    max_connections: Optional[int] = 50
    logging_level: Optional[Union[LogLevel, str]] = None
    static_files_directory: Optional[str] = None
    allowed_hosts: Optional[List[str]] = None
    timeout: Optional[int] = 10
    ssl_cert: Optional[Union[SecretStr, str]] = None
    ssl_key: Optional[Union[SecretStr, str]] = None
    ssl_enabled: Optional[bool] = False


class ServerConfigurationBuilder:
    def __init__(self):
        for field in fields(ServerConfiguration):
            setattr(self, field.name, field.default)

    def _validate_allowed_hosts(self, allowed_hosts: Optional[List[str]]):
        if allowed_hosts:
            for host in allowed_hosts:
                if not re.match(r"^[a-zA-Z0-9.-]+$", host):
                    raise ValueError(
                        f"Allowed host must be a valid hostname, got: {host}"
                    )

    def _validate_static_files_directory(self, static_files_directory: Optional[str]):
        if static_files_directory:
            if not os.path.exists(static_files_directory):
                raise ValueError(
                    f"Static files directory must be a valid directory, got: {static_files_directory}"
                )

    def _validate_timeout(self, timeout: Optional[int]):
        if timeout and timeout < 0:
            raise ValueError(f"Timeout must be a non-negative integer, got: {timeout}")

    def _validate_max_connections(self, max_connections: Optional[int]):
        if max_connections and max_connections < 0:
            raise ValueError(
                f"Max connections must be a non-negative integer, got: {max_connections}"
            )

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
        if ssl_enabled is True:
            if not ssl_cert or not ssl_key:
                raise ValueError(
                    "SSL is enabled but no SSL certificate or key was provided."
                )
        else:
            if ssl_cert or ssl_key:
                raise ValueError(
                    "SSL is disabled but SSL certificate or key was provided."
                )

    def set_host(self, host: str) -> "ServerConfigurationBuilder":
        self._validate_host(host)
        self.host = host
        return self

    def set_port(self, port: int) -> "ServerConfigurationBuilder":
        self._validate_port(port)
        self.port = port
        return self

    def set_max_connections(
        self, max_connections: Optional[int]
    ) -> "ServerConfigurationBuilder":
        self._validate_max_connections(max_connections)
        self.max_connections = max_connections
        return self

    def set_timeout(self, timeout: Optional[int]) -> "ServerConfigurationBuilder":
        self._validate_timeout(timeout)
        self.timeout = timeout
        return self

    def set_static_files_directory(
        self, static_files_directory: Optional[str]
    ) -> "ServerConfigurationBuilder":
        self._validate_static_files_directory(static_files_directory)
        self.static_files_directory = static_files_directory
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

    def set_allowed_hosts(
        self, allowed_hosts: Optional[List[str]]
    ) -> "ServerConfigurationBuilder":
        self._validate_allowed_hosts(allowed_hosts)
        self.allowed_hosts = allowed_hosts
        return self

    def build(self) -> ServerConfiguration:

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


# Director
class Director:
    def __init__(self):
        self.builder = ServerConfigurationBuilder()

    def producation_configuration(self):
        return (
            self.builder.set_host("127.0.0.1")
            .set_port(8080)
            .set_logging_level("INFO")
            .build()
        )


if __name__ == "__main__":
    director = Director()
    prod = Director()
    production = prod.producation_configuration()
    director.builder.set_port(8080).set_logging_level("DEBUG").set_ssl_cert(
        "/path"
    ).set_ssl_key("/path").set_ssl_enabled(True).set_max_connections(100)
    config = director.builder.build()
    print(config)
    print(production)

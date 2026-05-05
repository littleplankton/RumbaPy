from __future__ import annotations

import os
import logging
import configparser
from typing import Optional, Any, Union
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CredentialsConfig:
    cics_id: str
    cics_password: str
    ims_id: str
    ims_password: str

    @classmethod
    def from_config(cls, config: configparser.ConfigParser) -> CredentialsConfig:
        return cls(
            cics_id=config['cics']['id'],
            cics_password=config['cics']['password'],
            ims_id=config['rhelp']['id'],
            ims_password=config['rhelp']['password']
        )

@dataclass
class PathsConfig:
    python_32bit: Path

    @classmethod
    def from_config(cls, config: configparser.ConfigParser) -> PathsConfig:
        return cls(
            python_32bit=Path(config['32bit_python']['path'])
        )

class Config:
    _config_instance = None
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None) -> None:
        self.config_path = config_path or Path("config.ini")
        self.config = self._load_config()

        self.credentials = CredentialsConfig.from_config(self.config)
        self.paths = PathsConfig.from_config(self.config)

    def _load_config(self) -> configparser.ConfigParser:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        config = configparser.ConfigParser()
        config.read(self.config_path, encoding='utf-8')
        return config
    
    @classmethod
    def load_config(cls, config_path: Optional[Union[str, Path]] = None) -> configparser.ConfigParser:
        if cls._config_instance is None:
            cls._config_instance = cls(config_path)
        return cls._config_instance.config

class Logger:
    def __init__(self, name: str, log_dir: Path) -> None:
        self.name = name
        self.log_dir = log_dir
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        self.log_dir.mkdir(exist_ok=True)

        logger = logging.getLogger(self.name)

        if not logger.hasHandlers():
            logger.setLevel(logging.INFO)

            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )

            file_handler = logging.FileHandler(
                self.log_dir / f'{self.name}.log',
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        return logger

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        self.logger.critical(message, *args, **kwargs)
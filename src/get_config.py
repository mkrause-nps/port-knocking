#!/usr/bin/env python3

import configparser

CONFIG_FILENAME: str = "./config.ini"


def get_config() -> configparser.ConfigParser:
    """Assign configuration values to variables."""
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILENAME)
    except configparser.NoSectionError:
        print("No section config")
        exit(1)

    return config

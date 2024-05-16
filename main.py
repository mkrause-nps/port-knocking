#!/usr/bin/env python3

import configparser
from src.detect import detect_knock_sequence

CONFIG_FILENAME: str = './config.ini'

class Config:
    vars: dict = {}


def main():
    get_config()
    detect_knock_sequence()


def get_config():
    """Assign configuration values to variables."""
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILENAME)
    except configparser.NoSectionError:
        print('No section config')
        exit(1)

    try:
        for section in config.sections():
            print(f'Section: {section}')
            for key in config[section]:
                Config.vars[key] = config[section][key]

    except configparser.Error as e:
        print(f'An error occurred: {e}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""

    # disable if production
    # env_setting()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pur_beurre.settings.production')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def env_setting():
    # open file .env for set setting
    with open(".env", "r") as file:
        lines = file.readlines()
    for line in lines:
        lg = line.split(" ")
        word_list = []
        # remove "\n"
        for letter in lg[2]:
            if "\n" != letter:
                word_list.append(letter)
        word = "".join(word_list)
        # append key in os
        os.environ[lg[0]] = word


if __name__ == '__main__':
    main()



#!/usr/bin/env python
import os
import sys

base_dir = os.path.abspath(os.path.dirname(__file__))
config_dir = os.path.join(os.path.dirname(base_dir), 'selfieclub-config')
sys.path.append(config_dir)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selfieclub.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

#!/usr/bin/env python
import os
import sys
import logging

if __name__ == "__main__":
    sys.path.append('virtual_deconstruction_hub')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "virtual_deconstruction_hub.settings")

    from django.core.management import execute_from_command_line
    from util import constants, logger

    # Configure default.cfg file variables
    constants.load('virtual_deconstruction_hub/config/default.cfg')
    # Configure the logging module
    logger.configure()

    execute_from_command_line(sys.argv)

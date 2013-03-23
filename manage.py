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

    from django.db.models import signals
    from django.contrib.auth.management import create_superuser
    from django.contrib.auth import models as auth_app

    # Prevent interactive question about wanting a superuser created.  (This
    # code has to go in this otherwise empty "models" module so that it gets
    # processed by the "syncdb" command during database creation.)

    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_app,
        dispatch_uid = "django.contrib.auth.management.create_superuser")

    execute_from_command_line(sys.argv)

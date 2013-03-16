#!/usr/bin/env python

import os
import sys

if __name__ == "__main__":
    sys.path.append('virtual_deconstruction_hub')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "virtual_deconstruction_hub.settings")

    from django.core.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)

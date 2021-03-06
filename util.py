# -*- coding: utf-8 -*-
import time
import traceback

from config import config


def log_error(exception, args=None, kwargs=None):
    with open(config['ERROR_LOGS_DIR'] + time.strftime('%Y%m%d_%H%M%S') + ".txt", 'a') as err_file:
        if args:
            err_file.write("ARGS: " + str(args) + "\n")
        if kwargs:
            err_file.write("KEYWORD ARGS:\n")
            for key in kwargs:
                err_file.write(str(key) + " : " + str(kwargs[key]) + "\n")
        err_file.write(f'{exception}\n\n'.upper())
        traceback.print_exc(file=err_file)


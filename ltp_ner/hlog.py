#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import os
import time


__all__ = ["hlogger"]

Path = str


def hlogger(directory: Path = os.getcwd(), file_level: str = "INFO", stream_level: str = "DEBUG"):

    logger = logging.getLogger()
    logger.setLevel(level=logging.DEBUG)
    level_dict = {"INFO": logging.INFO, "DEBUG": logging.DEBUG, "WARN": logging.WARNING, "ERROR": logging.ERROR,
                  "CRITICAL": logging.CRITICAL, "NOTSET": logging.NOTSET}
    formatter = logging.Formatter("%(asctime)s - %(filename)s -%(funcName)s- %(lineno)s - %(levelname)s - %(message)s")
    logger_name = time.strftime("%Y%m%d", time.localtime(time.time())) + '.log'
    os.makedirs(os.path.join(directory, 'run'), exist_ok=True)

    #防止重复写日志
    if not logger.handlers:
        file = logging.FileHandler(os.path.join('run', logger_name))
        file.setLevel(level=level_dict[file_level])
        file.setFormatter(formatter)
        logger.addHandler(file)
        stream = logging.StreamHandler()
        stream.setFormatter(formatter)
        stream.setLevel(level=level_dict[stream_level])
        logger.addHandler(stream)

    return logger

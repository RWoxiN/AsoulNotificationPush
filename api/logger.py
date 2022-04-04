from distutils import log
# -*- coding: utf-8 -*-
import logging

logging.basicConfig(
    format='%(asctime)s : %(levelname)s: {%(module)s} [%(funcName)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

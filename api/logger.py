# -*- coding: utf-8 -*-
import logging

logging.basicConfig(
    filename='asoul.log',
    filemode='a',
    encoding='utf-8',
    format='%(asctime)s : %(levelname)s: {%(module)s} [%(funcName)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

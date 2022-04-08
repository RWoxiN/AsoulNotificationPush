# -*- coding: utf-8 -*-
import logging
from .config import *

a_config = anp_config().load_config()
low_version_python_compatible = a_config.get('low_version_python_compatible')

if low_version_python_compatible:
    logging.basicConfig(
        filename='asoul.log',
        filemode='a',
        format='%(asctime)s : %(levelname)s: {%(module)s} [%(funcName)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
else:
    logging.basicConfig(
        filename='asoul.log',
        filemode='a',
        encoding='utf-8', # 服务器中 python 版本过低需去掉该行，否则会报错
        format='%(asctime)s : %(levelname)s: {%(module)s} [%(funcName)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

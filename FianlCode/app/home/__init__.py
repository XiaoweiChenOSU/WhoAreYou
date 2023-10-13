# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2019/6/7--19:51
__author__ = 'Wei'

from flask import Blueprint

home = Blueprint('home',__name__)

import app.home.views
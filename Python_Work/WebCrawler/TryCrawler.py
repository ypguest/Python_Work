# !/usr/bin/python
# -*- coding: utf-8 -*-

import requests

r = requests.get('https://www.163.com')
print(r.text)
#!/usr/bin/python
# -*- coding: utf-8
##############################################################################
# Politraf, initial setup
##############################################################################

import dbmodels
import shutil
import os
import yaml

# Read config
with open("/etc/politraf/config.yaml", 'r') as stream:
    try:
        config = (yaml.load(stream))
        url = config['db_url']
        name = config['username']
        passw = config['password']
    except yaml.YAMLError as e:
        print(e)


try:
    # Read config
    print ("Copy config.yaml to /etc/politraf")
    shutil.copy2('config/config.yaml', '/etc/politraf/config.yaml')
    with open("/etc/politraf/config.yaml", 'r') as stream:
        config = (yaml.load(stream))
        url = config['db_url']
        name = config['username']
        passw = config['password']
    db = dbmodels.Database('politraf', db_url=url, username=name, password=passw, readonly=False, autocreate=True)
    print ("Make dir /opt/politraf")
    os.makedirs("/opt/politraf")
    print ("Setup services")
    shutil.copy2('config/systat.service', '/etc/systemd/system/systat.service')
    shutil.copy2('config/constat.service', '/etc/systemd/system/constat.service')
    print ("Copy politraf files")
    shutil.copy2('systat.py', '/opt/politraf/systat.py')
    shutil.copy2('otxget.py', '/opt/politraf/otxget.py')
    shutil.copy2('constat.py', '/opt/politraf/constat.py')
    shutil.copy2('dbmodels.py', '/opt/politraf/dbmodels.py')
    print ("Create database with tables")
    db.create_table(dbmodels.CONNStats)
    db.create_table(dbmodels.CPUStats)
    db.create_table(dbmodels.MEMStats)
    db.create_table(dbmodels.DISKStats)
    db.create_table(dbmodels.IOCStats)
except Exception as e:
    print(e)
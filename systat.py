#!/usr/bin/env python3
# -*- coding: utf-8

import dbmodels
from pytz import timezone
import psutil, time, datetime
from datetime import datetime


db = Database('sys_stat')
db.create_table(CPUStats)
db.create_table(MEMStats)
db.create_table(DISKStats)

if __name__ == '__main__':
    
    running = True
    while running:
        try:
            time.sleep(10)
            stats = psutil.cpu_percent(percpu=True)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            tz = pytz.timezone('Europe/Moscow')
            timestamp = datetime.now()
            today = datetime.strftime(datetime.now(), '%Y-%m-%d')
            db.insert([
                CPUStats(event_date=today, timestamp=timestamp, cpu_id=cpu_id, cpu_percent=cpu_percent)
                for cpu_id, cpu_percent in enumerate(stats)
            ])
            db.insert([
                MEMStats(event_date=today, timestamp=timestamp, total=mem[0], used=mem[3])
            ])
            db.insert([
                DISKStats(event_date=today, timestamp=timestamp, total=disk[0], used=disk[1])
            ])
        except Exception as e:
            print(e)
            running = False
        
# wanchain_monitor

## Task: Extend the monitor job
### osm_account_healthy_xrp_trust_line_monitor.py
    monitor the working groups trust lines

## config: Store the config file
    1. ".iWAN_Config.json"
     Apply the keys from "https://iwan.wanchain.org/"
        {
                "main": {
                    "secretkey": "***",
                    "Apikey": "***"
                },
                "test": {
                    "secretkey": "***",
                    "Apikey": "***"
                }
        }
    2. "chainInfos.json" 
     Get from "https://github.com/Nevquit/configW/blob/main/chainInfos.json"

    3. "crossPoolTokenInfo.json"
     Get from "https://github.com/Nevquit/configW/blob/main/crossPoolTokenInfo.json"

## Report: to store the related reports
    Notice: 1. ensure the report name is unique; 2.Follow the format Report_task_date.html


## utils: Extend tools for monitor
    1. update  __init__.py
    2. update utils.py

## requiremens.txt
       https://learnpython.com/blog/python-requirements-file/
       create: pip freeze > requirements.txt
       install:pip install -r requirements.txt

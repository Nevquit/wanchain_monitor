# wanchain_monitor
## How to add task
        1. add task under './task'
        2. config the email list and dingding api in './config/.email_ding_contact.json'
    
## Task: Extend the monitor job
### osm_account_healthy_xrp_trust_line_monitor.py
        monitor the working groups trust lines
### osm_account_balance_monitor.py
        monitor the accounts balance
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
        
        4. ".email_ding_contact.json"
         Create it manually when add a new task, ensure that task is same with "../task/*.py":
            {
                "task": {
                    "emaillist": "a@wanchain.org;b@wanchain.org",
                    "dingding": "ding_robot_api"
                },
                "EMAIL_REPORT_FROM_ADDRESS": "***@wanchain.org",
                "EMAIL_REPORT_SMTP_SERVER": "smtp.***.com"
            }
        
        5. ".stmp.pwd"
         Create it manually
    
        7. "evmChainCrossSc.json"
         Generate it from chainInfos.json
        
        8. ".foundation_accounts.csv"
         Create it mannually for "osm_account_balance_monitor"

        9. ".public_rpc.json"
         Create it for every chain 

## monitor_report
        to store the related reports
        Notice: 1. ensure the report name is unique; 
        2.Follow the format module_object_type_chain_content_monitor_jon_number.html


## utils
        Extend tools for monitor, how to extend?
        1. update  __init__.py
        2. update utils.py

## requiremens.txt
       https://learnpython.com/blog/python-requirements-file/
       create: pip freeze > requirements.txt
       install:pip install -r requirements.txt

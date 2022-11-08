'''
purpose:
To monitor the balance of related accounts for OpenStoreman
Steps:
1. get the accounts which need to be watched from config file
2. get the balance for every account
3. raise the alert when the balance is under threshold
'''
import json
import sys
sys.path.append('../')
import requests
import json
from utils import BalanceUtility
import pandas as pd
BalanceUtility.BalanceUtility().
class AccountBalance:
    def __init__(self):
        # init the variables
        ##rpcs
        with open('../config/.public_rpc.json','r') as f:
            self.rpc_config = json.load(f)
        ## the accouns for monitor
        self.accounts_info = pd.read_csv('../config/.foundation_accounts.csv')
        ## report format
        self.data = {'Net': [], 'Role': [], 'StoremanGroup': [], 'Account': [], 'Chain': [], 'Balance': [], 'Status': []}

    def get_accounts_balance(self):
        for i in range(len(self.accounts_info)):
            try:
                self.data['Net'].append(dic['Net'].values[i])
                self.data['Role'].append(dic['Role'].values[i])
                self.data['StoremanGroup'].append(dic['StoremanGroup'].values[i])
                self.data['Account'].append(dic['Address'].values[i])
                items = rpc.split('*')
                way = items[0]
                if way == 'web3':
                    node = items[1]
                    balance = getBalanceViaRPC(dic['Address'].values[i].lower(),node)/1000000000000000000
                elif way == 'tron3':
                    subCheck = items[1]
                    node = items[2]
                    if subCheck == 'balance':
                        balance = getTronAccBalance(dic['Address'].values[i],node)
                    elif subCheck == 'net':
                        balance = getTronAccAvailableNet(dic['Address'].values[i],node)
                    else:
                        balance = getTronAccAvailableEnergy(dic['Address'].values[i],node)
                if balance >= dic['Threshold'].values[i]:
                    status = 'OK'
                else:
                    status = 'Alert-Insufficient lower than {}'.format(dic['Threshold'].values[i])
            except:
                continue
            data['Chain'].append(dic['Chain'].values[i])
            data['Balance'].append(str(balance))
            data['Status'].append(status)
        return data

def main(net,job_num,report_path='../monitor_report'):
    '''
    :param net:
           job_num
           report_path
    :return:
            {
            "osm_account_healthy_xrp_trust_line_monitor": [
                {
                    "testnet_043": {
                        "account": "rsCWdxk6xpX6aydpYFw6tpNN574AX8RZ6C",
                        "account_lines": {
                            "rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ": "Xin"
                        },
                        "status": "pass"
                    }
                },
                {
                    "dev_092": {
                        "account": "rGcwUtTAyGw945aofyfaqdS6q5ujenrASD",
                        "account_lines": {
                            "rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ": "Xin"
                        },
                        "status": "pass"
                    }
                }
            ]
        }
    '''
    # it will not be watched in this list
    ignore_xrp_token = ['GZX:rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ',
                        '784249424C780000000000000000000000000000:rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ',
                        '584C495354000000000000000000000000000000:rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ',
                        'NVL:rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ']

    ignore_xrp_token = []
    result = {task:[]}
    html_json = {"StoremanGroup":[],"Account":[],"Account Lines":[],"Expected Account Lines":[],"Status":[]}
    #1. init acclines
    acclines = ACCLINES(net)
    #2. get working groups
    working_groups = acclines.get_working_grs()
    #3. check account lines
    for work_group in working_groups:
        group_name = utils.hex_string_convert.hexstring_to_string(work_group['groupId'][2::].lstrip('0'))
        if work_group['curve1'] == 0:
            xrp_pk = work_group['gpk1']
        else:
            xrp_pk = work_group['gpk2']
        account = utils.Gpk2XrpAddr.GPK2XRPADDRESS().genXrpAddr(xrp_pk)
        acc_line_set = acclines.check_trust_line_setting(account,ignore_xrp_token)
        result[task].append({group_name:acc_line_set})

    #4. generate html from html_json
    for data in result.get(task):
        group_name = list(data.keys())[0]
        html_json["StoremanGroup"].append(group_name)
        html_json["Account"].append(data[group_name]["account"])
        html_json["Account Lines"].append(data[group_name]["account_lines"])
        html_json["Expected Account Lines"].append(data[group_name]["expected_account_lines"])
        html_json["Status"].append(data[group_name]["status"])
    html_raw = utils.genhtml.html_build(html_json,task)
    html = utils.genhtml.render_new(html_raw,key= report_keyword)

    #5.output report
    with open(report_path+'/{}_{}_{}.html'.format(task,net,job_num),'a') as f:
        f.write(html)

    #6.send email
    attachment = '' #file
    utils.send_email(task,html,attachment)

    #7.send dingding msg
    msg = utils.dingMsg.msgFormat(task,html_json,fliter = report_keyword)
    url,mobile = utils.get_ding_url(task)
    utils.dingMsg.send_request(msg,url,mobile)

if __name__ == '__main__':
    import sys
    main(sys.argv[1],sys.argv[2],report_path=sys.argv[3]) #for jenkins deployment
    # main('test',8)




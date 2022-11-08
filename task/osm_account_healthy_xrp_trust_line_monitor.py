'''
purpose:
To monitor the trust lines for group
Steps:
1. get the groups to monitor
2. get the xrp_token tokenPairs, then check out the xrp token issuers for further use.
3. get the accout lines for group
4. compare the account lines with the token issuers in tokenPairs. expected that all token issuers should be set in account lines
'''
import json
import sys
sys.path.append('../')
import os
import xrpl.models
from utils import utils #import utils/utils.py
from xrpl.clients import WebsocketClient
task =os.path.basename(__file__).replace(".py","") #'osm_account_healthy_xrp_trust_line_monitor'
report_keyword = utils.get_report_keywords(task)
class ACCLINES:
    def __init__(self,net,chain='XRP',scheme='ws'):
        # init the variables
        self.net = net
        self.chain = chain
        self.scheme = scheme
        self.stm = utils.StoremanUtil(net).storeman_util()
        self.tokenPairs = utils.TokenPairUtil(net).token_util()
        self.rpc_selector = utils.RpcSelector(net,chain,scheme,utils.RpcSelect_obj().getXrpBlkNum)

    # define the functions
    def get_working_grs(self):
        '''
        get all working group's IDs
        :return:
        '''
        working_groups = self.stm.getWorkingGroupsDetails()
        return working_groups
    def get_token_issuers_from_tokenPairs(self):
        '''
        :return:{"Moo":"rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ"}
        '''
        xrptoken_infos = {}
        xrp_token_tokenpairs = self.tokenPairs.get_xrp_token_pairs()
        for xrp_token in xrp_token_tokenpairs:
            xrptokenInfo = utils.hex_string_convert.hexstring_to_string(xrp_token['fromAccount']).split(':') #{issuer}:${currency}
            xrptoken_infos[xrptokenInfo[1]] = xrptokenInfo[0]
        return xrptoken_infos
    def get_accout_lines(self,account):
        '''

        :param account:
        :return:
            {
                "status": "success",
                "result": {
                    "account": "rNWwzNesh85cVtVCSh2ipAHQQKDb3Q39o1",
                    "ledger_current_index": 31549231,
                    "lines": [
                        {
                            "account": "rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ",
                            "balance": "2",
                            "currency": "Moo",
                            "limit": "10000000000",
                            "limit_peer": "0",
                            "no_ripple": true,
                            "no_ripple_peer": false,
                            "quality_in": 0,
                            "quality_out": 0
                        }
                    ],
                    "validated": false
                },
                "id": "account_lines_457777",
                "type": "response"
            }
        '''
        rpc = self.rpc_selector.select_random()
        if not rpc:
            rpc = self.rpc_selector.select_best()
        websocket_client = WebsocketClient(rpc)
        websocket_client.open()
        request = xrpl.models.requests.account_lines.AccountLines(account=account)
        response = websocket_client.request(request).to_dict()
        websocket_client.close()
        return response
    def get_brief_account_lines(self,account_lines_raw):
        '''
        :param account_lines_raw, from the ledger rpc
        :return: {"Moo":"rDqaV8aoWPSqPGdy6iXLYzqeA1DEGMCrzJ"}
        '''
        account_lines = {}
        for account_line in account_lines_raw['result']['lines']:
            account_lines[account_line['currency']] = account_line['account']
        return account_lines
    def check_trust_line_setting(self,account,ignore_xrp_tokens):
        '''
        :param account:
        :param ignore_xrp_tokens->list, it will not be watched in this list
        :return:
            {"account":account,"account_lines":"issuer_a:currency_a\n issuer_b:currency_b"},"status":"pass"}
        '''
        status = "pass"
        account_expected_trust_lines = []
        account_setted_trust_lines = []
        miss_trust_line_set = []
        result = {"account":account,"expected_account_lines":"","account_lines":"","status":status}
        account_lines_raw = self.get_accout_lines(account)
        account_lines = self.get_brief_account_lines(account_lines_raw) #{currency:issuer}
        xrp_token_issuers = self.get_token_issuers_from_tokenPairs() #{currency:issuer}
        for currency, issuer in xrp_token_issuers.items():
            if "{}:{}".format(currency,issuer) not in ignore_xrp_tokens:
                account_expected_trust_lines.append("{}:{}".format(issuer,currency))
                if not account_lines.get(currency):
                    miss_trust_line_set.append({currency:issuer})
                else:
                    account_setted_trust_lines.append("{}:{}".format(issuer,currency))
        if miss_trust_line_set:
            status = "failed-trust_line_missing:\n"
            for xrp_token in miss_trust_line_set:
                status += '{}\n'.format(xrp_token)
        result["expected_account_lines"] = '\n'.join(account_expected_trust_lines)
        result["account_lines"] = '\n'.join(account_setted_trust_lines)
        result["status"] = status
        return result

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




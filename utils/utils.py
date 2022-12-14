import json
from utils import TokenPairsUtility,StoremanUtility,RpcProviderUtility,\
    hex_string_convert,dingMsg,sendEmail,genhtml
import random
from pubkey2address import Gpk2BtcAddr,Gpk2DotAddr,Gpk2XrpAddr #pip install pubkey2address

# load the config files
iWAN_config = '../config/.iWAN_config.json'
with open('../config/chainInfos.json','r') as f:
    chainInfo = json.load(f)
with open('../config/crossPoolTokenInfo.json','r') as f:
    crossPoolTokenInfo = json.load(f)
with open('../config/evmChainCrossSc.json','r') as f:
    evmChainCrossSc = json.load(f)
with open('../config/.public_rpc.json','r') as f:
    pub_rpc_dic = json.load(f)
with open('../config/.email_ding_contact.json','r') as f:
    email_ding_dic = json.load(f)
smtp_pwd = '../config/.smtp.pwd'

# load the utils
TokenUtil_obj = TokenPairsUtility.TokenPairsUtility
StoremanUtil_obj = StoremanUtility.StoremanUtility
RpcSelect_obj = RpcProviderUtility.PROVIDER_SELECTOR
SendEmail_obj = sendEmail.SendEmail

# init the utils for using
class TokenPairUtil():
    def __init__(self,net):
        self.net = net
    def token_util(self):
        return TokenUtil_obj(self.net,iWAN_config,chainInfo,crossPoolTokenInfo,evmChainCrossSc)

class StoremanUtil():
    def __init__(self,net):
        self.net = net
    def storeman_util(self):
        return StoremanUtil_obj(self.net, iWAN_config)

class RpcSelector():
    def __init__(self,net,chain,scheme,getBlockNum):
        '''
        :param chain: xrp
        :param getBlockNum: function, eg.RpcSelect_obj.getEvmBlkNum
        '''
        # print(pub_rpc_dic[net])
        self.rpcs = pub_rpc_dic[net][chain][scheme]
        self.getBlockNum = getBlockNum

    def select_random(self):
        rpc = random.choice(self.rpcs)
        if self.getBlockNum(rpc):
            return rpc

    def select_best(self):
        return RpcSelect_obj().select_best_provider(self.rpcs,self.getBlockNum)

def send_email(task,html,attachment):
    SendEmail_obj(smtp_pwd, email_ding_dic["EMAIL_REPORT_FROM_ADDRESS"], email_ding_dic["EMAIL_REPORT_SMTP_SERVER"],
                  email_ding_dic["SMTP_SERVER_PORT"]) \
        .send_email(task, html, email_ding_dic[task]['emaillist'], attachment)
def get_ding_url(task):
    dingInfo = email_ding_dic[task]['dingding']
    return dingInfo['url'], dingInfo['mobile']


def get_report_keywords(task):
    return email_ding_dic[task]['keyword']





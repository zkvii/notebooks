# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
import json
from hashlib import md5
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
# Set your own appid/appkey.
#config.json
"""
{
    "appid":"your appid",
    "appkey":"your appkey"
    "secret_id":"your secretid",
    "secret_key":"your secretkey"
}
    
"""
with open('./config.json') as f:
    conf=json.load(f)
    
appid = conf['appid']
appkey =conf['appkey'] 

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang = 'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

query = 'The body of Edwin Chiloba, a 25-year-old designer and model, was found on January 4 in a trunk on the side of the road in the Rift Valley in the west of the country.\n"According to our findings, he died as a result of asphyxiation caused by suffocation," Johansen Oduor told a press conference after the autopsy.'

# Generate salt and sign


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


salt = random.randint(32768, 65536)
sign = make_md5(appid + query + str(salt) + appkey)

# Build request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}


def translate(content):
    sign = make_md5(appid + content + str(salt) + appkey)
    payload = {'appid': appid, 'q': content, 'from': from_lang,
               'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()['trans_result']
    # Show response
    translated_ret = '\n'.join([ret['dst'] for ret in result])
    return translated_ret

def text_translate(content):

    cred = credential.Credential(conf['secret_id'], conf['secret_key'])
    # 实例化一个http选项，可选的，没有特殊需求可以跳过
    httpProfile = HttpProfile()
    httpProfile.endpoint = "tmt.tencentcloudapi.com"

    # 实例化一个client选项，可选的，没有特殊需求可以跳过
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    # 实例化要请求产品的client对象,clientProfile是可选的
    client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)

    # 实例化一个请求对象,每个接口都会对应一个request对象
    req = models.TextTranslateRequest()
    params = {
        "SourceText": f"{content}",
        "Source": "en",
        "Target": "zh",
        "ProjectId": 0
    }
    req.from_json_string(json.dumps(params))

    # 返回的resp是一个TextTranslateResponse的实例，与请求对象对应
    resp = client.TextTranslate(req)
    # 输出json格式的字符串回包
    # print(resp.to_json_string())
    return vars(resp)['TargetText']

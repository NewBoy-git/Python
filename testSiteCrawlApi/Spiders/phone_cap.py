
import requests
import json


def phone_search(phone):
    url = 'https://anquan.baidu.com/xiapi/api/v1/phone/query'
    data = {
    'search':phone,
    'request_page':'1',
    'position':'39.91488908|116.40387397',
    'data':'4c6ca00866fe9036555ef47a0b128d34e300f1a635a19baa5f29444d08ada1c7f38d8689be2c187cf6b8fc23634b2a59959d91dd37c59e961fb5f076c572e5b357cfbf91e2691c029f4d990e56a4d3a814ccf4817ff1175a54d3de91cbacd0199e181d677506f346332813e08ae061416cb80e65dbf0cb6f2ce66c0168f3ad22',
    'key_id':'14',
    'sign':'9eda435b',
    }


    headers = {
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection':'keep-alive',
    'Content-Length':'355',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'BAIDUID=58827D1A5FFF5A434FBD73C6CF5D7BCF:FG=1; PSTM=1559740841; BIDUPSID=F42DDDC4D2B56DE1BA22A6819EB27804; __cfduid=d119e902f044f4bb845b18d015aab5fe81564019992; BDSFRCVID=YC8sJeCCxG3jJX5wODTC-xJdNO2mbEdSFCee3J; H_BDCLCKID_SF=tRk8oKPyJKvbfP0k-nOKMJOH-UnLqb3KtT7Z0lOnMp05s-QpyRJcQ-C4Dh73Llopb6bX2-oVBtJPeIO_e6LbejoBjaDs-bbfHj6tWJj-HJOoDDk6DfO5y4LdLp7xJ-TZynTf2hbYyfnrHUI9jT5V-xLO0PjmK4LeWJLD_KIhJD--bP365ITa5tC_KmT22-us5jQlQhcH0hOWsIOFylAh5U4v32cBWq_DynkHWRoN5UOPEn5NDUC0Djb-DHDJtjnfb5kXQ458K4__Hn7zeprTebtpbtbmhU-e2eQv_43v3UbTKtn_bMTcD4uVQfOg0fJ-5R7ZVJO-KKCKhCP4DM5; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-%3A; BDUSS=JpQmFiYTZQcG41S3BEeG5-RmZrT0F3emlvaHJJbWU4LW1NUktrc0ExRmtKSHRkRVFBQUFBJCQAAAAAAAAAAAEAAACX6Ic70KHM0rrsb28AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGSXU11kl1NdcU; delPer=0; PSINO=2; userType=0; saasid=Flh5mzlfKbG1zB3mRG9jcDOvaosmOdzR4xEKTBFMkDympaOotmlSXQ%3D%3D; H_PS_PSSID=1459_21104_20698_29523_29520_29099_29567_28836_29221_29460_28701; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; Hm_lvt_bc03b77c07af0cbdcab6652e1d3f29a8=1565770027,1565776163; Hm_lpvt_bc03b77c07af0cbdcab6652e1d3f29a8=1565776163; CTOKEN=453ee08155bed8bee89eb6a15eda852e',
    'Host':'anquan.baidu.com',
    'Origin':'https://anquan.baidu.com',
    'Referer':'https://anquan.baidu.com/haoma/search?search=15578330927',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'same-origin',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'X-Requested-With':'XMLHttpRequest'
    }
    r = requests.post(url,data=data,headers=headers).text
    return r
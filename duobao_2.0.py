#encoding=utf8 
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')
import time
import requests
import  re
#1. 粘贴产品ID
#2. 输入预期价格  时间剩余2秒时 且  低于预期价格 开始加价
#3 输入cookie
ID = '114333533'    #产品id
my_price = 55           #预期价格
y = 1                   #加价幅度
s = 2                 #等待刷新时间

c = 'shshshfpb=0def37c482fc43f7643556ff541c84eeeabae5ec8258ab6a15b53d5d5a; shshshfpa=c62a0e3b-6bd7-ffea-58c7-6c0ce00e184d-1532740803; ipLocation=%u5c71%u897f; PCSYCityID=303; pinId=ORUTTcFI34MpSzusy67MfA; pin=7951183463; unick=%E9%99%88%E4%B8%80%E6%AF%9B; _tp=geU2G9t%2F69EjfzuLm3nslw%3D%3D; _pst=7951183463; cn=10; areaId=6; TrackID=1T3GbpM4f1AK78AMt5cs4rVASLO2VC7GsbPJ9lsN4EXZVxPhC9mu592tAb8foqJfikJtWk3ciGUoCE9LaPN903Wi6Df0t1-UPZ433-LS36RHp-tSQ1pLnQ_QDcTlkUEfK; ceshi3.com=201; unpl=V2_ZzNtbUAASh12DxNSeBsPV2IKFwpKXxMddw9OUXJMWVIzVEZYclRCFX0UR1FnGloUZAMZXEVcQBRFCEdkexhdBGYKGlRKVXMVcQ8oVRUZVQAJbRVaRVJCQXBfE1cpSllWYgoibUFXcxRFCEJWeBpfBG4KElRKUkMRcAlOU3IdXA1XMxJVRmdBEXUPT1Z5EF0HbjPF9OyBz7OhseyDyZtsAWEAFFlDVkIWRQl2VUtYMgJhBxdVQhpDEXcLRVd6EFUFbgsXXUZSQh1yAUJUcyldNWQ%3d; __jdv=122270672|www.linkstars.com|t_1000089893_156_0_184__66640e4fd2cb4b48|tuiguang|3f8926d723bc484f99a936948d4fefe4|1556370380492; mt_xid=V2_52007VwMWUF5bUVsWQBlVDWIDFldcUFVTG0kRbAUzUBcGXlhVRh1KSwgZYgESAkFQVggdVRleAmJURQBVDFIPTHkaXQVvHxNXQVtUSxxJEl0CbAASYl9oUWocSB9UAGIzElZc; ipLoc-djd=6-303-36783-36825; __jdu=15322208818941540968519; __tak=5a4ed200d389fb5785a0f1238bbb263e580cd4ce8eb27f5c265f8f4852f65974b76cf18e0790cefcddd942c82163160543bf54bf7cd7a5ab12cbdad5554aada57cba12951a41086cc9359ce143b1a705; 3AB9D23F7A4B3C9B=R3OTMZEY3BNY4ARXBTKF2LWK72DMJ7Q2C3DDDNZOZSSTNGQJEBJDBA4O437CSHCSRIYAPQ36NV7WGWNKIRB2KBOMCI; shshshfp=62b067bb6f5b1f5ebb6a731b1de11124; __jda=148612534.15322208818941540968519.1532220882.1556370380.1556412800.372; __jdc=148612534; thor=322D1EA65BDB142BB23D480A82BDFB63E572749C474C88302B690223361FBF0DB4B9C1A99E28D62EC3D0A346BD901889549AD6645E89689DF51259344820A3B10355F58E96B03EEA8A6C71362545F26AA038772E944179E879856117A0D1E50F4AA04BF4351D8FDFFAA7E4B22C34D9BCE0FD660FA20BF78EE32D70BDDCDBB841E8CA600F898D5D460C902A24295D30ED; __jdb=148612534.128.15322208818941540968519|372.1556412800'
#设置上面即可


HEADERS = {
    'Referer':'https://paipai.jd.com/auction-detail/113158389',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Cookie':'coo'
}
HEADERS['Cookie'] = c
url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'


#获取当前价格&剩余时间
def get_pricetime():
    r_url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'
    r = requests.get(r_url,headers=HEADERS)
    p_url = 'https://used-api.jd.com/auctionRecord/getCurrentAndOfferNum?auctionId=' + ID +'&callback=__jp17'
    p = requests.get(p_url,headers=HEADERS)
    cur_price = re.findall(r"currentPrice\":(.+?),",p.text)
    c_time = re.findall(r"currentTime\":\"(.+?)\"",r.text)
    e_time = re.findall(r"endTime\":(.+?),",r.text)
    cur_price = ''.join(cur_price)
    c_time = ''.join(c_time)
    e_time = ''.join(e_time)
    c_time = (float(e_time) - float(c_time))/1000   #计算剩余时间并换算成秒
    name = re.findall(r"model\":\"(.+?)\",",r.text)
    coloer = re.findall(r"quality\":\"(.+?)\",",r.text)
    #print(name + coloer ,end='')
    return cur_price,str(c_time)
#下单

def buy(price):
    # price = int(price)
    # buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice?auctionId='+ ID + '&price='+ str(price)  +'&callback=__jp24'
    # bib = requests.get(buy_url,headers=HEADERS)
    # print(bib.text)
    buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice'
    data = {
        'trackId': '3b154f3a78a78f8b6c2eea5a3cee5674',
        'eid': 'UTT4AVFUIZFVD6KGHHJRAGEEGFJ4MWFSOPDUEF7KBEHDA5ODK3GKDKP5PCVTWIAQ32N2ZT2AR5YBAH3T27354OAI3Q',
             
    }
    data['price'] = str(int(price))
    data['auctionId'] = str(ID)
    #print(data)
    resp = requests.post(buy_url,headers=HEADERS,data=data)
    print(resp.json())

try:
    while True:
        p = get_pricetime()
        print('编号:'+ID + ',当前的价格是:' + p[0] + '剩余时间' + p[1] + ',预期价格:' + str(my_price) )
        x = p[0]
        x = float(x)
        tt = p[1]
        tt = float(tt)
        if  x <= my_price  and tt <= 1:
            print('开始加价: 加价金额为' + str(x + y))
            buy(x + y)
        if tt < 6 and s != 0.0002:
            s = 0.0002
            print('开始加速 ' + str(s))
        time.sleep(s)    #等待刷新时间
        if tt < -1 :
            print('程序结束')
            break
except KeyboardInterrupt:
    print('已停止')

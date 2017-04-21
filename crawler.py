from timeit import default_timer as timer
import urllib.request
import urllib.parse
import json, re

########## Functions ##########
def makeRequest(url):
    accept = ""
    cookie = "Language=undefined; Language_Version=20160720"
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
    req.add_header('Referer', 'http://ebus.tycg.gov.tw/Taoyuan/Dybus.aspx')
    req.add_header('Accept-Language', 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4')
    req.add_header('Accept-Encoding', 'gzip, deflate, sdch')
    if sessionId=="":
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    else:    
        cookie += '; ASP.NET_SessionId='+sessionId
        accept = '*/*'
    req.add_header('Cookie', cookie)        
    req.add_header('Accept', accept)
    return req
####################
def httpRequest(lang, goBack, line):
    params = urllib.parse.urlencode({'GoBack': goBack, 'Lang': lang, 'Line': line, 'Mode':2})
    url = "http://ebus.tycg.gov.tw/Taoyuan/API/BusXMLLine_close.aspx?%s" % params
    stops_name = []
    with urllib.request.urlopen(makeRequest(url)) as f:
        try:
            routes_data = re.search('.+\s+?(?=\<!DOCTYPE html\>)',f.read().decode('utf-8')).group(0).strip().split('|')
            for route_data in routes_data:
                stop = {}
                route = route_data.split(',')
                if re.match("^[1-9]\d?$", route[0]) is not None:
                    stop['id'] = route[0]
                    stop['name'] = route[2]
                    stops_name.append(stop)
        except:
            print("the session id may expired")
    return stops_name
####################
def downloadData(goOrBack, line):
    ## get en/zh stops than return combined result
    enStops = httpRequest("En", goOrBack, line)
    zhStops = httpRequest("Cht", goOrBack, line)
    return parseStops(enStops, zhStops)
####################
def parseStops(en, zh):
    stopOfRoute = []
    for i in range(0, len(zh), 1):
        if en[i]['id'] == zh[i]['id']:
            stop = {}
            stop['sequence']=zh[i]['id']
            stop['en']=en[i]['name']
            stop['zh']=zh[i]['name']
            stopOfRoute.append(stop)
    return stopOfRoute
########## main thread ##########
start = timer()
sessionId = ""
stopOfRoute = []
url = "http://ebus.tycg.gov.tw/Taoyuan/Dybus.aspx"
## get session id first
if sessionId == "":
    with urllib.request.urlopen(makeRequest(url)) as f:
        sessionId = re.search('(?<=ASP.NET_SessionId=)\w+',f.info()['Set-Cookie']).group(0)
        print("ASP.NET_SessionId: "+sessionId)

## read bus lines
with open('all_routes.json', 'r', encoding='utf8') as routes_file:
    line_data = json.loads(routes_file.read())
    for line in line_data['bus']:
        print("download stops of %s" % line)
        stopofroute = {}
        goRoute = downloadData(1, line)
        backRoute = downloadData(2, line)
        stopofroute['id'] = line
        if (len(goRoute))>0:
            stopofroute['goRoute'] = goRoute       
        if (len(backRoute))>0:
            stopofroute['backRoute'] = backRoute    
        stopOfRoute.append(stopofroute)

with open('taoyuan_stopOfRoute.json', 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(stopOfRoute, ensure_ascii=False))
end = timer()
print("===output taoyuan_stopOfRoute.json, elapsed time: %s seconds==="%int(end - start))
    	



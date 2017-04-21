桃園市公車中英文路線與站牌資料
===================

資料來源為[桃園市公車動態資訊系統](http://ebus.tycg.gov.tw/Taoyuan/Dybus.aspx)，透過 [Tamper](https://chrome.google.com/webstore/detail/tamper-chrome-extension/hifhgpdkfodlpnlmlnmhchnkepplebkb) 取得 API ，再利用 Python 開發，將資料輸出成 JSON 格式。

----------

用法
-------------
Python 3+ 的環境下，執行以下指令

    $ python crawler.py

會先讀取同目錄下的 **all_routes.json**，執行成功後會在該目錄產生 **taoyuan_stopOfRoute.json** 檔案

輸出格式
-------------

    taoyuan_stopOfRoute.json{     
	    id(string): 路線識別代碼,
        goRoute(stops): 去程所有經過站牌,
        backRoute(stops): 返程所有經過站牌
    }
    stops{ 	
	    sequence(string): 路線經過站牌之順序,
        en(string): 中文繁體名稱,
        zh(string): 英文名稱  
    }
####單向路線    
以下路線(id)為單向路線，只有去程

 - 112 
 - 3260 
 - 3520 
 - 3510 
 - 3282 
 - 3281 
 - 7062 
 - 50991 
 - 51061 
 - 51062 
 - 51071 
 - 51072 
 - 51073
 - 51091 
 - 8020 
 - 8030 
 - 8000 
 - 8010 
 - 8090 
 - 8080 
 - 8070 
 - 8060 
 - 8120 
 - 8110 
 - 8100 
 - 8050
 - 8040 
 - 6500 
 - 6510 
 - 6520 
 - 6530 
 - 6540 
 - 6550 
 - 6560 
 - 6580 
 - 6720 
 - 6710 
 - 6740 
 - 6730 
 - 6760
 - 6750 
 - 6770 
 - 6780 
 - 36510 
 - 36520 
 - 36530 
 - 36540

關於
-------------
相比於高雄市的站牌路線資料，在開發桃園市資料爬蟲中花費較久時間，首先網頁使用了 Session ，因此在第一次連接時需要將伺服器回傳的 id 存起來，然後每次送要求時夾帶在表頭之中，其次是伺服器回傳沒有特定格式，像是一串字串並透過逗號與垂直條( "|" )來分隔，最後是路線選取的部分以下拉式選單來使用，因此我就直接從原始碼複製路線選單中的選項。

相關專案
-------------
####[高雄市中英文公車路線與站牌資料](https://github.com/mattlin4567/Kaohsiung-bus-opendata)

Licience
-------------
MIT
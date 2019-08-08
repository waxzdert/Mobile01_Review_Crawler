# Mobile01 回覆抓取爬蟲

[Mobile01](https://www.mobile01.com/)簡單的回覆抓取爬蟲

### 執行環境

- Windows 10 Home
- Anaconda (Python 3.7 version)

### 使用前準備

0. 安裝[Anaconda (Python 3.7版本)](https://repo.anaconda.com/archive/Anaconda3-2019.07-Windows-x86_64.exe)，在安裝過程中請將Anaconda加入環境變數PATH裡面，在安裝過程中可以在Advanced Options當中勾選。

1.  執行命令提示字元(cmd.exe)輸入並執行 ```activate base```

2.  輸入並執行 ```pip install requests```
   
3.  輸入並執行 ```pip install beautifulsoup4```
   
4.  進到存放Mobile01_Review_Crawler.py爬蟲的資料夾，新增一個文字文件
5.  打開文字文件並將想要爬取的文章頁面網址貼入文字文件中，輸入完第一個網址後要換行
   
    像是以下這樣

    https://www.mobile01.com/topicdetail.php?f=568&t=5864034
    https://www.mobile01.com/topicdetail.php?f=568&t=5866129

    輸入完後存檔

6.  按住shift鍵並按滑鼠右鍵開啟選單，點選在這裡開啟命令提示字元或在這裡開啟PowerShell視窗

7.  輸入並執行 ```activate base```
   
8.  輸入並執行 ```python Mobile01_Review_Crawler.py```

9.  輸入想抓取回覆的天數(例如:5)，並按下Enter
    
10. 輸入要讀取的檔案名稱(例如:Samsung.txt)，並按下Enter
    
11. 耐心等待抓取
    
12. 輸入輸出Excel的檔名

----

如果你遇到其他問題可以[email](mailto:waxzdert16@gmail.com)給我，或是可以再Github上提出issue。






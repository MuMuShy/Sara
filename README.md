# Sara
個人語音助理
持續開發中
使用方法: 目錄下 python3 Sara.py

目前功能(指令):
時間,爬取學校最新公告,天氣

如何使用:執行檔->利用txt裡面的下載連結下載檔案 解壓縮後執行Sara.exe
可利用輸入區域輸入你的指令,或是按下說話按鈕然後說出你要與Sara說的話

如何開發Sara功能:
我們定義好與Sara的接口(SaraModules,Sara指令表)
 1.直接撰寫module 範例(SaraModules/SaraWeb.py)即是一個簡單的python開啟網頁的功能 撰寫好後將檔案放入SaraModules                        下資料夾下,並將模組名稱加入(SaraModules/__init.py__) 打開此檔案會看到__all__=[] 請將你的模組名稱加入進來(參                        考"SaraWeb") Sara就會在執行時Import你的模組
 2.將你的指令加入指令表(Sara指令表/Sara指令表.xlsx)是一個excel檔裡面放置了Sara聽到什麼關鍵指令要去執行你的模組功                        能,格式為[指令關鍵字,模組名稱,函式名稱,CallBack] 依序為 '使用者說到什麼要執行','要執行的函示名稱','回傳語句(                        就是讓Sara講這個功能執行完要說什麼簡單的讓使用者知道他要求的指令已完成)
              

# pttNotice

使用 Python3 爬取 ptt.cc/bbs 中之板塊後，使用 Line Notify 發送通知至使用者、群組，

須搭配 Crontab 定期爬取 PTT，

開發原意是為了爬 SOHO 板看有沒有打工的機會而隨便寫的（後來發現早一點知道也沒什麼用，雇主也不會因為你先搶就先贏XD）

**因範例為八卦板，請注意會有被廢文洗板的風險**

## 使用說明

請先到 [Line Notify](https://notify-bot.line.me/zh_TW/) 註冊一個自己的 Token，選擇你要的群組、自己，就可以使用這組 Token 把訊息送到你想要的地方。

*Ref: [使用 Python 實作發送 LINE Notify 訊息](https://bustlec.github.io/note/2018/07/10/line-notify-using-python/)*

## 程式原理

1. 這隻程式會先爬目前該板最新頁面、上一頁的所有文章，儲存成 `posts.json`，因第一次執行，所以會把這些內容送到 Line Notify，並把已送出通知的文章之 網址存在 `sents.json`，在送出前會再次確認 `sents.json` 是否有曾經送過，如有送過就不寄出通知

2. 下次執行時，會比較目前爬到的內容是否存在於 `posts.json`，如果是新的內容，就寄送通知，並紀錄已送出的通知

## 執行結果

**八卦板廢文真的很多，請小心不要炸到別人的群組**

![](https://i.imgur.com/UayoSMx.png)


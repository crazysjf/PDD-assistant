# 传商品：goods_uploader.py

从拼多多和淘宝中导出商品资料放入一个文件夹:

拼多多超级店长:商品导出 => 导出SPU => 选在售中商品,勾选商品编码
淘宝超级店长:宝贝管理 => 导出，注意勾选商家编码

执行goods_uploader.py，文件夹名称作为参数。




# 白底图下载：wbg_downloader.py
- 用调试模式运行chrome：
 chrome.exe --remote-debugging-port=9233 --user-data-dir=remote-profile
 注意要在固定的目录下执行该命令。remote-profile会创建在当前目录下，这样收藏夹这些可以重复使用。


 - 运行wbg_downloader
 - 登录拼多多后台

import sys
import requests
import threading
import datetime
import easygui

url = 0
num_thread = 0


def Handler(start, end, url, filename):
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    r = requests.get(url, headers=headers, stream=True,timeout=5)
    # 写入文件对应位置
    with open(filename, "r+b") as fp:
        fp.seek(start)
        var = fp.tell()
        fp.write(r.content)
def download_file(url, num_thread = 16):
    r = requests.head(url)
    try:
        file_name = url.split('/')[-1]
        file_size = int(r.headers['content-length'])   # Content-Length获得文件主体的大小，当http服务器使用Connection:keep-alive时，不支持Content-Length
    except SyntaxError:
        return "Error #1:Syntax Error"
    except ImportError:
        return "Error #2:ImportError:If You Are Using Source Code,Please Check The Libs Are Installer"
    except PermissionError:
        return "Error#Important0x0:PremissionError:Are You Trying To Run It In Root?(windows:C:/,linux/mac:~/)"
    #  创建一个和要下载文件一样大小的文件
    fp = open(file_name, "wb")
    fp.truncate(file_size)
    fp.close()
    # 启动多线程写文件
    part = file_size // num_thread
    # 如果不能整除，最后一块应该多几个字节
    for i in range(num_thread):
        start = part * i
        if i == num_thread - 1:   # 最后一块
            end = file_size
        else:
            end = start + part
        t = threading.Thread(target=Handler, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
        t.setDaemon(True)
        t.start()
    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s 下载完成' % file_name)
if __name__ == '__main__':
    mainbox = easygui.buttonbox("Welcome To PythonMTDownloader",choices=['Start Downloading','About'])
    if mainbox == 'Start Downloading':
        url = easygui.enterbox("Download:")
        num_thread = easygui.integerbox("Thread:")
    else:
        easygui.msgbox("""About
Python Mutithread Downloader Alpha v1.0.2 .replaced-ver
By Richmind Coding Club""")
    start = datetime.datetime.now().replace(microsecond=0)
    download_file(url,num_thread)
    end = datetime.datetime.now().replace(microsecond=0)
    print("用时: ", end='')
    print(end-start)

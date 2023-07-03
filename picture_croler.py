import requests
import sys
import os
import urllib.request as req
import asyncio
import threading
import numpy as np

try:
    raw_url = sys.argv[1]
    path = sys.argv[2]
    savename = sys.argv[3]
    threds = sys.argv[4]
except:
    raw_url = None
    path = None
    savename = None
    thread = None

url = []
imgurl = []
pixiv_list = []
source_list = []
plist_count = 0

complited_files = 0

'''
raw_url = "./url.txt"
path = "./"
savename = "test"
'''

pixiv_headers = [
    ('authority', 'i.pximg.net'),
    ('accept', 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'),
    ('accept-language', 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'),
    ('cache-control', 'no-cache'),
    ('pragma', 'no-cache'),
    ('referer', 'https://www.pixiv.net/'),
    ('sec-ch-ua', '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"'),
    ('sec-ch-ua-mobile', '?0'),
    ('sec-ch-ua-platform', '"Windows"'),
    ('sec-fetch-dest', 'image'),
    ('sec-fetch-mode', 'no-cors'),
    ('sec-fetch-site', 'cross-site'),
    ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')
]

gal_headers = [
    ('authority', 'img3.gelbooru.com'),
    ('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'),
    ('accept-language', 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5'),
    ('cache-control', 'no-cache'),
    ('pragma', 'no-cache'),
    ('sec-ch-ua', '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"'),
    ('sec-ch-ua-mobile', '?0'),
    ('sec-ch-ua-platform', '"Windows"'),
    ('sec-fetch-dest', 'document'),
    ('sec-fetch-mode', 'navigate'),
    ('sec-fetch-site', 'none'),
    ('sec-fetch-user', '?1'),
    ('upgrade-insecure-requests', '1'),
    ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'),
]   
#전체적인 실행방식
#URL, 저장위치, 스레드, 이름을 지정하고, 지정한 폴더내에 사진들과 소스를 저장한다.
#수정사항: URL 가공과 스레트방식 추가 -작업착수, 다운로드 스레드 지정 -완료

class main():

    def download(self,path,name,url,axis,num_sync,taskid):
        num = 0 #일러스트 번호
        row = 0 #리스트 열

        for i in range(len(url[axis])):
            spath_png = str(path+"/"+name+"/"+name+f" ({(num_sync*axis)+(num+1)})"+".png").replace("//" , "/")
            spath_jpg = str(path+"/"+name+"/"+name+f" ({(num_sync*axis)+(num+1)})"+".jpg").replace("//" , "/")
            spath_none = str(path+"/"+name+"/"+name+f" ({(num_sync*axis)+(num+1)})").replace("//" , "/")
            #이미지 확장자 프리셋

            if "https://cdn.donmai.us" in url[axis][row]:
                try:
                    req.urlretrieve(url[axis][row], spath_jpg)
                    print(f"Downloaded image from task{taskid} : {spath_jpg}")
                except:
                    x = url[axis][row].replace(".jpg", ".png")
                    req.urlretrieve(x, spath_png)
                    print(f"Downloaded image from task{taskid} : {spath_png}")
            if "https://i.pximg.net" in url[axis][row]: #픽시브 일러스트 리스트쪽에 문제있음. 고처야함
                try:
                    opener = req.build_opener()
                    opener.addheaders = pixiv_headers
                    req.install_opener(opener) #헤터추가, 403 Forbidden 우회용.
                    req.urlretrieve(url[axis][row], spath_jpg)
                    print(f"Downloaded image from task{taskid} : {spath_jpg}")
                except:
                    x = url[axis][row].replace(".jpg", ".png")
                    opener = req.build_opener()
                    opener.addheaders = pixiv_headers
                    req.install_opener(opener) #헤터추가, 403 Forbidden 우회용.
                    req.urlretrieve(x, spath_png)
                    print(f"Downloaded image from task{taskid} : {spath_png}")
            if "https://img3.gelbooru.com/" in url[axis][row]:
                    opener = req.build_opener()
                    opener.addheaders = gal_headers
                    req.install_opener(opener) #헤터추가, 403 Forbidden 우회용.
                    first = url[axis][row].find(".jpg")
                    try:
                        req.urlretrieve(url[axis][row], spath_jpg)
                        print(f"Downloaded image from task{taskid} : {spath_jpg}")
                    except:
                        try:
                            url[axis][row] = url[axis][row][0:first]+".jpeg"
                            req.urlretrieve(url[axis][row], spath_none+".jpeg")
                            print(f"Downloaded image from task{taskid} : {spath_none}"+".jpeg")
                        except:
                            
                            url[axis][row] = url[axis][row][0:first]+".png"
                            req.urlretrieve(url[axis][row], spath_none+".png")
                            print(f"Downloaded image from task{taskid} : {spath_none}"+".png")
            num = num + 1
            row += 1
            #await asyncio.sleep(0.1)

    def sync_download(self,thread):
        global imgurl

        #np.array를 사용해서 스레드 수만큼 URL을 나누고, 만약 남는 URL이 있다면 그 URL는 따로 뺴둔 상태로 지정후 뒤에서부터 추가
        if len(imgurl)%thread == 0:
            sync_url = np.array(imgurl).reshape((thread, int(len(imgurl)/thread)))
            sync_url = sync_url.tolist()
        else:
            temp = []
            for i in range(len(imgurl)%thread):
                temp.append(imgurl.pop()) #남는 URL 빼두는 과정
            sync_url = np.array(imgurl).reshape((thread, int(len(imgurl)/thread)))
            sync_url = sync_url.tolist()
            for i in range(len(temp)):
                sync_url[thread-(i+1)].append(temp.pop()) #남는 URL 추가.
            
            #다운로드 시작
            print("\n\n################ download start! ################")

            #download_new(self,path,name,url,axis,thread,taskid)
            task = []
            for i in range(thread):
                task.append(threading.Thread(target=self.download, args=(path, savename, sync_url, i, len(sync_url[0]), 0+i)))
                task[i].start()
        
    def getdanimg(self,url):
        r = requests.get(url)
        cont = str(r.content)
        first = cont.find("image-container")
        first = cont.find("<picture>",first)
        last = cont.find("</picture>",first)
        cont = cont[first:last]
        first = cont.find("src=")
        last = cont.find("\">\\n", first)
        cont = cont[first:last]
        cont = cont.replace("src=\"","")
        cont = cont.replace("/sample/","/original/")
        cont = cont.replace("sample-","")
        
        if cont.find("https://") == -1:
            print("somthing wen't wrong, error in " + url)
        else:
            print(cont)
        return cont
    
    def getpixivimg(self,url):
        global plist_count
        r = requests.get(url)
        x = str(r.content)

        first = x.find("https://i.pximg.net/img-master/")
        if first == -1:
            first = x.find("https://i.pximg.net/c/250x250_80_a2")
            last = x.find("square1200.jpg", first)+14
            x = x[first:last].replace("c/250x250_80_a2/", "").replace("square", "master")
            print(x)
            return x
        else:
            last  = x.find(".jpg", first)
            x = x[first:last+4]
            
            if x.find("https://") == -1:
                print("somthing wen't wrong, error in " + url)
            else:
                print(x)
            return x

    def getgalimg(self,url):
        global source_list
        r = requests.get(url)
        x = str(r.content)

        #소스 출력, 이거를 txt로 저장
        get_source_start = x.find("Source: <a href=\"")
        get_source_end = x.find("\" rel=\"")
        get_source = x[get_source_start+17:get_source_end]
        if (get_source.find("https://") > 1) | (get_source.find("http://") > 1):
            print("\nSomething went wrong..... log:\n***************************************\n"+get_source+"\n************************************\n") 
        else:
            print("\n"+get_source)
            source_list.append(get_source)


        first = x.find("<picture>")
        last = x.find("</picture>",first)
        x = x[first:last]

        first = x.find("https://img3.gelbooru.com//images/")

        if first == -1:
            first = x.find("https://img3.gelbooru.com//samples/")
            last = x.find("jpg" , first)
            
            if last == -1:
                last = x.find("jpeg", first)
                img = x[first:last+4]

                img = img.replace("/samples/","images/")
                img = img.replace("sample_","")
            else:
                img = x[first:last+3]

                img = img.replace("/samples/","images/")
                img = img.replace("sample_","")

        else:
            last = x.find("jpg" , first)
            if last == -1 or last > first+100:
                last = x.find("jpeg", first, first+100)
                img = x[first:last+4].replace("//imag", "/imag")
                if last == -1 or last > first+100:
                    last = x.find("png", first, first+100)
                    img = x[first:last+3].replace("//imag", "/imag")
            else:
                img = x[first:last+3].replace("//imag", "/imag")
    
        if img.find("https://") == -1:
            print("somthing wen't wrong, error in " + url)
        else:
            print(img)
        return img

    
    def coverturl(self,path):   
        global url 
        n = 0
        with open(path) as f:
            url = f.read()
            url = url.split("\n")
            if url[len(url)-1] == "":
                del url[len(url)-1]

    def __init__(self):
        global raw_url
        global path
        global savename
        global thread
        global source_list
        
        if raw_url == None:
            while True:
                raw_url = input("url txt path : ")
                if raw_url.endswith(".txt") == True:
                    break
        if path == None:
            path = input("save path : ")
            if path != path.endswith("/"):
                path += "/"
            if os.path.isdir(path) == False:
                os.mkdir(path.replace("/", ""))
            if path != path.find("/", len(path)-1):
                path = path+"/"
        if savename == None:
            savename = input("save name : ")
        if thread == None:
            thread = int(input("threds (defalt:3) : "))


        os.makedirs(path+"/"+savename, exist_ok=True)
        self.coverturl(raw_url)

        for i in range(len(url)):

            if "https://danbooru.donmai.us/" in url[i]:
                imgurl.append(self.getdanimg(url[i]))

            if "https://www.pixiv.net/" in url[i]:
                imgurl.append(self.getpixivimg(url[i]))

            if "https://gelbooru.com/" in url[i]:
                imgurl.append(self.getgalimg(url[i]))

            
        with open(f"{path}/{savename}/source.txt", "w", encoding="utf8") as f:
            for i in range(len(source_list)):
                f.write(f"{source_list[i]}\n")

        t = threading.Thread(target=self.sync_download, args=(thread,))
        t.start()
        while True:
            if t.is_alive() == False:
                print("done!")
                break
            
main()
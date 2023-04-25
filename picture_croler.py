import requests
import sys
import os
import urllib.request as req
import asyncio

try:
    raw_url = sys.argv[1]
    path = sys.argv[2]
    savename = sys.argv[3]
    threds = sys.argv[4]
except:
    raw_url = None
    path = None
    savename = None
    threds = 3

url = []
imgurl = []
pixiv_list = []
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


class main():
    async def download(self,path,name,url,i,taskid,start_num):
        num = start_num
        global complited_files
        
        spath_png = str(path+"/"+name+"/"+name+f" ({num+1})"+".png").replace("//" , "/")
        spath_jpg = str(path+"/"+name+"/"+name+f" ({num+1})"+".jpg").replace("//" , "/")
        spath_none = str(path+"/"+name+"/"+name+f" ({num+1})").replace("//" , "/")
        
        if "https://cdn.donmai.us" in url[i]:
            try:
                req.urlretrieve(url[i], spath_jpg)
                print(f"Downloaded image from task{taskid} : {spath_jpg}")
            except:
                x = url[i].replace(".jpg", ".png")
                req.urlretrieve(x, spath_png)
                print(f"Downloaded image from task{taskid} : {spath_png}")
        if "https://i.pximg.net" in url[i]:
            try:
                opener = req.build_opener()
                opener.addheaders = pixiv_headers
                req.install_opener(opener)
                req.urlretrieve(url[i], spath_jpg)
                print(f"Downloaded image from task{taskid} : {spath_jpg}")
            except:
                x = url[i].replace(".jpg", ".png")
                opener = req.build_opener()
                opener.addheaders = pixiv_headers
                req.install_opener(opener)
                req.urlretrieve(x, spath_png)
                print(f"Downloaded image from task{taskid} : {spath_png}")
        if "https://img3.gelbooru.com/" in url[i]:
                opener = req.build_opener()
                opener.addheaders = gal_headers
                req.install_opener(opener)
                first = url[i].find(".jpg")
                try:
                    req.urlretrieve(url[i], spath_jpg)
                    print(f"Downloaded image from task{taskid} : {spath_jpg}")
                except:
                    try:
                        url[i] = url[i][0:first]+".jpeg"
                        req.urlretrieve(url[i], spath_none+".jpeg")
                        print(f"Downloaded image from task{taskid} : {spath_none}"+".jpeg")
                    except:
                        
                        url[i] = url[i][0:first]+".png"
                        req.urlretrieve(url[i], spath_none+".png")
                        print(f"Downloaded image from task{taskid} : {spath_none}"+".png")
        num = num + 1


    async def sync_download(self):
        global imgurl
        lefted = None

        if len(imgurl) >= 3:
            if len(imgurl) % 3 == 0:

                url_length = len(imgurl)
                amount = int(url_length / 3)
                sync_url_1 = []
                sync_url_2 = []
                sync_url_3 = []

                for i in range(int(url_length / 3)):
                    sync_url_1.append(imgurl[i])

                for i in range(int(url_length / 3)):
                    sync_url_2.append(imgurl[i+int(url_length / 3)])

                for i in range(int((url_length / 3))):
                    sync_url_3.append(imgurl[i+int(url_length / 3)*2])

            else:
                lefted = len(imgurl) % 3
                url_length = len(imgurl) - lefted
                amount = int(url_length / 3)
                sync_url_1 = []
                sync_url_2 = []
                sync_url_3 = []

                for i in range(int(url_length / 3)):
                    sync_url_1.append(imgurl[i])

                for i in range(int(url_length / 3)):
                    sync_url_2.append(imgurl[i+int(url_length / 3)])

                for i in range(int((url_length / 3)+lefted)):
                    sync_url_3.append(imgurl[i+int(url_length / 3)*2])

        

            print("\n\n################ download start! ################")

            for i in range(amount):
                task1 = asyncio.create_task(self.download(path, savename, sync_url_1, i, '1', 0+i))
                task2 = asyncio.create_task(self.download(path, savename, sync_url_2, i, '2', len(sync_url_2)+i))
                task3 = asyncio.create_task(self.download(path, savename, sync_url_3, i, '3', len(sync_url_2)*2+i))

                await asyncio.gather(task1,task2,task3)
            if lefted != None:
                for i in range((len(sync_url_3)-amount)):
                    task3 = asyncio.create_task(self.download(path, savename, sync_url_3, i, '3', len(sync_url_2)*3))
                    await task3

        else:
            print("\n\n################ download start! ################")
            task1 = asyncio.create_task(self.download(path, savename, imgurl, 0))
            await task1

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
        r = requests.get(url)
        x = str(r.content)

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
        
        if raw_url == None:
            while True:
                raw_url = input("url txt path : ")
                if ".txt" in raw_url:
                    break
        if path == None:
            path = input("save path : ")
        if savename == None:
            savename = input("save name : ")
        if threds == None:
            threds = input("threds (defalt:3) : ")
        


        os.makedirs(path+"/"+savename, exist_ok=True)
        self.coverturl(raw_url)

        for i in range(len(url)):

            if "https://danbooru.donmai.us/" in url[i]:
                imgurl.append(self.getdanimg(url[i]))

            if "https://www.pixiv.net/" in url[i]:
                imgurl.append(self.getpixivimg(url[i]))

            if "https://gelbooru.com/" in url[i]:
                imgurl.append(self.getgalimg(url[i]))

        asyncio.run(self.sync_download())
        print("done!")
            
main()
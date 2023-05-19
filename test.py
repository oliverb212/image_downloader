import numpy as np
import asyncio
imgurl = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
threds = 5
def sync_download_new():
    global imgurl
    if len(imgurl)%threds == 0:
        sync_url = np.array(imgurl).reshape((threds, int(len(imgurl)/threds)))
    else:
        temp = []
        for i in range(len(imgurl)%threds):
            temp.append(imgurl.pop())
        sync_url = np.array(imgurl).reshape((threds, int(len(imgurl)/threds)))
    sync_url = sync_url.tolist()
    for i in range(len(temp)):
        sync_url[threds-(i+1)].append(temp.pop())
    return sync_url


async def test():
    print("Testing")

a = [asyncio.create_task(test()), asyncio.create_task(test()), asyncio.create_task(test())]

asyncio.gather(a)

print(a)

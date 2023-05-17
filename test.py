import numpy as np

imgurl = [1,2,3,4,5,6,7,8,9,10]
threds = 5
def sync_download_new():
    global imgurl
    lefted = None
    sync_url = []

    thread_to_url_amt = (len(imgurl)/threds)
    if len(imgurl) % threds == 0:
        for i in range(threds):
            for q in range(int(thread_to_url_amt)):
                np.append(sync_url, imgurl[q+(threds*i)], axis=0)

    return sync_url
        
a = sync_download_new()

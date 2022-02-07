import json, m3u8, requests, os
def __write(url,title,seg,psk=None):
    path = 'music'
    try:
        os.mkdir(path)
    except OSError as error:
        pass 
    
    l = len(seg)
    with open(f"music\{title}.mp3","wb") as f:
        print(f"Downloading: {title}\n")
        for i,seg in enumerate(seg):
            if psk is not None:
                seg_url = f'{url}320/{seg["uri"]}?{psk}'
            else:
                seg_url = f'{url}{seg["uri"]}'
                
            seg_req = requests.get(seg_url).content
            f.write(seg_req)
            print(f"\033[ADownloaded {round((i+1)/l*100)}%")
            
    return "ok", 200

def wynk(main_url):
    url, policy_sig_keypair = main_url.split("32/index.m3u8?")
    songId = url.split("/")[4]
    songInfo = requests.get(f"https://content.wynk.in/music/v3/content?id={songId}&type=SONG").json()

    title = f'{songInfo["title"]}'.replace("\"","").replace(' ','_')

    index_res =  requests.get(url+"320/index.m3u8?"+policy_sig_keypair)

    m3u8_index = m3u8.loads(index_res.text)
    seg = m3u8_index.data["segments"]
    
    return __write(url,title,seg,psk=policy_sig_keypair)
    
    

def gaana(main_url,title="song"):
    url = main_url.split("index.m3u8")[0]
    res = requests.get(main_url)
    m3u8_index = m3u8.loads(res.text)
    seg = m3u8_index.data["segments"]
    return __write(url,title,seg)
    
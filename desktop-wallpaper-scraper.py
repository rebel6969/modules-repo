import os , requests , re , random , urllib , string
N = 10
from threading import Thread
def dl(rf,ff):
    try:
        urllib.request.urlretrieve(rf,ff)
    except:
        pass
def scrape():
    pc = requests.get("http://getwallpapers.com/").text
    f = re.compile('/coll\w+.+')
    f = f.findall(pc)
    if f == "" or None:
        scrape()
    for fh in f:
        hb = "http://getwallpapers.com/"+fh.replace('">',"").replace("'>","").replace('">;',"").replace("'>;","")
        lo = requests.get(hb).text
        fcs = re.compile("/\w+/full.+.jpg")
        g = fcs.findall(lo)
        if g == None or "":
            continue
        fuck  = []
        jd = 0
        for ifh in g:
            if jd > 100:
                for i in fuck:
                    try:
                        i.join()
                    except:
                        pass
            ff = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))+ ".jpg"             
            rf = "http://getwallpapers.com/"+ifh
            
            hf = Thread(target=dl,args=(rf,ff))
            fuck.append(hf)
            jd = jd+1
        for idn in fuck:
            idn.start()
            
            


scrape()
import os
from datetime import datetime

def ring():
    print("RING RING RING")

def saveBoundingBox(box, cat, fullFilePath):
    print(box)
    print(cat)
    res = '{'
    res += ' "origin_x": ' + str(box.origin_x)
    res += ', "origin_y": ' + str(box.origin_y)
    res += ', "width": ' + str(box.width)
    res += ', "height": ' + str(box.height)
    res += ', "score": ' + str(cat.score)
    res += ', "category_name": ' + str(cat.category_name) 
    res += '}'
    f = open(fullFilePath, "w")
    f.write(res)

def getCaptureFolderSize(path):
    size= 0
    for ele in os.scandir(path):
        size+=os.stat(ele).st_size
    size = (size / (2**30))
    #print("Capture folder size: " + str(size)[:5] + " GiB") 
    return size  

class SimonsTimer():
    startTime = datetime.now() 
    times = []
    messages = []

    def start(self, message):
        self.startTime = datetime.now() 
        self.times = []
        self.messages = []
        self.times.append(self.startTime)
        self.messages.append(message)
        t1 = datetime.strftime(self.startTime, "%H:%M:%S")
        #print (t1 + "\t" + message)

    def milestone(self, message):
        lapTime = datetime.now()
        delta = lapTime - self.times[len(self.times)-1]
        self.times.append(lapTime)
        self.messages.append(message)
        #print (message + str(delta))

    def done(self):
        t = datetime.now()
        #print("Done " + datetime.strftime(t, "%H:%M:%S"))  
        delta = t - self.startTime  
        #print ("It took " + str(delta))
        for i in range(len(self.times)-1):
            pass
            #print(str(self.times[i]) + "\t" + self.messages[i])



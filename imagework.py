import morse,struct,zlib

mm = ['','.','-','-']
lastWord=[]

prefix=b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D'

def big(x):
    if (x%256)<30:
        if((x//256)%256)<30:
            if((x//(256**2))%256)<30:
                return False

    return True

blank=''
blankt=''

def getXABC(img,x,y,width):

    i=1+y*((width*3)+1) + x*3
    d=img[i:i+3]
    a=bytearray([0,0,0])
    b=a.copy()
    c=b.copy()

    if x!=0:
        i=1+y*((width*3)+1) + (x-1)*3
        a=img[i:i+3]

    if y!=0:
        i=1+(y-1)*((width*3)+1) + x*3
        b=img[i:i+3]
    
    if x!=0 and y!=0:
        i=1+(y-1)*((width*3)+1) + (x-1)*3
        c=img[i:i+3]

    

    return d,a,b,c



def getMorseWD(buffer):
    global blank,blankt
    start=buffer.index(b'IHDR')+4
    width=struct.unpack(">I",buffer[start:start+4])[0]
    start+=4
    height=struct.unpack(">I",buffer[start:start+4])[0]
    start+=9
    crc32 = struct.unpack(">I",buffer[start:start+4])[0]
    start+=4
    datalength = struct.unpack(">I",buffer[start:start+4])[0]
    start+=8
    try:
        image = zlib.decompress(buffer[start:start+datalength])
    except:
        print(struct.pack(">I",datalength),88)

        exit(1)
    # blank,blankt=  struct.unpack(">2I",b'\x00'+image[0:3]+b'\x00'+image[3:6])
    return readImageline(image,width,height)

def add(x,y):
    out=x.copy()
    for i in range(len(x)):
        out[i]=(x[i]+y[i])%256
    return out

def div(x,y):
    out=x.copy()
    for i in range(len(x)):
        out[i]=int(x[i]//y)%256
    return out

def readImageline(img,width,height):
    global lastWord
    lastWord=[]
    x=0
    y=0
    filter=0
    i=0

    accum=0
    letter=""
    word=""

    blank=struct.unpack(">I",b'\x00'+img[1:4])[0]

    img=bytearray(img)

    while y<height:

        if(x%width==0):
            filter=img[y*((width*3)+1)]
            img[y*((width*3)+1)]=0

        i=1+y*((width*3)+1)+x*3
        if(x==width):
            y+=1
            x=0
            img[i-1]=0
            word+=f"{morse.morsedict[letter]}"
            lastWord+=[letter]
            accum=0
            letter=''
            continue
               
        dat,a,b,c=getXABC(img,x,y,width)
        img[i:i+3]=invfilter[filter](dat,a,b,c,0)
        dat=struct.unpack(">I",b'\x00'+img[i:i+3])[0]
        
        if (dat!=blank and dat!=((blank//256)*256)):
           accum+=1
        else:
            letter+=mm[accum]
            accum=0

        x+=1
       
    return word  

def pFunc(a,b,c):
    p = a + b - c
    p%=256
    pa = abs(p - a)%256
    pb = abs(p - b)%256
    pc = abs(p - c)%256
    if pa <= pb and pa <= pc : Pr = a
    elif pb <= pc : Pr = b
    else :Pr = c
    return Pr

def invpFilter(x,a,b,c,d):
    out=x.copy()
    for i in range(0,len(x)):
        out[i]=(x[i]+pFunc(a[i],b[i],c[i]))%256
    return out    
def Nofilter(x,a,b,c,d):return x
def invSub(x,a,b,c,d):return add(x,a)
def invUp(x,a,b,c,d):return add(x,b)
def invAverage(x,a,b,c,d):return add(x,div(add(a,b),2))

invfilter=[Nofilter,invSub,invUp,invAverage,invpFilter]



def getMorseWDEx(buffer):
    global blank,blankt
    start=buffer.index(b'IHDR')+4
    width=struct.unpack(">I",buffer[start:start+4])[0]
    start+=4
    height=struct.unpack(">I",buffer[start:start+4])[0]
    start+=9
    crc32ch = struct.unpack(">I",buffer[start:start+4])[0]
    start+=4
    datalength = struct.unpack(">I",buffer[start:start+4])[0]
    start+=8
    try:
        image = zlib.decompress(buffer[start:start+datalength])[:]
    except:
        print(struct.pack(">I",datalength))
        exit(1)
    image=readImageline(image,width,height)

    # height=len(image)//(width*3+1)   

    # image=zlib.compress(image)

    # imagelen = len(image)
    # imagemetadata = b'IHDR'+struct.pack(">2I",width,height)+b'\x08\x02\x00\x00\x00'
    # crc32ch=struct.pack(">I",zlib.crc32(imagemetadata))
    # imagechunk=b'IDAT'+image
    # imagecrc32=struct.pack(">I",zlib.crc32(imagechunk))
    # buffer=prefix+imagemetadata+crc32ch+struct.pack('>I',imagelen)+imagechunk+imagecrc32+b'\x00\x00\x00\x00IEND\xAE\x42\x60\x82'
    # return buffer
    return image

if __name__=='__main__':
    with open("flag/pwd.png","rb") as imgMorse:
        try:
            buffer=imgMorse.read()
        except:
            exit(1)
    image=getMorseWD(buffer) 
    print(image)

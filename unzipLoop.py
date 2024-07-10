import zipfile,imagework,os,os.path as ath,signal,sys
#St the defaults 
zippy = zipfile.ZipFile("flag_1000.zip")
pwd=None
val=1000
string=b''

goodPWD=goodZip=None

#check for setup vals to overwite defauslts
def checkforflag():

    global zippy,pwd,val

    #check for an existing folder
    if(ath.exists("flag/")):
        #make sure it has files 
        files=os.listdir("flag/")
        Flagfiles = [i for i in files if (".zip"==i[-4:] and "flag_"==i[:5])]

        #select latest flags
        if(len(Flagfiles)!=0):
            mn = val
            fnam=None
            for i in Flagfiles:
                g = int(i[5:-4])
                if(mn>g) and ath.exists(f"flag/pwd_{g}/flag/pwd.png"):
                    mn=g
                    fnam=i
            
            #change val to be the smallest file        
            val=mn  
            if fnam ==None:     
                return
            #close defualt 
            zippy.close()       

            #open new  
            zippy=zipfile.ZipFile(f"flag/{fnam}") 

            # get last pwd       
            log=open(f"flag/pwd_{val}/flag/pwd.png","rb")
            pwd=imagework.getMorseWD(log.read()).encode("utf-8")       
            log.close() 

checkforflag()

#set loom end
end=False

#declare vars
morsepwd=old=None
oldpwd=None

v=False
#loop
for i in range(val-1,-1,-1):
    #
    
    if(end):
        break

    #
    try:    
        old=zippy
        oldpwd=pwd

        zippy=zipfile.ZipFile(old.open(f"flag/flag_{i}.zip",pwd=pwd))
        morsepwd=old.open(f"flag/pwd.png",pwd=pwd)
        old.extract(f'flag/pwd.png',f'flag/pwd_{i}',pwd=oldpwd)
        old.extract(f'flag/flag_{i}.zip',pwd=oldpwd)

               
        
    #   
        goodZip=old 
        goodPWD=pwd
        

        pwd=imagework.getMorseWD(morsepwd.read()).encode()
        string+=pwd
        zippy.open("flag/pwd.png","r",pwd).close()
        
    except (Exception,KeyboardInterrupt) as e:
        oldhandler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT,lambda x,y:print(x,y,sep='\n'))
        end=True   
        if(old):
            
            print('old//',old.filename)
            old.extract(f'flag/flag_{i}.zip',pwd=oldpwd)
            old.extract(f'flag/pwd.png',f'flag/pwd_{i}',pwd=oldpwd)

        else:
            print('zippy//',zippy.filename)
                
        print(pwd)
        signal.signal(signal.SIGINT,oldhandler)
        v=e
        
    finally:
        print(imagework.lastWord)
        print(i)        
        print(pwd)

        
    morsepwd.close()
    old.close() 

print(string)

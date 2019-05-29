import os
#check folder
def tree(folder):
    FL=folder.split('/')
    fl=[]
    for i in range(0,len(FL)):
        if FL[i]!='':
            fl.append(FL[i])
    FL=fl
    if FL[0]=='.':
        FL=FL[1:len(FL)+1]
        FL[0]='./'+FL[0]
    res=[]
    for i in range(1,len(FL)+1):
        res.append('/'.join(FL[0:i]))
    return res

    
def checkFolder(carpeta,create=True):
    paths=tree(carpeta)
    while len(paths)>0:
        folder=paths[0]
        exist=os.path.isdir(folder)
        if(not exist):
            if create:
                os.mkdir(folder)
        paths=paths[1:len(paths)+1]
    return (carpeta)
        
def listFolder(folder,ext=''):
    if folder[-1]!='/':
        folder+='/'
    exist=os.path.isdir(folder)
    #print(exist)
    if exist:
        dirs = os.listdir(folder)
        #print(len(dirs))
        # This would print all the files and directories
        f=[]
        for file in dirs:            
            if os.path.isfile(folder+file):
                compare=True
                if ext!='':
                    compare=os.path.splitext(file)[1]==ext
                if compare:
                    f.append(file)
        return f
    else:
        return []

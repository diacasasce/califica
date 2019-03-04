import os
#check folder
def checkFolder(folder,create=True):
    exist=os.path.isdir(folder)
    if(not exist):
        if create:
        #print(folder)
            os.mkdir(folder)
            return(folder)
        else:
            return exist
    else:
        return (folder)
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

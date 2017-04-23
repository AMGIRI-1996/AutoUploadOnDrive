from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import tkinter as tk
from tkinter import filedialog
import os

gauth = GoogleAuth()
gauth.LoadCredentialsFile("credentials.txt")
#gauth.approval_prompt('force')
if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.LocalWebserverAuth()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("credentials.txt")

drive = GoogleDrive(gauth)
main_dir= "Auto-work-save"
main_dir_id = 0
def init():
    global main_dir_id
    
    file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
    for file1 in file_list:
        if file1['title']==main_dir :
            main_dir_id=file1['id']
    
    if main_dir_id == 0 :
        file1 = drive.CreateFile({'title': main_dir ,"mimeType": "application/vnd.google-apps.folder"})
        file1.Upload()
            
def getDirPath(top) :
    root = tk.Tk()
    root.withdraw()
    dire = filedialog .askdirectory()

    top.pr(dire)
    print(dire)

    #return os.path.basename(os.path.normpath(dire))
    return dire

def getFilePath(top) :
    root = tk.Tk()
    root.withdraw()
    file = filedialog.askopenfilename()

    top.pr(file)
    print(file)
    #return os.path.basename(os.path.normpath(dire))
    return file

def getId(tit,d_id):
	c_id= 0
	file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % d_id}).GetList()
	for file1 in file_list:
		if file1['title']==tit:
			c_id=file1['id']

	return c_id

def createFolder(top,tit,d_id):
	file1 = drive.CreateFile({'title': tit,"parents":  [{"id": d_id}],"mimeType": "application/vnd.google-apps.folder"})
	file1.Upload()
	top.pr("created folder %s" % tit)
    print("created folder %s" % tit)

def uploadFile(top,d,tit,d_id):
	path="%s/%s" % (d,tit)
	c_id= getId(tit,d_id);
	if c_id==0 :
		file1 = drive.CreateFile({'title': tit,"parents":  [{"id": d_id}]})
		file1.SetContentFile(path)
		file1.Upload()
		top.pr("created file %s" % tit)
        print("created file %s" % tit)
	else:
		file1 = drive.CreateFile({'id': c_id })
		file1.Delete()
		top.pr("deleted file %s" % tit)
        print("deleted file %s" % tit)
		uploadFile(top,d,tit,d_id)

def uploadFolder(top, d,d_id):
    tit= os.path.basename(os.path.normpath(d))
    
    c_id= getId(tit,d_id);    
    if c_id==0 :
        createFolder(top,tit,d_id)
        c_id= getId(tit,d_id);
    else :
    	top.pr("%s already exixts" % d)
        print("%s already exixts" % d)

    for name in os.listdir(d):
        if os.path.isfile(os.path.join(d, name)):
        	try:
        		uploadFile(top,d,name,c_id)
        	except:
        		top.pr("error in file: %s"%name)
                print("error in file: %s"%name)
        	else:
        		top.pr("is file: %s"%name)
                print("is file: %s"%name)

        elif os.path.isdir(os.path.join(d, name)):
        	pa="%s/%s" % (d,name)
        	try:
        		uploadFolder(pa,c_id)
        	except:
        		top.pr("Error in Dir: %s"%name)
                print("Error in Dir: %s"%name)
        	else:
        		top.pr("is Dir: %s"%name)
                print("is Dir: %s"%name)


    top.pr("%s uploaded" % d)
    print("%s uploaded" % d)


def uploadOnlyFile(top,path,tit,d_id):
    #path="%s/%s" % (d,tit)
    c_id= getId(tit,d_id);
    if c_id==0 :
        file1 = drive.CreateFile({'title': tit,"parents":  [{"id": d_id}]})
        file1.SetContentFile(path)
        file1.Upload()
        top.pr("created file %s" % tit)
        print("created file %s" % tit)
    else:
        file1 = drive.CreateFile({'id': c_id })
        file1.Delete()
        top.pr("deleted file %s" % tit)
        print("deleted file %s" % tit)
        uploadOnlyFile(top,path,tit,d_id)


def uploadFolderInit(top):
    global main_dir,main_dir_id
    init()
    D = getDirPath(top)
    uploadFolder(top,D,main_dir_id)
    #top.pr('title: %s, id: %s , upload : %s' % (main_dir, main_dir_id, D))

def uploadFileInit(top):
    global main_dir,main_dir_id
    init()
    F = getFilePath(top)
    name = os.path.basename(os.path.normpath(F))
    uploadOnlyFile(top,F,name,main_dir_id)
    #top.pr('title: %s, id: %s , file to upload : %s' % (main_dir, main_dir_id, D))

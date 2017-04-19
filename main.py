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
            
def getDirPath() :
    root = tk.Tk()
    root.withdraw()
    dire = filedialog .askdirectory()

    print(dire)
    #return os.path.basename(os.path.normpath(dire))
    return dire

def getId(tit,d_id):
	c_id= 0
	file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % d_id}).GetList()
	for file1 in file_list:
		if file1['title']==tit:
			c_id=file1['id']

	return c_id

def createFolder(tit,d_id):
	file1 = drive.CreateFile({'title': tit,"parents":  [{"id": d_id}],"mimeType": "application/vnd.google-apps.folder"})
	file1.Upload()
	print("created folder %s" % tit)

def uploadFile(d,tit,d_id):
	path="%s/%s" % (d,tit)
	c_id= getId(tit,d_id);
	if c_id==0 :
		file1 = drive.CreateFile({'title': tit,"parents":  [{"id": d_id}]})
		file1.SetContentFile(path)
		file1.Upload()
		print("created file %s" % tit)
	else:
		file1 = drive.CreateFile({'id': c_id })
		file1.Delete()
		print("deleted file %s" % tit)
		uploadFile(d,tit,d_id)

	


    
def uploadFolder( d,d_id):
    tit= os.path.basename(os.path.normpath(d))
    
    c_id= getId(tit,d_id);    
    if c_id==0 :
        createFolder(tit,d_id)
        c_id= getId(tit,d_id);
    else :
    	print("%s already exixts" % d)

    for name in os.listdir(d):
        if os.path.isfile(os.path.join(d, name)):
        	try:
        		uploadFile(d,name,c_id)
        	except:
        		print("error in file: %s"%name)
        	else:
        		print("is file: %s"%name)

        elif os.path.isdir(os.path.join(d, name)):
        	pa="%s/%s" % (d,name)
        	try:
        		uploadFolder(pa,c_id)
        	except:
        		print("Error in Dir: %s"%name)
        	else:
        		print("is Dir: %s"%name)


    print("%s uploaded" % d)
    
init()
D = getDirPath()
uploadFolder(D,main_dir_id)
print('title: %s, id: %s , file to upload : %s' % (main_dir, main_dir_id, D))

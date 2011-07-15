#!/usr/bin/python
import paramiko,os,re, shutil, string
def cpInter(base_dir, u, p):
    filename = raw_input("File name["+base_dir + "]:")
    if os.path.exists(filename.strip()):#entered full path
        fp = filename.strip()
    else:
        fp = os.path.join(base_dir,filename.strip())
        if not os.path.exists(fp):
            return False
        
    if os.path.isdir(fp):
        files = os.listdir(fp)
            
        for file in files:
            full_file = os.path.join(fp, file)
            
            remote_dir = string.replace(string.replace(full_file, base_dir, ''), file, '')
            copyFile(full_file, remote_dir, u, p)
    else:
        dir, file = os.path.split(fp)
        remote_dir = string.replace(dir, base_dir, '')
        copyFile(fp, remote_dir, u, p)


def copyFile(locFile, remoteDir, username, password):
    host = "www.igb.illinois.edu"                    #hard-coded
    port = 22
    print "Making Transport"
    ftp_base_dir = '/var/www/html/labs/price'

    transport = paramiko.Transport((host, port))
    print "connecting"
    transport.connect(username = username, password = password.strip())
    print "making ftp client"
    sftp = paramiko.SFTPClient.from_transport(transport)
    print "copying " + locFile + " to  " + ftp_base_dir + '/' + remoteDir
    fname = os.path.split(locFile)[1]
    res = sftp.put(locFile, ftp_base_dir + '/' + remoteDir + '/'+fname)
    print res
    sftp.close()
    transport.close()
    print 'done.'

def dropboxFiles(web_folder="/home/earls3/Price/website/Price/Website/downloads"):
    a = re.compile(r'AUREA')
    return [os.path.join(web_folder, x) for x in os.listdir(web_folder) if os.path.exists(os.path.join(web_folder,x)) and a.match(x) is not None ]
    

def copyBuildsFromDropbox(    
    db_folder= '/home/earls3/Dropbox/Price/builds', 
    web_folder="/home/earls3/Price/website/Price/Website/downloads"):
    files = os.listdir(db_folder)
    for file in files:
        full_file = os.path.join(db_folder, file)
        shutil.copy(full_file, web_folder)

if __name__ == "__main__":
 
    username = "earls3"
    unamein = raw_input("Username["+username+"]:")
    if len(unamein.strip()) > 0:
        username = unamein.strip()

    password = raw_input("Password:")
    
    dorf = raw_input("Dropbox or Aurea Dir[d|a]:")
    if dorf.strip() == 'd':
        copyBuildsFromDropbox()
        for file in dropboxFiles():
            copyFile(file, "downloads/", username, password)
    else:
        cpInter('/home/earls3/Price/website/Price/Website', username, password)
    
    

#This program makes connection with the IBM BlueMix account and creates a container if does not exist
#Encrypts the file and uploads it to the container
#Decrypts back when download the file from the container
#Author Roopesh Kumar 1/24/2016
import swiftclient
import keystoneclient
import sys
import gnupg
import os
import tempfile
import shutil

#variables
auth_url = 'https://identity.open.softlayer.com/v3'
user_id = 'cf213672afc14cebb9010ed58aadabf9'
password = 'x*6VJe=jW8pvYX!b'
project_id= 'b41641f4c8a14ad980981b64a9c53d6d'
region_name='dallas'
container_name = 'roopesh_container'
isExist = False
path = "E:/WorkSpace/CloudComputing/assignment1-roopesh/sync/"
temppath="E:/WorkSpace/CloudComputing/assignment1-roopesh/tmp"

#Initialise the connection using object storage credentials
conn = swiftclient.Connection(key=password,
authurl=auth_url,
auth_version='3',
os_options={"project_id": project_id,
"user_id": user_id,
"region_name": region_name})


#initialise the gnupg home directory and generate the input key
mypassphrase = "my passphrase"
recipient = "kroopeshkumar@yahoo.com"
gpg = gnupg.GPG(gnupghome='./gnupg')
input_data = gpg.gen_key_input(name_email=recipient, passphrase=mypassphrase)
key = gpg.gen_key(input_data)
#End of initialisation

#Function to delete the container: Takes one parameter which is the container name and returns boolean
def deleteContainer(container_name):
    conn.delete_container(container_name)
    return True
#End of function deleteContainer()

#Function to encrypt the file: Takes one parameter which is the file name to encrypt and returns the status
def encryptFile(encryptfile):
     with open(path  + encryptfile,'rb') as f:
         status=gpg.encrypt_file(f,recipients=recipient, output=temppath+"/"+encryptfile)
         f.close()
         return status
#End of function encryptFile()

#function to push the files to the server: Takes one parameter which is the container name to push. Does not return anything
def pushObjects(container_name):
    fileList = os.listdir(temppath)
    for files in fileList:
        f = open(temppath + "/" + files,"r+", 2048)
        content= f.read()
        conn.put_object(container_name,files,contents=content, content_type='text/plain')
        f.close()
    shutil.rmtree(temppath, ignore_errors=True)
#End of function pushObjects()

#function to decrypt the data: Takes two parameter which are data to decrypt and file name to write the decrypted data. Does not return anything
def decryptFile(decryptData,fileName):
    encryptedData = gpg.decrypt(decryptData,passphrase = mypassphrase)
    with open(path+fileName,"wb") as newFile:
        newFile.write(str(encryptedData))
        newFile.close()
#End of function decryptFile()

#Function to pull the data object from the server. Takes one parameter which is container name. Does not return anything.
def pullObjects(container_name):
    for files in conn.get_container(container_name)[1]:
        fileName = files['name']
        downfile = conn.get_object(container_name,fileName)[1]
        decryptFile(downfile,fileName)
#End of function pullObjects()

#Function to encrypt the files. Does not take any parameters. Does not return anything.
def encryptFiles():
    fileList = os.listdir(path)
    if not os.path.exists(temppath):
        os.mkdir(temppath)
        os.chmod(temppath,777)
    for file in fileList:
            result = encryptFile(file)
    pushObjects(container_name)
    shutil.rmtree(temppath, ignore_errors=True)
    
#End of function encryptFiles()

#Function to list the files in a container. Takes one parameter which is the container name. Does not return anything
def listFiles(container_name):
    for container in conn.get_account()[1]:
        print "List of objects in the container " + container['name'] + "\n"
        for data in conn.get_container(container['name'])[1]:
            print data['name']
#end of function listFiles

def createContainer():
    for container in conn.get_account()[1]:
        if container['name'] == 'roopesh_container':
            isExist = True

    if isExist == False :
        conn.put_container(container_name)
        print "Container %s created successfully." % container_name + "\n"
    else:
        print "Container " + container_name + " exist\n"
#End of function createContainer()

#Main Function
def main():
    #creating a container if none exist: executes only once
    createContainer()
    encryptFiles()
    listFiles(container_name)
    pullObjects(container_name)
#end of function main()

#program execution starts here
main()

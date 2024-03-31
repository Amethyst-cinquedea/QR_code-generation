import qrcode
import os
from PIL import Image
from Google import Create_Service
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import cv2

def upload_to_drive(ppt):
    CLIENT_SECRET_FILE = 'client-secret.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    # Specify the file to upload
    file_name = ppt # Replace with the actual path of your file
    l=len(file_name)
    file_name = file_name[1:l-1]
    print(file_name)

    # Create file metadata
    file_metadata = {'name': 'file1'}  # Change the name as needed

    # Upload the file to Google Drive
    media = MediaFileUpload(file_name, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File uploaded! File ID: {file.get("id")}')
    file_id=file.get("id")
    request_body = {
        'role' : 'reader',
        'type' : 'anyone'
    }
    response_permission = service.permissions().create(
        fileId=file_id,
        body=request_body
    ).execute()
    rlink=service.files().get(
        fileId=file_id,
        fields='webViewLink'
    ).execute()
    link=rlink.get('webViewLink')
    return link

def generateQR(ppt):
    link=upload_to_drive(ppt)
    qr = qrcode.make(link)
    image_name="ppt_qrcode.png"
    image_path= os.path.join('imageqr',image_name)
    os.makedirs('imageqr', exist_ok=True)
    qr.save(image_path)
    final_img=cv2.imread(image_path)
    cv2.imwrite("ppt_qrcode.png",final_img)
    final_img=Image.open("ppt_qrcode.png")
    final_img.show()
    
    

    #sl.image("ppt_qrcode.png",caption='Scan this to get your presentation')


def main():
    print("Upload your ppt file")
    presentation=input("file path")
    presentation=presentation.replace('/',"\\")
    generateQR(presentation)

main()

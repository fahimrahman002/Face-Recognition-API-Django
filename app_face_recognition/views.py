from django.http import HttpResponse
from rest_framework.response import Response
import cv2
import os
import face_recognition as fr 
from app_api.models import GroupImage, Thumbnail
from django.core.files.storage import default_storage
from django.core.files import File
from rest_framework.decorators import api_view
from app_api.serializers import ThumbnailSerializer
from random import randint
import shutil
from app_face_recognition.gauth import get_drive
# cleanup_old_files
from django.apps import apps
apps.get_models()


@api_view(['GET'])
def test(req):
    my_list={
        'message':"All is well",
        'status':200,
    }
    return Response(my_list)

def main(images,group_image_object,root_path,group_img_path,grp_img_names_without_extention,thumb_dir):
    
    thumbFilesDir = root_path+fr"\thumbnails\{grp_img_names_without_extention}\\"


    if Thumbnail.objects.filter(groupImage=group_image_object).exists():
        Thumbnail.objects.filter(groupImage=group_image_object).delete()

    groupImagePaths  = [fr"{group_img_path}\{name}" for name in os.listdir(group_img_path)]
    # print(groupImagePaths)
    google_drive=get_drive()
    for imgPath in groupImagePaths:
        img = cv2.imread(imgPath)
        fr_image = fr.load_image_file(imgPath)
        face_locations = fr.face_locations(fr_image)
        generate_thumbnails(google_drive,thumbFilesDir,face_locations,img,group_image_object,thumb_dir,grp_img_names_without_extention)
    
    # Forcefully delete the folders
    shutil.rmtree(group_img_path, ignore_errors=True)
    shutil.rmtree(thumb_dir, ignore_errors=True)

    thumbnails=Thumbnail.objects.filter(groupImage=group_image_object)
    serializer=ThumbnailSerializer(thumbnails,many=True)
    return Response(serializer.data)

def generate_thumbnails(google_drive,thumbFilesDir,face_locations,img,group_image_object,thumb_dir,grp_img_names_without_extention):
    randomNumber=randint(1, 1000)
    for idx,(top, right, bottom, left) in enumerate(face_locations):
        file_name = str(randomNumber)+"_thumb_"+str(idx)
        roi = img[top-50:bottom+50,left:right]
        save_image(google_drive,thumbFilesDir,file_name,roi,group_image_object,grp_img_names_without_extention)
    return 
    
def save_image(google_drive,thumbFilesDir,file_name,img,group_image_object,group_image_name_without_extention):
    out_file = thumbFilesDir + file_name + ".jpg"
    cv2.imwrite(out_file,img)
    # Upload thumbnails to AWS S3
    # s3_bucket_link="https://adobe-premiere-pro-project-files.s3.us-east-2.amazonaws.com/"
    # thumbSaveDir=f"thumbnails/{file_name}"+".jpg"
    # s3fileUrl=f"{s3_bucket_link}{thumbSaveDir}"
    # default_storage.save(f'{thumbSaveDir}', File(open(out_file, 'rb')))
    print(f"uploading {file_name}.jpg to drive...")
    fileId=uploadToDrive(google_drive,file_name,out_file)
    fileUrl=f"https://drive.google.com/uc?id={fileId}"
    print(f"Upload complete.")
    thumbnail=Thumbnail.objects.create(
            groupImage=group_image_object,
            title=file_name,
            thumbnail=fileUrl
        )
    thumbnail.save()

    return

def uploadToDrive(google_drive,filename,out_file):
    file = google_drive.CreateFile({'parents': [{'id': '1T_4PMG_3a7-nfHfO4qzTT7N0ZYR_yhGz'}],'title': f'{filename}.jpg'})
    file.SetContentFile(out_file)
    file.Upload()
    return file['id']
   




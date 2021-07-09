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

def main(image,group_image_object,root_path,group_img_path):
    image_name_without_extention=image.name.split(".")[0]
    thumb_dir=root_path+fr"\thumbnails\{image_name_without_extention}"
    if os.path.isdir(thumb_dir)==False:
        os.mkdir(thumb_dir)
    thumb_root_path = root_path+fr"\thumbnails\{image_name_without_extention}\\"
    img = cv2.imread(group_img_path)
    fr_image = fr.load_image_file(group_img_path)
    face_locations = fr.face_locations(fr_image)
    generate_thumbnails(thumb_root_path,face_locations,img,group_image_object,image_name_without_extention,thumb_dir)
    os.remove(group_img_path)
    thumbnails=Thumbnail.objects.filter(groupImage=group_image_object)
    serializer=ThumbnailSerializer(thumbnails,many=True)
    return Response(serializer.data)

def generate_thumbnails(thumb_root_path,face_locations,img,group_image_object,group_image_name_without_extention,thumb_dir):
    for idx,(top, right, bottom, left) in enumerate(face_locations):
        file_name = "thumb_"+str(idx)
        roi = img[top-50:bottom+50,left:right]
        save_image(thumb_root_path,file_name,roi,group_image_object,group_image_name_without_extention)
    os.rmdir(thumb_dir)
    return 
    
def save_image(thumb_root_path,file_name,img,group_image_object,group_image_name_without_extention):
    out_file = thumb_root_path + file_name + ".jpg"
    cv2.imwrite(out_file,img)
    # Upload thumbnails to AWS S3
    default_storage.save(f'thumbnails/{group_image_name_without_extention}/'+file_name+'.jpg', File(open(out_file, 'rb')))
    thumbnail=Thumbnail.objects.create(
            groupImage=group_image_object,
            title=file_name,
            thumbnail=f"https://adobe-premiere-pro-project-files.s3.us-east-2.amazonaws.com/thumbnails/{group_image_name_without_extention}/{file_name}.jpg"
        )
    thumbnail.save()
    os.remove(out_file)
    return



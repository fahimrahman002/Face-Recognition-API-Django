from pathlib import Path
import app_face_recognition
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GeneratedTimeline, GroupImage, SelectedThumbnail, Thumbnail
from app_api.serializers import GeneratedTimelineSerializer, ThumbnailSerializer
import os
from django.http import QueryDict
import json
from django.core.exceptions import ObjectDoesNotExist
# cleanup_old_files
from django.apps import apps
apps.get_models()



@api_view(['GET'])
def home(request):
    my_list = {
        'message': "All is well",
        'status':200,
    }
    return Response(my_list)


@api_view(['GET'])
def getSelectedThumbnails(request,group_img_name):
    try:
        if GroupImage.objects.filter(title=group_img_name).exists():
            groupImage=GroupImage.objects.filter(title=group_img_name)[0]
        else:
            return Response({"message": "Group image of this name is not found.", "status": 404})
            
        thumbnailsExists = Thumbnail.objects.filter(groupImage=groupImage).exists()
        if thumbnailsExists:
            serializer = ThumbnailSerializer(Thumbnail.objects.filter(groupImage=groupImage), many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "There is no thumbnail of this group image.", "status": 404})
    except Exception as e:
        msg=f"Exception {e} occurred."



@api_view(['GET'])
def videoTimeline(request):
    generatedTimeline=GeneratedTimeline.objects.all()
    # print(generatedTimeline[0].videoTimeline)

    serializer=GeneratedTimelineSerializer(generatedTimeline, many=True)
    return Response(serializer.data)
    # return Response({"message": "File uploaded", "status": 200})


@api_view(['POST'])
def postGeneratedTimeline(request):
    videoFileName=request.data['videoFileName']
    videoTimeline=request.data['videoTimeline']
    generatedTimeline=GeneratedTimeline.objects.create(videoFileName=videoFileName,videoTimeline=videoTimeline)
    generatedTimeline.save()
    return Response({"message": "File uploaded", "status": 200})


@api_view(['POST'])
def uploadThumbnails(request):
    # print(type(request.data['selectedThumbnails']))
    # return Response({"message": "File uploaded", "status": 200})
    groupImageExists=GroupImage.objects.filter(pk=int(request.data['groupImageId'])).exists()
    if groupImageExists:
        groupImage=GroupImage.objects.get(pk=int(request.data['groupImageId']))
        selectedThumbnail=SelectedThumbnail.objects.create(groupImage=groupImage,selectedThumbnails=request.data['selectedThumbnails'])
        selectedThumbnail.save()
        return Response({"message": "File uploaded", "status": 200})
    else:
        return Response({"message": "Can't fetch group image", "status":404 })

@api_view(['GET'])
def get_thumbnails(request):
    thumbnails = Thumbnail.objects.all()
    serializer = ThumbnailSerializer(thumbnails, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def testUpload(request):
    try:
        images = request.FILES.getlist('image__first')
        print(images[0].name)
        return Response({"message": "File uploaded", "status": 200})
    except Exception as e:
        print("Exception: "+str(e))
        return Response({"message": "Request has no resource file attached", "status": 404})

@api_view(['POST'])
def groupImageUpload(request):
    try:
        images = request.FILES.getlist('image__first')
        
        try:
            img = images[0]
        except Exception as e:
            return Response({"message": "Can't locate your file", "status": 404})

        root_path = os.getcwd()+ os.sep + os.pardir+fr"\tmp"
        checkDataDir(root_path)
        group_img_path = root_path+fr"\group_images\{img.name}"
        with open(group_img_path, 'wb') as destination:
            for chunk in img.chunks():
                destination.write(chunk)
        groupImage = GroupImage.objects.create(title=img.name)
        groupImage.save()
        return app_face_recognition.views.main(img, groupImage,root_path, group_img_path)
    except Exception as e:
        print("Exception: "+str(e))
        return Response({"message": "Request has no resource file attached", "status": 404})

def checkDataDir(root_path):
    if os.path.isdir(root_path)==False:
        os.mkdir(root_path)
    group_img_dir=root_path+fr"\group_images"
    if os.path.isdir(group_img_dir)==False:
        os.mkdir(group_img_dir)
    thumb_dir=root_path+fr"\thumbnails"
    if os.path.isdir(thumb_dir)==False:
        os.mkdir(thumb_dir)


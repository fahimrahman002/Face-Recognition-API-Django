from pathlib import Path
import app_face_recognition
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GeneratedTimeline, GroupImage, SelectedThumbnail, Thumbnail
from app_api.serializers import GeneratedTimelineSerializer, GroupImageSerializer, ThumbnailSerializer,SelectedThumbnailSerializer
import os
from django.http import QueryDict
import json
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
# cleanup_old_files
from django.apps import apps
apps.get_models()

import json

@api_view(['GET'])
def home(request):
    my_list = {
        'message': "All is well",
        'status':200,
    }
    return Response(my_list)


@api_view(['POST'])
def updateTime(request,pk):
    try:
        time=request.data['time']
        GroupImage.objects.filter(pk=pk).update(time=time)
        return Response({"message": "Fetch time update.", "status": 200})
    except Exception as e:
        print(e)
        return Response({"message": "Group image does not exist.", "status": 404})

@api_view(['DELETE'])
def deleteSelectedThumbnails(request,group_img_id):
    try:
        if GroupImage.objects.filter(pk=group_img_id).exists():
            groupImage=GroupImage.objects.get(pk=group_img_id)
        else:
            return Response({"message": "Group image of this name is not found.", "status": 404})
            
        thumbnailsExists = Thumbnail.objects.filter(groupImage=groupImage).exists()
        if thumbnailsExists:
            Thumbnail.objects.filter(groupImage=groupImage).delete()
            return Response({"message": "All selected files have been deleted.", "status": 200})
        else:
            return Response({"message": "There is no thumbnail of this group image.", "status": 404})
    except Exception as e:
        msg=f"Exception: {e}"
        return Response({"message": msg, "status": 404})

@api_view(['GET'])
def getSelectedThumbnails(request,pk):
    try:
        if GroupImage.objects.filter(pk=pk).exists():
            groupImage=GroupImage.objects.get(pk=pk)
        else:
            return Response({"message": "Group image does not exist.", "status": 404})
        
        thumbnailsExists = SelectedThumbnail.objects.filter(groupImage=groupImage).exists()
        if thumbnailsExists:
            serializer = SelectedThumbnailSerializer(SelectedThumbnail.objects.filter(groupImage=groupImage), many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "There is no thumbnail of this group image.", "status": 404})
    except Exception as e:
        msg=f"Exception {e} occurred."


@api_view(['GET'])
def videoTimeline(request,pk):
    if GroupImage.objects.filter(pk=pk).exists():
        if GeneratedTimeline.objects.filter(groupImage=GroupImage.objects.get(pk=pk)).exists():
            generatedTimeline=GeneratedTimeline.objects.filter(groupImage=GroupImage.objects.get(pk=pk))
            serializer=GeneratedTimelineSerializer(generatedTimeline, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "Timeline haven't generated yet", "status": 404})
    else:
        return Response({"message": "Timeline haven't generated yet", "status": 404})

@api_view(['POST'])
def postGeneratedTimeline(request,pk):
    videoTimeline=request.data['videoTimeline']
    if GroupImage.objects.filter(pk=pk).exists():
        if GeneratedTimeline.objects.filter(groupImage=GroupImage.objects.get(pk=pk)).exists():
            groupImg=GeneratedTimeline.objects.filter(groupImage=GroupImage.objects.get(pk=pk)).first()
            groupImg.update(videoTimeline=videoTimeline)
        else:
            generatedTimeline=GeneratedTimeline.objects.create(groupImage=GroupImage.objects.get(pk=pk),videoTimeline=videoTimeline)
            generatedTimeline.save()
        return Response({"message": "Generated timelines uploaded successfully", "status": 200})
    else:
        return Response({"message": "Group image does not exist.", "status": 200})

@api_view(['DELETE'])
def deleteGeneratedTimeline(request,pk):
    if GeneratedTimeline.objects.filter(pk=pk).exists():
        generatedTimeline=GeneratedTimeline.objects.get(pk=pk)
        generatedTimeline.delete()
        return Response({"message": "Generated timelines deleted successfully", "status": 200})
    else:
        return Response({"message": "No such generated timeline to delete.", "status": 404})
    


@api_view(['POST'])
def uploadThumbnails(request):
    groupImageExists=GroupImage.objects.filter(pk=int(request.data['groupImageId'])).exists()
    if groupImageExists:
        groupImage=GroupImage.objects.get(pk=int(request.data['groupImageId']))
        if SelectedThumbnail.objects.filter(groupImage=groupImage).exists():
            selectedThumbnail=SelectedThumbnail.objects.filter(groupImage=groupImage).first()
            selectedThumbnail.groupImage=groupImage
            selectedThumbnail.selectedThumbnails=request.data['selectedThumbnails']
            selectedThumbnail.save()
        else:
            selectedThumbnail=SelectedThumbnail.objects.create(groupImage=groupImage,selectedThumbnails=request.data['selectedThumbnails'])
            selectedThumbnail.save()
            
        return Response({"message": "Selected Thumbnails uploaded for processing.", "status": 200})
    else:
        return Response({"message": "Can't fetch group image", "status":404 })

@api_view(['GET'])
def thumbnailList(request):
    thumbnails = Thumbnail.objects.all()
    serializer = ThumbnailSerializer(thumbnails, many=True)
    return Response(serializer.data)
    
@api_view(['GET'])
def selectedThumbnailList(request):
    selectedThumbnails = SelectedThumbnail.objects.all()
    # mystr=json.loads(selectedThumbnails[0].selectedThumbnails)
    # print(len(mystr))
    serializer = SelectedThumbnailSerializer(selectedThumbnails, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def groupImageList(request):
    groupImages = GroupImage.objects.all()
    serializer = GroupImageSerializer(groupImages, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteGroupImage(request,pk):
    if GroupImage.objects.filter(pk=pk).exists():
        groupImage=GroupImage.objects.get(pk=pk)
        # if Thumbnail.objects.filter(groupImage=groupImage).exists():
        #     thumbnails=Thumbnail.objects.filter(groupImage=groupImage)
        #     for thumbnail in thumbnails:
        #         default_storage.delete(f'thumbnails/{thumbnail.title}.jpg')
        
        groupImage.delete()
        
        return  Response({"message": "Group Image deleted successfully", "status":200 })
    else:
        return Response({"message": "Group Image doesn't exist", "status":404 })


@api_view(['DELETE'])
def removeImageFromS3(request):
    default_storage.delete('thumbnails/888_thumb_0.jpg')
    return  Response({"message": "Images deleted successfully", "status":200 })

@api_view(['POST'])
def testUpload(request):
    try:
        images = request.FILES.getlist('image__first')
        
        return Response({"message": "File uploaded", "status": 200})
    except Exception as e:
        
        return Response({"message": "Request has no resource file attached", "status": 404})

@api_view(['POST'])
def groupImageUpload(request):
    try:
        images = request.FILES.getlist('groupImages')
        projectName=request.data['projectName']
        importedVideos=request.data['importedVideos']
     
        root_path = os.getcwd()+ os.sep + os.pardir+fr"\tmp"
        grp_img_names_without_extention="G"
        for img in images:
            grp_img_names_without_extention=grp_img_names_without_extention+"+"+img.name.split(".")[0]
        
        group_img_path = root_path+fr"\group_images\{grp_img_names_without_extention}"
        thumb_dir=root_path+fr"\thumbnails\{grp_img_names_without_extention}"
        checkDataDir(root_path,group_img_path,thumb_dir)
   
        for img in images:
            with open(group_img_path+fr"\{img.name}", 'wb') as destination:
                for chunk in img.chunks():
                    destination.write(chunk)
      
        groupImage = GroupImage.objects.create(title=grp_img_names_without_extention,projectName=projectName,importedVideos=importedVideos)
        return app_face_recognition.views.main(groupImage,root_path, group_img_path,grp_img_names_without_extention,thumb_dir)
    
    except Exception as e:
        exceptionMsg=f"Exception:{e}"
        print(exceptionMsg)
        return Response({"message":exceptionMsg , "status": 404})

    

def checkDataDir(root_path,group_img_path,thumb_dir):
    if os.path.isdir(root_path)==False:
        os.mkdir(root_path)
    else:
        print("root path ok")
    groupImgRootdir=root_path+fr"\group_images"
    if os.path.isdir(groupImgRootdir)==False:
        print(groupImgRootdir+" dir created")
        os.mkdir(groupImgRootdir)
    if os.path.isdir(group_img_path)==False:
        print(group_img_path+" dir created")
        os.mkdir(group_img_path)
    thumbRootDir=root_path+fr"\thumbnails"
    if os.path.isdir(thumbRootDir)==False:
        print(thumbRootDir+" dir created")
        os.mkdir(thumbRootDir)
    if os.path.isdir(thumb_dir)==False:
        print(thumb_dir+" dir created")
        os.mkdir(thumb_dir)


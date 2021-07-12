from django.db import models

        
class GroupImage(models.Model):
    title=models.CharField(max_length=600,blank=True,null=True)
    def __str__(self):
        return self.title

class Thumbnail(models.Model):
    groupImage=models.ForeignKey(GroupImage,default=None,on_delete=models.CASCADE)
    title=models.CharField(max_length=200,blank=True,null=True)
    thumbnail=models.CharField(max_length=300,blank=True,null=True)
    def __str__(self):
        return self.groupImage.title+"_"+self.title

class SelectedThumbnail(models.Model):
    groupImage=models.ForeignKey(GroupImage,blank=True,null=True,on_delete=models.CASCADE)
    selectedThumbnails=models.TextField(blank=True,null=True) #In json string format coz SQLite doesn't support JSONField

class GeneratedTimeline(models.Model):
    groupImage=models.ForeignKey(GroupImage,blank=True,null=True,on_delete=models.CASCADE)
    videoTimeline=models.TextField(blank=True,null=True) #In json string format coz SQLite doesn't support JSONField

    

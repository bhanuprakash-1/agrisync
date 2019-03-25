from django.db import models
from oauth.models import Farmer,Expert
#from ckeditor_uploader.fields import RichTextUploadingField








class Topic(models.Model):
    CAT_CHOICES =(
        ('Q','Question'),
        ('I','Improvement'),
        ('S','Suggestion'),
    )
    author=models.ForeignKey(Farmer,Expert , on_delete=models.CASCADE, verbose_name="author of topic")
    title=models.CharField(max_length=256)
    #Work on tags
    #tags=models.CharField(max_length=60,blank=True,null=True,default=None)
    #content=RichTextUploadingField()
    content=models.CharField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    topic=models.ForeignKey(Topic,on_delete=models.CASCADE, verbose_name="topic of answer")
    author=models.ForeignKey(Farmer,on_delete=models.CASCADE,verbose_name="author of the answer")
    #content = RichTextUploadingField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000)

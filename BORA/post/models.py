from django.db import models
from account.models import User,Hashtag


# Create your models here.


    
class Post(models.Model):
    DIFFS = (       # json형태 보고 Choice말고 그냥 Int로 해야할수도..
        (1, 'light'),
        (2, 'middle'),
        (3, 'heavy')
    )
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=200)
    date=models.DateTimeField('date published') 
    post_image=models.ImageField(upload_to = "post_image", null=True, blank=True)
    diff=models.IntegerField(choices=DIFFS)
    hashtag=models.ManyToManyField(Hashtag)
    post_user=models.ForeignKey(User, related_name='post_user',on_delete=models.SET_NULL,null=True)
    bookmark=models.ManyToManyField(User,related_name='post_like')

class PostSec(models.Model):
    sec_id=models.AutoField(primary_key=True)
    num=models.IntegerField()
    title=models.CharField(max_length=200)
    content=models.TextField()
    sec_post=models.ForeignKey(Post, related_name='sec_post',on_delete=models.CASCADE)
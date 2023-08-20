from django.db import models
from account.models import User
from post.models import PostSec
from line.models import Line

# Create your models here.
class Debate(models.Model):
    CONDS=((1,'진행중'),(2,'완료'))
    debate_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=400)
    cond=models.IntegerField(choices=CONDS,default=1)
    debate_user=models.ForeignKey(User, related_name='debate_user',on_delete=models.SET_NULL,null=True)
    debate_postsec=models.ForeignKey(PostSec, related_name='debate_postsec',on_delete=models.CASCADE)
    debate_line=models.ForeignKey(Line, related_name='debate_line',on_delete=models.CASCADE)
    link=models.TextField(null=True,blank=True)
    def __str__(self):
        return "{}: '{}'의 토론 '{}'".format(self.debate_id,self.debate_postsec.sec_post.title,self.title)

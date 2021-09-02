from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from post.models import Post
# Create your models here.



class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post')
    text=models.TextField()
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='replies')
    created_date=models.DateTimeField(editable=False)

    class Meta:
        ordering=('created_date',)

    def save(self,*args,**kwargs):
        if not self.id:
            self.created_date=timezone.now()
        self.modified_date=timezone.now()

        return super(Comment, self).save(*args,**kwargs)

    def __str__(self):
        return self.post.title +" " + self.author.username + " "+self.text

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def any_children(self):
        return Comment.objects.filter(parent=self).exists()
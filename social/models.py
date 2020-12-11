from django.contrib.auth.models import User,auth
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models import CASCADE

# Create your models here.

class profile(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True,default="")
    username = models.CharField(max_length=200,default="")
    nickname = models.CharField(max_length=200,default="")
    user = models.OneToOneField(to=User,on_delete=CASCADE)
    age = models.IntegerField(default=18, validators=[MinValueValidator(18)])
    gender = models.CharField(max_length=20,default="",null=True,blank=True)
    status = models.CharField(max_length=20,default="",null=True,blank=True)
    phone = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    about = models.CharField(max_length=500,null=True,blank=True,default="")
    profile_pic = models.ImageField(upload_to='social/profile/pic', default='social/profile/pic/user.png')
    cover_pic = models.ImageField(upload_to='social/profile/cover',default='social/profile/cover/default-cover.png')
    updated = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.name

class about(models.Model):
    prof = models.OneToOneField(to=profile, on_delete=CASCADE,related_name="profile")
    school = models.CharField(max_length=300,default="",null=True,blank=True)
    jr_college = models.CharField(max_length=300,default="",null=True,blank=True)
    college = models.CharField(max_length=300,default="",null=True,blank=True)
    job = models.CharField(max_length=200,default="",null=True,blank=True)
    movie = models.CharField(max_length=300,default="",null=True,blank=True)
    song = models.CharField(max_length=300,default="",null=True,blank=True)
    book = models.CharField(max_length=300,default="",null=True,blank=True)
    colour = models.CharField(max_length=200,default="",null=True,blank=True)
    fruit = models.CharField(max_length=200,default="",null=True,blank=True)
    food = models.CharField(max_length=200,default="",null=True,blank=True)
    game = models.CharField(max_length=200,default="",null=True,blank=True)
    place = models.CharField(max_length=200,default="",null=True,blank=True)
    singer = models.CharField(max_length=200,default="",null=True,blank=True)
    actor = models.CharField(max_length=200,default="",null=True,blank=True)
    player = models.CharField(max_length=200,default="",null=True,blank=True)

    def __str__(self):
        return "%s" % self.prof


class post(models.Model):
    uploaded_by = models.ForeignKey(to=profile,on_delete=CASCADE)
    pic = models.ImageField(upload_to='social/post',blank=True,null=True)
    text = models.CharField(max_length=1000,default="")
    cr_date = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=200,blank=True,null=True,default="")
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    resized = models.BooleanField(default=False)
    private = models.BooleanField(default=False)
    def __str__(self):
        return "%s (%s)" % (self.uploaded_by ,self.subject)

class comment(models.Model):
    post = models.ForeignKey(to=post,on_delete=CASCADE)
    message = models.CharField(max_length=500)
    commented_by = models.ForeignKey(to=profile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.commented_by

class like(models.Model):
    post = models.ForeignKey(to=post,on_delete=CASCADE)
    liked_by = models.ForeignKey(to=profile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.liked_by

class friend(models.Model):
    profile = models.ForeignKey(to=profile , on_delete=CASCADE)
    followed_by = models.ForeignKey(to=User , on_delete=CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "%s is followed by %s" % (self.profile, self.followed_by)

class chat(models.Model):
    user1 = models.ForeignKey(to=profile , on_delete=CASCADE)
    user2 = models.ForeignKey(to=User , on_delete=CASCADE)
    msg = models.TextField(max_length=2000, default="")
    rec = models.BooleanField(default=False)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s is msg  %s" % (self.user1, self.user2)

class seenChat(models.Model):
    user11 = models.ForeignKey(to=profile , on_delete=CASCADE)
    user22 = models.ForeignKey(to=User , on_delete=CASCADE)
    msgg = models.TextField(max_length=2000, default="")
    recc = models.BooleanField(default=False)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s is msg %s" % (self.user11, self.user22)


class chatFriend(models.Model):
    usr1 = models.ForeignKey(to=profile , on_delete=CASCADE)
    usr2 = models.ForeignKey(to=User , on_delete=CASCADE)
    def __str__(self):
        return "%s is received msg by %s" % (self.usr1, self.usr2)



class notification(models.Model):
    receiver = models.ForeignKey(to=profile , on_delete=CASCADE)
    sender = models.ForeignKey(to=User , on_delete=CASCADE)
    type = models.CharField(max_length=200,default="")  # follow_accept , follow_request
    read = models.BooleanField(default=False)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % (self.receiver)
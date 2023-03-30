# Create your models here.
# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pic/',default = 'defaults/no_pic.png')
    bio = models.TextField(max_length=160, blank=True, null=True,default='hey, this is my synergy profile')
    cover = models.ImageField(upload_to='user_covers/', blank=True,default = 'defaults/default-user-cover.png')
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, default = timezone.now)  # Field renamed to remove unsuitable characters.
    updated_at = models.DateTimeField(blank=True, null=True,  default = timezone.now)
    city = models.CharField(max_length=50, blank=True, null=True)
    is_reported = models.IntegerField(blank=True, null=True,default=False)
    is_block = models.IntegerField(blank=True, null=True, default = False)



    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.profile_pic.url,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def __str__(self):
        return self.username
    
    def img_url(self):
        return self.profile_pic.url
    
    def cover_url(self):
        return self.cover.url



class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255, blank=True, null=True)
    event_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True,default=timezone.now)
    event_picture = models.TextField(blank=True, null=True)
    event_venue = models.TextField(blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True,default=timezone.now)
    e_likers = models.ManyToManyField(User,blank=True , related_name='e_likes')
    e_like_count = models.IntegerField(blank=True, null=True,default=0)
    event_member_count = models.IntegerField(blank=True, null=True,default=0)
    attendees = models.ManyToManyField(User, related_name='attended_events', blank=True)
    event_comment_count = models.IntegerField(blank=True, null=True,default=0)
    created_by_user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    created_by_org = models.ForeignKey('Orgs', on_delete=models.CASCADE, blank=True, null=True)
    
    def img_url(self):
        return self.event_picture.url
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=models.Q(created_by_user__isnull=True) | models.Q(created_by_org__isnull=True),
    #             name='only_one_creator'
    #         )
    #     ]
    


class Orgs(models.Model):
    org_id = models.AutoField(primary_key=True)
    org_name = models.CharField(max_length=255, blank=True, null=True)
    org_tag = models.CharField(unique=True, max_length=255, blank=True, null=True)
    biodata = models.TextField(blank=True, null=True, default = "we would love to welcome you to our community")
    org_created = models.DateTimeField(blank=True, null=True,default=timezone.now)
    org_dp = models.ImageField(upload_to='org_profile/',blank=True, null=True, default = 'defaults/default_group.png')
    cover = models.ImageField(upload_to='org_covers/', blank=True, default = 'defaults/default_org_cover.jpeg')
    org_member_count = models.IntegerField(blank=True, null=True,default = 0)
    org_member = models.ManyToManyField(User, related_name='org_members', blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)  # Field renamed to remove unsuitable characters.

    def img_url(self):
        return self.org_dp.url
    
    def cover_url(self):
        return self.cover.url


class Problems(models.Model):
    problem_id = models.AutoField(primary_key=True)
    problem_name = models.CharField(max_length=255, blank=True, null=True)
    problem_description = models.TextField(blank=True, null=True)
    problem_pic = models.ImageField(upload_to='problems/',blank=True)
    created_at = models.DateTimeField(blank=True, null=True,default=timezone.now)
    help_desc = models.TextField(blank=True, null=True)
    p_likers = models.ManyToManyField(User,blank=True , related_name='p_likes')
    p_like_count = models.IntegerField(blank=True, null=True,default=0)
    problem_comment_count =  models.IntegerField(blank=True, null=True,default=0)
    progress_desc = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    def img_url(self):
        return self.problem_pic.url

class ProblemComments(models.Model):
    problem = models.ForeignKey(Problems, on_delete=models.CASCADE, related_name='comments_on_problem')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pro_commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)
    def serialize(self):
        return {
            "id": self.problem,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }

class EventComments(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, related_name='comments_on_event')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eve_commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)
    def serialize(self):
        return {
            "id": self.event,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
        }

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')

    def __str__(self):
        return f"User: {self.user}"
        


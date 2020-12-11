#from notification import notification
from django.contrib import admin
from .models import profile, post, comment, like, friend, notification, about, chat, chatFriend, seenChat
from django.contrib.admin.options import ModelAdmin

# Register your models here.

class profileAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name","phone"]
    list_filter = ["name","age","gender"]
admin.site.register(profile,profileAdmin)

class aboutAdmin(ModelAdmin):
    list_display = ["prof"]
    search_fields = ["prof"]
    list_filter = ["prof","college","school"]
admin.site.register(about,aboutAdmin)

class postAdmin(ModelAdmin):
    list_display = ["uploaded_by"]
    search_fields = ["uploaded_by","subject"]
    list_filter = ["cr_date","like_count"]
admin.site.register(post,postAdmin)

class commentAdmin(ModelAdmin):
    list_display = ["commented_by"]
    search_fields = ["commented_by","message"]
    list_filter = ["cr_date"]
admin.site.register(comment,commentAdmin)

class likeAdmin(ModelAdmin):
    list_display = ["liked_by"]
    search_fields = ["liked_by"]
    list_filter = ["cr_date"]
admin.site.register(like,likeAdmin)

class friendAdmin(ModelAdmin):
    list_display = ["profile"]
    search_fields = ["profile","followed_by"]
    list_filter = ["profile","accepted"]
admin.site.register(friend,friendAdmin)

class notificationAdmin(ModelAdmin):
    list_display = ["sender"]
    search_fields = ["sender","type"]
    list_filter = ["sender","read"]
admin.site.register(notification,notificationAdmin)

class chatAdmin(ModelAdmin):
    list_display = ["user1","user2"]
    search_fields = ["user1","user2","msg","rec"]
    list_filter = ["cr_date","rec"]
admin.site.register(chat,chatAdmin)

class seenChatAdmin(ModelAdmin):
    list_display = ["user11","user22"]
    search_fields = ["user11","user22","msgg","recc"]
    list_filter = ["cr_date","recc"]
admin.site.register(seenChat,seenChatAdmin)

class chatFriendAdmin(ModelAdmin):
    list_display = ["usr1","usr2"]
    search_fields = ["usr1","usr2"]
admin.site.register(chatFriend,chatFriendAdmin)
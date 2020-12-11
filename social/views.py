import json
from io import BytesIO

from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.core.files.base import ContentFile

from .models import profile, post, friend, notification, like, comment, about, chatFriend, seenChat, chat


# Create your views here.

#Search query
@login_required
def sendMail(request):
    subject, from_email, to = 'hello', 'bhatipravin09@gmail.com', 'bhatipravin777@gmail.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return redirect('/setting/security/')

@login_required
def changePassword(request):
    if request.method == 'GET':
        npassword = request.GET['npassword']
        opassword = request.GET['opassword']
        data={}

        a = auth.authenticate(username=request.user.username,password=opassword)
        data['password_error']=""
        data['password_error2']=""

        if not a:
            data['password_error']="Password not match."
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            if len(npassword) < 6 :
                data['password_error2'] = "Password must contain atleast 6 character."
                return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                u = User.objects.get(username=request.user.username)
                u.set_password(npassword)
                u.save()
                data['password_error'] = ""
                data['password_error2'] = ""
                return HttpResponse(json.dumps(data), content_type="application/json")





@login_required
def searchMatch(request, query, item):
    " ".join(query.split())
    user = User.objects.all()
    x = query.split()


    if query != '':
        for i in x:
            if i.lower() in item.name.lower():
                return True
            elif i.lower() in item.last_name.lower():
                return True
            elif i.lower() in item.username.lower():
                return True
            elif i.lower() in (item.name.lower()+item.last_name.lower()) or i.lower() in (item.last_name.lower()+item.name.lower()) :
                return True
            elif i.lower() in (item.name.lower()+" "+item.username.lower()+" "+item.last_name.lower()):
                return True
            else:
                temp = [use for use in user if (i == use.email)]
                for j in temp:
                    if item.username == j.username:
                        return True
                return False
    else:
        return False


@login_required
def follow_operation(request):
    if request.method == 'GET':

        myid = request.GET['prof_id']
        operation = request.GET['operation']

        if operation=='follow':
            prof = profile.objects.get(pk=myid)
            f = friend(profile=prof,followed_by=request.user)
            f.save()
            noty = notification(receiver=prof,sender=request.user,type="follow_request")
            noty.save()
            data = {}
            data['requested'] = 'True'
            return HttpResponse(json.dumps(data), content_type="application/json")

        elif operation=='accept_req':
            prof = profile.objects.get(pk=myid)
            user2=User.objects.get(username=prof.username)
            f = friend.objects.get(profile=request.user.profile,followed_by=user2)
            f.accepted=True
            f.save()

            cfa = chatFriend.objects.filter(usr1 = request.user.profile,usr2=user2)

            if len(cfa)==0:
                cf1 = chatFriend(usr1=request.user.profile,usr2=user2)
                cf1.save()
                cf2 = chatFriend(usr1=prof,usr2=request.user)
                cf2.save()

            noty = notification(receiver=prof,sender=request.user,type="follow_accept")
            noty.save()
            data = {}
            data['accepted'] = 'True'
            return HttpResponse(json.dumps(data), content_type="application/json")

        elif operation=='unfollow':
            prof = profile.objects.get(pk=myid)
            f = friend.objects.get(profile=prof,followed_by=request.user,accepted=True)
            f.delete()
            data = {}
            data['unfollowed'] = 'True'
            return HttpResponse(json.dumps(data), content_type="application/json")

        elif operation=='cancel_req':
            prof = profile.objects.get(pk=myid)
            f = friend.objects.get(profile=prof,followed_by=request.user,accepted=False)
            f.delete()
            data = {}
            data['cancel_req'] = 'True'
            return HttpResponse(json.dumps(data), content_type="application/json")

        elif operation=='reject':
            prof = profile.objects.get(pk=myid)
            user2=User.objects.get(username=prof.username)
            f = friend.objects.get(profile=request.user.profile,followed_by=user2,accepted=False)
            f.delete()
            data = {}
            data['rejected'] = 'True'
            return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        return HttpResponse("error")

@login_required
def follow_request(request):
    follow_req = friend.objects.filter(profile=request.user.profile,accepted=False)
    if len(follow_req)==0:
        params = {'follow_req': 0}
    else:
        params = {'follow_req':follow_req}
    return render(request,'social/follow_request.html',params)

@login_required
def like_post(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        prof_id = request.GET['prof_id']
        p = post.objects.get(pk=post_id)
        temp=p.like_count
        likes = like.objects.filter(liked_by=request.user.profile,post=p)
        data = {}
        if(len(likes)==0):
            l = like(post=p,liked_by=request.user.profile)
            l.save()
            temp = temp + 1
            p.like_count=temp
            p.save()

            prof = profile.objects.get(pk=prof_id)

            if(prof != request.user.profile):
                noty = notification(receiver=prof, sender=request.user, type="liked_post")
                noty.save()

            data['liked'] = 'True'
            data['l_count'] = temp
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            likes.delete()
            temp = temp - 1
            p.like_count = temp
            p.save()
            data['liked'] = 'False'
            data['l_count'] = temp
            return HttpResponse(json.dumps(data), content_type="application/json")

@login_required
def comment_post(request):

    if request.method == 'GET':
        post_id = request.GET['post_id']
        prof_id = request.GET['prof_id']
        cmt = request.GET['cmt']
        data = {}
        if cmt!="":
            p = post.objects.get(pk=post_id)
            temp=p.comment_count

            c = comment(post=p,commented_by=request.user.profile,message=cmt)
            c.save()
            temp = temp + 1
            p.comment_count=temp
            p.save()

            prof = profile.objects.get(pk=prof_id)

            if(prof != request.user.profile):
                noty = notification(receiver=prof, sender=request.user, type="commented_post")
                noty.save()

            data['commented'] = 'True'
            data['c_count'] = temp
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data['commented'] = 'False'
            return HttpResponse(json.dumps(data), content_type="application/json")



@login_required
def clear_notification(request):
    noty = notification.objects.filter(receiver=request.user.profile)
    noty.delete()
    data={}
    data['cleared'] = 'True'
    return HttpResponse(json.dumps(data), content_type="application/json")



@method_decorator(login_required, name="dispatch")
class HomeView(View):


    def get(self, request, *args, **kwargs):
        post_collection = post.objects.all().order_by('-cr_date')
        foll = friend.objects.filter(followed_by=request.user, accepted=True)
        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl
        posts = []
        for i in post_collection:
            for j in foll:
                if j.profile == i.uploaded_by:
                    posts.append([i])
        l = like.objects.all().order_by('-cr_date')
        c = comment.objects.all().order_by('cr_date')
        my_profile = profile.objects.get(pk=request.user.profile.pk)

        params = {'my_profile': my_profile, 'posts': posts, 'likes': l, 'comments': c, 'chat_frd': chat_frd,
                  'cquery': ""}

        return render(request, 'social/index.html', params)

    def search(request):
        query = request.GET.get('search')
        collection_temp=profile.objects.all().order_by('name')
        profile_collection = [item for item in collection_temp if searchMatch(request,query, item)]

        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl
        if len(profile_collection)==0:
            params = {'all_profile':0,'query':query,'chat_frd': chat_frd, 'cquery': ""}
        else:
            params = {'all_profile': profile_collection, 'chat_frd': chat_frd, 'cquery': ""}
        return render(request, 'social/search.html', params)



@method_decorator(login_required, name="dispatch")
class ProfileView(View):

    def profile(request,myid):
        my_profile=profile.objects.filter(pk=myid)
        posts = post.objects.filter(uploaded_by__in=my_profile).order_by('-cr_date')
        my_profile = profile.objects.get(pk=myid)
        user2=User.objects.get(username=my_profile.username)
        you = friend.objects.filter(profile=my_profile,followed_by=request.user)
        other = friend.objects.filter(profile=request.user.profile,followed_by=user2)
        follower = friend.objects.filter(profile=my_profile,accepted=True)
        following = friend.objects.filter(followed_by=user2,accepted=True)
        l = like.objects.all().order_by('-cr_date')
        c = comment.objects.all().order_by('cr_date')
        abt = about.objects.get(prof=my_profile)

        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl

        if(len(you)==0):
            if (len(other) == 0):
                params={'my_profile':my_profile,'you':'0','other':'0','posts':posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
            else:
                temp = [item for item in other if item.accepted]
                if len(temp)==0:
                    params = {'my_profile': my_profile, 'you':'0', 'other': 'request', 'posts': posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
                else:
                    params = {'my_profile': my_profile, 'you':'0','other':'follow', 'posts': posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
        else:
            if (len(other) == 0):
                temp = [item for item in you if item.accepted]
                if len(temp)==0:
                    params = {'my_profile': my_profile, 'you': 'request', 'other': '0', 'posts': posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
                else:
                    params={'my_profile':my_profile,'you':'follow','other':'0','posts':posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
            else:
                temp = [item for item in you if item.accepted]
                if len(temp) == 0:
                    temp_in = [item_in for item_in in other if item_in.accepted]
                    if len(temp_in) == 0:
                        params = {'my_profile': my_profile, 'you': 'request', 'other': 'request', 'posts': posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
                    else:
                        params = {'my_profile': my_profile, 'you': 'request', 'other': 'follow', 'posts': posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
                else:
                    temp_in = [item_in for item_in in other if item_in.accepted]
                    if len(temp_in) == 0:
                        params = {'my_profile': my_profile, 'you': 'follow', 'other': 'request', 'posts': posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}
                    else:
                        params = {'my_profile': my_profile, 'you': 'follow', 'other': 'follow', 'posts': posts,'follower':follower,'following':following,'likes':l ,'comments':c, 'chat_frd': chat_frd, 'cquery': "",'about':abt}

        return render(request, 'social/profile.html', params)

    def prof_pic_update(request):
        if request.method == "POST":

            pp=True
            my_profile = profile.objects.get(username=request.user.username)

            try:
                my_profile.profile_pic = request.FILES['profile_pic']
                try:
                    img = Image.open(request.FILES['profile_pic'])
                    img.verify()
                except Exception:
                    pp = False
            except Exception:
                pp = False

            if pp:
                my_profile.profile_pic = request.FILES['profile_pic']
                my_profile.save()

                p = profile.objects.get(username=request.user.username)

                image = Image.open(p.profile_pic)

                (width, height) = image.size
                if width > 400 or height > 400:
                    "Max width and height 400"
                    if (width > height):
                        height = (height / width) * 400
                        width = 400
                    else:
                        width = (width / height) * 400
                        height = 400
                    size = (int(width), int(height))
                    img = image.resize(size, Image.ANTIALIAS)
                    img.save(p.profile_pic.path)
                p.save()

            return redirect('/profile/' + str(my_profile.pk))
        else:
            return redirect('/profile/' + str(request.user.profile.pk))

    def post(request):
        if request.method == 'POST':
            error_image = ""
            ie=True
            txt=request.POST.get('text')

            if txt == "":
                try:
                    img = Image.open(request.FILES['new_img'])
                    img.verify()

                    ie = True
                    error_image = ""
                except Exception:
                    error_image = "Invalid Image."
                    ie=False

                params={"error_image":error_image}


                if(ie):
                    my_post=post(uploaded_by=request.user.profile,pic=request.FILES['new_img'],subject=request.POST.get('subject'))
                    my_post.save()
                    p = post.objects.filter(resized=False)
                    for i in p:
                        if i.text == "":
                            image = Image.open(i.pic)
                            (width, height) = image.size
                            if width > 700 or height > 700:
                                "Max width and height 700"
                                if (width > height):
                                    height = (height/width)*700
                                    width=700
                                else:
                                    width = (width / height) * 700
                                    height = 700
                                size = (int(width), int(height))
                                img = image.resize(size, Image.ANTIALIAS)
                                img.save(i.pic.path)
                            i.resized=True
                            i.save()
                    return redirect('/profile/'+str(request.user.profile.pk))
                else:
                    return redirect('/profile/'+str(request.user.profile.pk))

            else:
                my_post = post(uploaded_by=request.user.profile, text=request.POST.get('text'))
                my_post.save()
                return redirect('/profile/' + str(request.user.profile.pk))
        else:
            return redirect('/profile/'+str(request.user.profile.pk))

    def post_delete(request,myid):
        post.objects.filter(pk=myid).delete()
        return redirect('/profile/'+str(request.user.profile.pk))

@method_decorator(login_required, name="dispatch")
class ChatView(View):

    def get(self, request, *args, **kwargs):
        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl
        params = {'chat_frd': chat_frd , 'cquery': ""}
        return render(request,'social/chat.html',params)


    def csearch(request):
        query = request.GET.get('search')
        if query == '':
            return redirect('/chat/')
        else:
            cfrd = chatFriend.objects.filter(usr2=request.user)
            pl = []
            for i in cfrd:
                pl.append(i.usr1)
            profile_collection = [item for item in pl if searchMatch(request,query, item)]
            if len(profile_collection)==0:
                params = {'chat_frd':0,'cquery':query}
            else:
                params = {'chat_frd': profile_collection, 'cquery': query}
            return render(request, 'social/chat.html', params)

    def message(request, rid):
        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl
        rec = profile.objects.get(pk=rid)
        u = User.objects.get(username=rec.username)
        msg = seenChat.objects.filter(user11=request.user.profile,user22=u).order_by('cr_date')
        params={'rec':rec,'msg':msg,'chat_frd': chat_frd , 'cquery': ""}
        return render(request, 'social/message.html', params)

    def sendMessage(request):
        if request.method == 'GET':
            rid = request.GET['rec_id']
            msg = request.GET['message']
            if msg != "":
                u1 = profile.objects.get(pk=rid)
                c1 = chat(user1=u1,user2=request.user,rec=True,msg=msg)
                c1.save()
                u2 = User.objects.get(username=u1.username)
                c2 = chat(user1=request.user.profile,user2=u2,rec=False,msg=msg)
                c2.save()
            data = {}
            data['sent'] = "True"
            return HttpResponse(json.dumps(data), content_type="application/json")

    def messageFetch(request):
        if request.method == 'GET':
            output = []
            rid = request.GET['rec_id']
            p1 = profile.objects.get(pk=rid)
            u1 = User.objects.get(username=p1.username)

            m = chat.objects.filter(user1=request.user.profile,user2=u1).order_by('cr_date')
            for i in m :
                data = {}
                if i.rec:
                    data['rec'] = 'True'
                    c = seenChat(user11=request.user.profile, user22=u1, recc=True, msgg=i.msg)
                    c.save()
                else:
                    c = seenChat(user11=request.user.profile, user22=u1, recc=False, msgg=i.msg)
                    c.save()
                data['msg'] = i.msg
                output.append(data)
                i.delete()
            return HttpResponse(json.dumps(output), content_type="application/json")

@method_decorator(login_required, name="dispatch")
class NotificationView(View):

    def get(self, request, *args, **kwargs):
        my_profile = profile.objects.filter(pk=request.user.profile.pk)
        my_notification = notification.objects.filter(receiver__in=my_profile).order_by('-cr_date')
        follow_req = friend.objects.filter(profile=request.user.profile,accepted=False)
        my_profile = profile.objects.get(pk=request.user.profile.pk)

        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl

        for i in my_notification:
            i.read=True
            i.save()
        if(len(my_notification) == 0):
            params = {'my_profile': my_profile, 'my_notification': 0,'follow_req':len(follow_req), 'chat_frd': chat_frd, 'cquery': ""}
        else:
            params = {'my_profile': my_profile, 'my_notification': my_notification,'follow_req':len(follow_req), 'chat_frd': chat_frd, 'cquery': ""}
        return render(request, 'social/notification.html', params)

    def fetch(request):
        if request.method == 'GET':
            my_notification = notification.objects.filter(receiver=request.user.profile,read=False)
            data = {}
            data['notification_count'] = len(my_notification)
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponse("error")

@method_decorator(login_required, name="dispatch")
class SettingView(TemplateView):
    template_name = "social/setting.html"

    def profile_update(request):
        gender_choice = ["","Male", "Female", "Transgender"]
        status_choice = ["","Single", "Married", "Divorced", "Separated"]
        choices = {"gender_choice": gender_choice, "status_choice": status_choice}

        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl

        error_name=""
        error_last_name=""
        error_email=""
        error_phone=""
        error_age=""
        error_profile=""
        error_cover=""
        if request.method == "POST":

            my_profile = profile.objects.get(username = request.user.username)
            my_profile.name = request.POST.get('first_name')
            my_profile.last_name = request.POST.get('last_name')
            my_profile.email = request.POST.get('email')
            my_profile.phone = request.POST.get('phone')
            my_profile.about = request.POST.get('about')
            my_profile.gender = request.POST.get('gender')
            my_profile.status = request.POST.get('status')
            my_profile.age = request.POST.get('age')
            my_profile.nickname = request.POST.get('nickname')

            pp = True
            pc = True


            try:
                my_profile.profile_pic = request.FILES['profile_pic']
                try:
                    img = Image.open(request.FILES['profile_pic'])
                    img.verify()
                except Exception:
                    pp = False
                    error_profile = "Invalid Image."
            except Exception:
                print("Empty Image.")

            try:
                my_profile.cover_pic = request.FILES['cover_pic']
                try:
                    img = Image.open(request.FILES['cover_pic'])
                    img.verify()
                except Exception:
                    pp = False
                    error_cover = "Invalid Image."
            except Exception:
                print("Empty Image.")


            if (int(my_profile.age) < 15 and int(my_profile.age) > 120):
                error_age = "Age must be greater than 15 and less than 120."
            else:
                error_age = ""


            punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

            for char in my_profile.name:
                if char in punctuations:
                    error_name = "Name can't contain symbols."
                    break

            for char in my_profile.last_name:
                if char in punctuations:
                    error_last_name = "Last name can't contain symbols."
                    break

            params = {"choices": choices, "error_name": error_name,
                      "error_last_name": error_last_name, "error_email": error_email,
                      "error_phone": error_phone, "error_age": error_age,
                      "error_profile": error_profile, "error_cover": error_cover, 'chat_frd': chat_frd, 'cquery': ""}

            if(pp and pc and error_name == "" and error_last_name == ""  and error_phone == ""  and error_age == "" ):
                my_profile.updated = True
                my_profile.save()

                p = profile.objects.get(username = request.user.username)

                image1 = Image.open(p.profile_pic)
                image2 = Image.open(p.cover_pic)

                (width, height) = image1.size
                if width > 400 or height > 400:
                    "Max width and height 400"
                    if (width > height):
                        height = (height/width)*400
                        width=400
                    else:
                        width = (width / height) * 400
                        height = 400
                    size = (int(width), int(height))
                    img = image1.resize(size, Image.ANTIALIAS)
                    img.save(p.profile_pic.path)

                size = (1100,500)
                img = image2.resize(size, Image.ANTIALIAS)
                img.save(p.cover_pic.path)
                p.save()


                return render(request, 'social/profile_update.html',params)
            else:
                return render(request, 'social/profile_update.html', params)

        else:
            params = {"choices": choices, "error_name": error_name,
                      "error_last_name": error_last_name, "error_email": error_email,
                      "error_phone": error_phone, "error_age": error_age,
                      "error_profile": error_profile, "error_cover": error_cover, 'chat_frd': chat_frd, 'cquery': ""}
            return render(request, 'social/profile_update.html',params)

    def security(request):
        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl
        params={'chat_frd': chat_frd , 'cquery': ""}
        return render(request, 'social/set_security.html',params)


    def about(request):
        cfrd = chatFriend.objects.filter(usr2=request.user)
        pl = []
        for i in cfrd:
            pl.append(i.usr1)
        if len(pl) == 0:
            chat_frd = 0
        else:
            chat_frd = pl
        if request.method == "POST":
            abt = about.objects.get(prof = request.user.profile)
            abt.school = request.POST.get('school')
            abt.jr_college = request.POST.get('jr_college')
            abt.college = request.POST.get('college')
            abt.job = request.POST.get('job')
            abt.movie = request.POST.get('movie')
            abt.song = request.POST.get('song')
            abt.book = request.POST.get('book')
            abt.colour = request.POST.get('colour')
            abt.fruit = request.POST.get('fruit')
            abt.food = request.POST.get('food')
            abt.game = request.POST.get('game')
            abt.place = request.POST.get('place')
            abt.singer = request.POST.get('singer')
            abt.actor = request.POST.get('actor')
            abt.player = request.POST.get('player')

            abt.save()

        abt = about.objects.get(prof=request.user.profile)
        params={'about':abt,'chat_frd':chat_frd,'cquery':""}
        return render(request, 'social/set_about.html',params)
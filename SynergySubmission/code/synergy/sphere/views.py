from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import *
# Create your views here.
def index(request):
    all_posts = Events.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    suggestions = []
    c_suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
    return render(request, "sphere/index.html", {
        "posts": posts,
        "suggestions": suggestions,
        "c_suggestions":c_suggestions,
        "page": "all_events",
        'profile': False
    })

def problems(request):
    all_posts = Problems.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    suggestions = []
    c_suggestions = []
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
    return render(request, "sphere/index.html", {
        "posts": posts,
        "suggestions": suggestions,
        "c_suggestions":c_suggestions,
        "page": "all_problems",
        'profile': False
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "sphere/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "sphere/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        profile = request.FILES.get("profile")
        print(f"--------------------------Profile: {profile}----------------------------")
        cover = request.FILES.get('cover')
        print(f"--------------------------Cover: {cover}----------------------------")

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sphere/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            if profile is not None:
                user.profile_pic = profile
            else:
                user.profile_pic = "profile_pic/no_pic.png"
            user.cover = cover           
            user.save()
            follow_obj = Follower.objects.create(user=user)

        except IntegrityError:
            return render(request, "sphere/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "sphere/register.html")

def profile_events(request, username):
    user = User.objects.get(username=username)
    all_posts = Events.objects.filter(created_by_user=user).order_by('-created_at')
    all_problems = Problems.objects.filter(created_by=user).order_by('-created_at')
    created_orgs = Orgs.objects.filter(org_member=user).all()
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    c_suggestions = []
    follower = False
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        if request.user in Follower.objects.get(user=user).followers.all():
            follower = True
    
    following_count = Orgs.objects.filter(org_member=user).count()
    return render(request, 'sphere/profile.html', {
        "username": user,
        "posts": posts,
        "orgs_count":created_orgs.count(),
        "problem_count":all_problems.count(),
        "posts_count": all_posts.count(),
        "suggestions": suggestions,
        "c_suggestions":c_suggestions,
        "page": "profile",
        "is_follower": follower,
        "following_count": following_count
    })

def org_profile(request, username):
    user = Orgs.objects.get(org_name=username)
    all_posts = Events.objects.filter(created_by_org=user).order_by('-created_at')
    # all_problems = Problems.objects.filter(created_by=user).order_by('-created_at')
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    suggestions = []
    c_suggestions = []
    follower = False
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        if request.user in Orgs.objects.get(org_member=user).org_member.all():
            follower = True
    
    following_count = Orgs.objects.filter(org_member=user).count()
    return render(request, 'sphere/orgprofile.html', {
        "username": user,
        "posts": posts,
        # "problem":all_problems,
        # "problem_count":all_problems.count(),
        "posts_count": all_posts.count(),
        "suggestions": suggestions,
        "c_suggestions":c_suggestions,
        "page": "org_profile",
        "is_follower": follower,
        "following_count": following_count
    })

@login_required
def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            text = request.POST.get('text')
            pic = request.FILES.get('picture')
            venue = request.POST.get('venue')
            event_time = request.POST.get('eventtime')
            try:
                
                post = Events.objects.create(created_by_user=request.user, created_by_org = None ,event_name=title, event_description=text,
                                            event_picture=pic,event_venue=venue,event_member_count=0,event_time = event_time)
                return HttpResponseRedirect(reverse('index'))
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'POST'")
    else:
        return HttpResponseRedirect(reverse('login'))
    
@login_required
def create_org(request):
    if request.method == 'POST':
        org_name = request.POST.get('orgname')
        text = request.POST.get('text')
        org_tag = request.Post.get('orgtag')
        pic = request.FILES.get('picture')
        try:
            org = Orgs.objects.create(created_by=request.user.id,org_name=org_name, biodata=text,
                                       org_tag=org_tag,cover=pic)
            org.org_member.add(request.user)
            return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be 'POST'")

@login_required
def create_problem(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        help_desc = request.POST.get('help_desc')
        progress_desc = request.POST.get('progress')
        
        try:
            post = Events.objects.create(created_by_user=request.user,problem_name=title, problem_description=text,
                                        problem_pic=pic,help_desc=help_desc,progress_desc = progress_desc)
            return HttpResponseRedirect(reverse('index'))
        except Exception as e:
            return HttpResponse(e)
    else:
        return HttpResponse("Method must be 'POST'")

@login_required
@csrf_exempt
def edit_problem(request,post_id ):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        img_chg = request.POST.get('img_change')
        help_desc = request.POST.get('help')
        progress_desc = request.POST.get('progress')
        post_id = request.POST.get('id')
        post = Problems.objects.get(problem_id=post_id)
        try:
            post.problem_name = title
            post.problem_description = text
            post.help_desc = help_desc
            post.progress_desc = progress_desc

            if img_chg != 'false':
                post.problem_pic = pic
            post.save()
            
            if(post.problem_name):
                post_name = post.problem_name
            else:
                post_name = False

            if(post.help_desc):
                post_help_desc = post.help_desc
            else:
                post_help_desc = False
            
            if(post.progress_desc):
                post_progress_desc = post.progress_desc
            else:
                post_progress_desc = False

            if(post.problem_description):
                post_text = post.problem_description
            else:
                post_text = False

            if(post.problem_pic):
                post_image = post.img_url()
            else:
                post_image = False
            
            return JsonResponse({
                "success": True,
                "title":post_name,
                "problem_progress": post_progress_desc,
                "problem_help": post_help_desc,
                "text": post_text,
                "picture": post_image,
                
            })
        except Exception as e:
            print('-----------------------------------------------')
            print(e)
            print('-----------------------------------------------')
            return JsonResponse({
                "success": False
            })
    else:
            return HttpResponse("Method must be 'POST'")


@csrf_exempt
def like_problem(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Problems.objects.get(problem_id=id)
            print(post)
            try:
                post.likers.add(request.user)
                post.like_count += 1 
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unlike_problem(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Problems.objects.get(problem_id=id)
            print(post)
            try:
                post.likers.remove(request.user)
                post.like_count -= 1
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@csrf_exempt
def edit_post(request,post_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        pic = request.FILES.get('picture')
        img_chg = request.POST.get('img_change')
        venue = request.POST.get('venue')
        event_time = request.POST.get('eventtime')
        post_id = request.POST.get('id')
        post = Events.objects.get(event_id=post_id)
        try:
            post.event_name = title
            post.event_description = text
            post.event_venue = venue
            post.event_time = event_time

            if img_chg != 'false':
                post.event_picture = pic
            post.save()
            
            if(post.event_name):
                post_name = post.event_name
            else:
                post_name = False

            if(post.event_venue):
                post_venue = post.event_venue
            else:
                post_venue = False
            
            if(post.event_time):
                post_time = post.event_time
            else:
                post_time = False

            if(post.event_description):
                post_text = post.event_description
            else:
                post_text = False

            if(post.event_picture):
                post_image = post.img_url()
            else:
                post_image = False
            
            return JsonResponse({
                "success": True,
                "title":post_name,
                "event_time": post_time,
                "event_venue": post_venue,
                "text": post_text,
                "picture": post_image,
                
            })
        except Exception as e:
            print('-----------------------------------------------')
            print(e)
            print('-----------------------------------------------')
            return JsonResponse({
                "success": False
            })
    else:
            return HttpResponse("Method must be 'POST'")

@csrf_exempt
def like_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Events.objects.get(event_id=id)
            print(post)
            try:
                post.likers.add(request.user)
                post.like_count += 1 
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unlike_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Events.objects.get(event_id=id)
            print(post)
            try:
                post.likers.remove(request.user)
                post.like_count -= 1
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def save_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Events.objects.get(event_id=id)
            print(post)
            try:
                post.attendees.add(request.user)
                post.event_member_count += 1
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unsave_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Events.objects.get(event_id=id)
            print(post)
            try:
                post.attendees.remove(request.user)
                post.event_member_count -= 1
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def event_comment(request, event_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body) 
            comment = data.get('comment_text')
            post = Events.objects.get(event_id=event_id)
            try:
                newcomment = EventComments.objects.create(event=post,commenter=request.user,comment_content=comment)
                post.event_comment_count += 1
                post.save()
                print(newcomment.serialize())
                return JsonResponse([newcomment.serialize()], safe=False, status=201)
            except Exception as e:
                return HttpResponse(e)
    
        post = Events.objects.get(event_id=event_id)
        comments = EventComments.objects.filter(event=post)
        comments = comments.order_by('-comment_time').all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def problem_comment(request, problem_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            data = json.loads(request.body)
            comment = data.get('comment_text')
            post = Problems.objects.get(problem_id=problem_id)
            try:
                newcomment = ProblemComments.objects.create(problem=post,commenter=request.user,comment_content=comment)
                post.problem_comment_count += 1
                post.save()
                print(newcomment.serialize())
                return JsonResponse([newcomment.serialize()], safe=False, status=201)
            except Exception as e:
                return HttpResponse(e)
    
        post = Problems.objects.get(problem_id=problem_id)
        comments = ProblemComments.objects.filter(problem=post)
        comments = comments.order_by('-comment_time').all()
        return JsonResponse([comment.serialize() for comment in comments], safe=False)
    else:
        return HttpResponseRedirect(reverse('login'))



@csrf_exempt
def delete_problem(request, problem_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Problems.objects.get(problem_id=problem_id)
            if request.user == post.created_by:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def delete_event(request, event_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Events.objects.get(id=event_id)
            if request.user == post.created_by_user:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def delete_org(request, org_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Orgs.objects.get(id=org_id)
            if request.user == post.created_by:
                try:
                    delet = post.delete()
                    return HttpResponse(status=201)
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse(status=404)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def follow_org(request, org_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            try:
                org = Orgs.objects.get(org_id=org_id)
                org.org_member.add(request.user)
                org.save()
                print(f".....................User: {request.user}......................")
                print(f".....................org: {org}......................")
                return HttpResponse(status=204)
                
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))
    
@csrf_exempt
def unfollow_org(request, org_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            try:
                org= Orgs.objects.get(org_id=org_id)
                org.org_member.remove(request.user)
                org.save()
                print(f".....................User: {request.user}......................")
                print(f".....................org: {org}......................")
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def follow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Follower: {request.user}......................")
            try:
                (follower, create) = Follower.objects.get_or_create(user=user)
                follower.followers.add(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))

@csrf_exempt
def unfollow(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user = User.objects.get(username=username)
            print(f".....................User: {user}......................")
            print(f".....................Unfollower: {request.user}......................")
            try:
                follower = Follower.objects.get(user=user)
                follower.followers.remove(request.user)
                follower.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")
    else:
        return HttpResponseRedirect(reverse('login'))


def following(request):
    if request.user.is_authenticated:
        following_orgs = Orgs.objects.filter(org_member=request.user)
        all_posts = Events.objects.filter(created_by_org__in=following_orgs).order_by('-created_at')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, "sphere/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            "page": "following"
        })
    else:
        return HttpResponseRedirect(reverse('login'))

def saved(request):
    if request.user.is_authenticated:
        all_posts = Events.objects.filter(attendees=request.user).order_by('-created_at')

        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        if page_number == None:
            page_number = 1
        posts = paginator.get_page(page_number)

        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, "sphere/index.html", {
            "posts": posts,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            "page": "following"
        })
    else:
        return HttpResponseRedirect(reverse('login'))
    
def communitylist(request,username):
    user = User.objects.get(username=username)
    comm_list1 =  Orgs.objects.filter(org_member=user)
    comm_list2 = list(comm_list1)
    user2 = User.objects.get(username=request.user.username)
    common_comm = comm_list1.filter(org_member=user2)
    orgs_list = []
    c_suggestions = []
    suggestions = []
    for org in list(common_comm):
        if org in comm_list2:
            comm_list2.remove()
        org_dict = {
                    'id': org.org_id,
                    'name': org.org_name,
                    'tag': org.org_tag,
                    'dp': org.org_dp.url,
                    'is_following': True  # set to False since user2 is not following this org
                }
        orgs_list.append(org_dict)
    
    for org in comm_list2:
        org_dict = {
                    'id': org.org_id,
                    'name': org.org_name,
                    'tag': org.org_tag,
                    'dp': org.org_dp.url,
                    'is_following': False  # set to False since user2 is not following this org
                }
        orgs_list.append(org_dict)
    
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "orgs",
            "orgs_list":orgs_list,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "orgs",
            "orgs_list":orgs_list,
            'profile': False
        })

def followerlist(request,username):
    follow_list = Follower.objects.get(user = username).followers.all()
    comm_list2 = list(follow_list)
    common_friend = follow_list.filter(followers=request.user.username)
    follower_list = []
    c_suggestions = []
    suggestions = []
    for friend in list(common_friend):
        if friend in comm_list2:
            comm_list2.remove()
        friend_dict = {
                    'id': friend.id,
                    'name': friend.first_name + friend.last_name,
                    'tag': friend.username,
                    'dp': friend.profile_pic.url,
                    'is_following': True  
                }
        follower_list.append(friend_dict)
    
    for friend in comm_list2:
        friend_dict = {
                    'id': friend.id,
                    'name': friend.first_name + friend.last_name,
                    'tag': friend.username,
                    'dp': friend.profile_pic.url,
                    'is_following': True  
                }
        follower_list.append(friend_dict)
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "follower_list":follower_list,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "follower_list":follower_list,
            'profile': False
        })

def followinglist(request,username):
    following_list = Follower.objects.filter(followers = username).all()
    comm_list2 = list(following_list)
    common_friend = following_list.filter(followers=request.user.username)
    follower_list = []
    c_suggestions = []
    suggestions = []
    for friend in list(common_friend):
        if friend in comm_list2:
            comm_list2.remove()
        friend_dict = {
                    'id': friend.id,
                    'name': friend.first_name + friend.last_name,
                    'tag': friend.username,
                    'dp': friend.profile_pic.url,
                    'is_following': True  
                }
        follower_list.append(friend_dict)
    
    for friend in comm_list2:
        friend_dict = {
                    'id': friend.id,
                    'name': friend.first_name + friend.last_name,
                    'tag': friend.username,
                    'dp': friend.profile_pic.url,
                    'is_following': True  
                }
        follower_list.append(friend_dict)
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "follower_list":follower_list,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "follower_list":follower_list,
            'profile': False
        })    

def e_likerlist(request,event_id):
    liker_list = list(Events.objects.get(event_id=event_id).e_likers.all())
    likers_list = []
    c_suggestions = []
    suggestions = []
    for liker in liker_list:
        liker_dict = {
                    'id': liker.id,
                    'name': liker.first_name + liker.last_name,
                    'tag': liker.username,
                    'dp': liker.profile_pic.url, 
                }
        likers_list.append(liker_dict)
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "liker_list":likers_list,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "liker_list":likers_list,
            'profile': False
        })    
    
def p_likerlist(request,problem_id):
    liker_list = list(Problems.objects.get(event_id=problem_id).p_likers.all())
    likers_list = []
    c_suggestions = []
    suggestions = []
    for liker in liker_list:
        liker_dict = {
                    'id': liker.id,
                    'name': liker.first_name + liker.last_name,
                    'tag': liker.username,
                    'dp': liker.profile_pic.url, 
                }
        likers_list.append(liker_dict)
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "liker_list":likers_list,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "liker_list":likers_list,
            'profile': False
        })
    
def e_memberlist(request,event_id):
    member_list = list(Events.objects.get(event_id=event_id).attendees.all())
    members_list = []
    c_suggestions = []
    suggestions = []
    for member in member_list:
        member_dict = {
                    'id': member.id,
                    'name': member.first_name + member.last_name,
                    'tag': member.username,
                    'dp': member.profile_pic.url, 
                }
        members_list.append(member_dict)
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "member_list":members_list,
           "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "member_list":members_list,
            'profile': False
        })
    
def c_memberlist(request,org_name):
    member_list = list(Orgs.objects.get(org_name=org_name).org_member.all())
    members_list = []
    c_suggestions = []
    suggestions = []
    for member in member_list:
        member_dict = {
                    'id': member.id,
                    'name': member.first_name + member.last_name,
                    'tag': member.username,
                    'dp': member.profile_pic.url, 
                }
        members_list.append(member_dict)
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "member_list":members_list,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "user",
            "member_list":members_list,
            'profile': False
        })

def createdcommunities(request,username):
    user = User.objects.get(username=username)
    created_orgs = list(Orgs.objects.filter(created_by=user).all())
    orgs_list = []
    c_suggestions = []
    suggestions = []
    for org in created_orgs:
        org_dict = {
                    'id': org.org_id,
                    'name': org.org_name,
                    'tag': org.org_tag,
                    'dp': org.org_dp.url,
                    'is_following': False  # set to False since user2 is not following this org
                }
        orgs_list.append(org_dict)
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        return render(request, 'sphere/list.html', {
            "list_type": "orgs",
            "orgs_list":orgs_list,
            "suggestions": suggestions,
            "c_suggestions":c_suggestions,
            'profile': False
        })
    else:
        return render(request, 'sphere/list.html', {
            "list_type": "orgs",
            "orgs_list":orgs_list,
            'profile': False
        })

def communityevent(request,username,org_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST.get('title')
            text = request.POST.get('text')
            pic = request.FILES.get('picture')
            venue = request.POST.get('venue')
            creator = request.POST.get('creator') 
            event_time = request.POST.get('eventtime')
            try:
                post = Events.objects.create(created_by_user=username,created_by_org=org_id,event_name=title, event_description=text,
                                            event_picture=pic,event_venue=venue,event_member_count=0,event_time = event_time)
                return HttpResponseRedirect(reverse('index'))
                
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'POST'")
    else:
        return HttpResponseRedirect(reverse('login'))
    
def profile_problems(request, username):
    user = User.objects.get(username=username)
    all_posts = Events.objects.filter(created_by_user=user).order_by('-created_at')
    all_problems = Problems.objects.filter(created_by=user).order_by('-created_at')
    created_orgs = Orgs.objects.filter(org_member=user).all()
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    if page_number == None:
        page_number = 1
    posts = paginator.get_page(page_number)
    followings = []
    c_suggestions = []
    suggestions = []
    follower = False
    if request.user.is_authenticated:
        followings = Follower.objects.filter(followers=request.user).values_list('user', flat=True)
        suggestions = User.objects.exclude(pk__in=followings).exclude(username=request.user.username).order_by("?")[:6]
        followings_c = Orgs.objects.filter(org_member=request.user).values_list('org_member', flat=True)
        c_suggestions = Orgs.objects.exclude(pk__in=followings_c).exclude(created_by=request.user.id).order_by("?")[:6]
        if request.user in Follower.objects.get(user=user).followers.all():
            follower = True
    
    following_count = Orgs.objects.filter(org_member=user).count()
    return render(request, 'sphere/profile.html', {
        "username": user,
        "posts": posts,
        # "problem":all_problems,
        "problem_count":all_problems.count(),
        "posts_count": all_posts.count(),
        "orgs_count": created_orgs.count(),
        "suggestions": suggestions,
        "c_suggestions":c_suggestions,
        "page": "profile",
        "is_follower": follower,
        "following_count": following_count
    })
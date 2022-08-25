from re import M
from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import FollowerCount, LikePost, Profile, Post
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)    
    user_profile = Profile.objects.get(user=user_object)   
    
    user_following_list = []
    feed = []
    
    user_following = FollowerCount.objects.filter(follower=request.user.username)
    
    #getting the followed users
    for users in user_following:
        user_following_list.append(users.user)
     
    #showing posts for if only followed particular user   
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
        
        
    #shows all posts one after the other    
    feed_list = list(chain(*feed))
        
    #user suggestion
    all_users = User.objects.all()
    user_following_all = []
    
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
        
    #creating suggestions for not followed user     
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all()))]
    #identifying current user
    current_user = User.objects.filter(username=request.user.username)
    #excluding the logged in user from showing on suggestions
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    
    return render(request,'index.html',{'user_profile':user_profile,'posts':feed_list})

@login_required(login_url='signin')
def upload(request):
    
    #requests the information while uploading
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
    #saving the infromation 
        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        
        return redirect('/')
    else:
        return redirect('/')
    
@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    if request.method == 'POST':
        username = request.POST['username']
        #checks for username in database as we type in search 
        username_object = User.objects.filter(username__icontains=username) 
        
        username_profile = []
        username_profile_list = []
    
    #getting the user id 
        for users in username_object:
            username_profile.append(users.id)
            
    #getting the profile of user using id_user        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
            
        username_profile_list = (list(chain(*username_profile_list)))         
            
    return render(request,'search.html',{'user_profile':user_profile,'username_profile_list':username_profile_list})
    
@login_required(login_url='signin')
def like_post(request):
    
    username = request.user.username    #showscurrently loggedin user 
    post_id = request.GET.get('post_id') #sending post_id to template
    
    post = Post.objects.get(id=post_id) #getting the Posts id 
    
    like_filter = LikePost.objects.filter(post_id=post_id,username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    #if user already likes the post decrement the like
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
 
@login_required(login_url='signin')
def follow(request):
    
    if request.method == "POST":
        follower = request.POST['follower']
        user = request.POST['user']
        
        #if a user wants to unfollow other user
        if FollowerCount.objects.filter(follower=follower,user=user).first():
            delete_follower = FollowerCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user) 
        
        #unfollowed user can follow other user
        else:
            new_follower = FollowerCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)     
    else:
        return redirect('/')
        



@login_required(login_url='signin') 
def profile(request,pk):    
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk) #filtering posts for particular user
    user_post_length = len(user_posts) #total number of posts to be displayed

    follower = request.user.username
    user = pk
    
    
    if FollowerCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow' #if user follows other user then user can unfollow
    else:
        button_text = 'Follow'  #if user not follows other user then user can follow
    
    #finding how many users have followed 
    user_followers = len(FollowerCount.objects.filter(user=pk))
        
    #finding how many users the current profile user has followed  
    user_following = len(FollowerCount.objects.filter(follower=pk)) 
        
    context = {
        
        'user_object' : user_object,
        'user_profile' : user_profile,            
        'user_posts' : user_posts,
        'user_post_length' : user_post_length,
        'button_text' : button_text,
        'user_followers' : user_followers,
        'user_following' : user_following,
        
    }
    
    return render(request,'profile.html',context)   

@login_required(login_url='signin')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image =user_profile.profileimg
            bio =request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio =request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('/') 
        
    return render(request, 'setting.html',{'user_profile':user_profile})

def signup(request):

    # created POST method 
    if request.method == "POST":
        username  = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        #checking fields are correct or not and redirecting again
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already exists')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username,password=password) 
                auth.login(request, user_login)
                

                #create a Profile object for the user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
                
        else:
            messages.info(request,'Password does not match')
            return redirect('signup')
    else:
        return render(request,'signup.html')
    
  
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username , password=password)   
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request,'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
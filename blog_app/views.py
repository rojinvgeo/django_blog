from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages

# Create your views here.


def blog(request):
    travel_category = Category.objects.get(slug='travel')
    health_category=Category.objects.get(slug='lifestyle')
    technology_category=Category.objects.get(slug='technology')
    business_category=Category.objects.get(slug='business')
    education_category=Category.objects.get(slug='education')
    fitness_category=Category.objects.get(slug='fitness')

    specific_categories = [travel_category, 
                           technology_category,
                           business_category,
                           health_category,
                           education_category,
                           fitness_category,
                           ]
    # Retrieve top 3 clicked posts
    top_stories = Post.objects.order_by('-clicks')[:3]
    print(list(top_stories))
    # Retrieve 5 recent posts
    recent_articles = Post.objects.order_by('-updated_at')[:5]     
    
    print(list(recent_articles))
    
    for post in top_stories:
        if post.author.is_superuser:
            post.author_name = "Admin"
        else:
            post.author_name = post.author.username
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.clicks += 1
        post.save()
        messages.success(request, 'Post viewed successfully!')
        return redirect('blog')
    return render(request, 'index.html',{
        'specific_categories': specific_categories,
        'top_stories': top_stories,
        'recent_articles' : recent_articles
    })

def top_blogs(request):
    top_blogs = Post.objects.order_by('-clicks')
    paginator = Paginator(top_blogs, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
    }
    return render(request, 'postlist_by_category.html', context)

	






def blog_admin(request):
    return render(request,'blog-admin.html')



def admin_login(request):
    if request.method=="POST":
        uname=request.POST.get('uname')
        pwd=request.POST.get('pwd')
        if uname.lower() == 'admin' and pwd == '1234':
            request.session['user'] = uname
            return redirect(blog_admin)
        else:
            return HttpResponse('PLEASE ENTER A VALID USERNAME AND PASSWORD')
    else:
        return render(request,'admin_signin.html')
    
def post(request):
    return render (request, 'post.html')


def create_post(request):
    categories = Category.objects.all()
    author_username = request.session.get('user')
    print(f"Session user: {author_username}")

    
    if 'user' not in request.session:
        return HttpResponse("You must be logged in to create a post", status=403)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        print(f"Category ID: {category_id}")
        image = request.FILES.get('image')
        created_at = request.POST.get('created_at')

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse("Category not found", status=404)

        if request.session['user'] == 'admin':
            # Admin is creating the post
            post = Post(
                title=title,
                content=content,
                category=category,
                image=image,
                created_at=created_at,
                author=request.user 
            )
        else:
            # Regular user is creating the post
            post = Post(
                title=title,
                content=content,
                category=category,
                image=image,
                created_at=created_at,
                author=request.user
            )
        
        post.save()
        

    return render(request, 'post.html', {'categories': categories})






# def create_post(request):
#     categories = Category.objects.all()
#     author_username = request.session.get('user')
#     print(f"Session user: {author_username}")
#     admin_user = User.objects.get(username='admin')
    
#     if 'user' not in request.session:
#         return HttpResponse("You must be logged in to create a post", status=403)
#     post = None  # Define post variable here

#     if request.session['user'] == 'admin':
#         # Admin is creating the post, so proceed with admin-specific logic
#         pass
#     else:
#         # Regular user is creating the post, so proceed with user-specific logic
#         pass

#     # Rest of your code here...

#     # Since you don't have a User model, we'll use the auth_name directly
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         category_id = request.POST.get('category')
#         print(f"Category ID: {category_id}")
#         image = request.FILES.get('image')
#         created_at = request.POST.get('created_at')

#         try:
#             category = Category.objects.get(id=int(category_id))
#         except Category.DoesNotExist:
#             return HttpResponse("Category not found", status=404)

       
#         # Create and save the Post instance
#         post = Post(
#             title=title,
#             content=content,
#             category=category,
#             image=image,
#             created_at=created_at,
#             author=request.user,
#             admin= admin_user 
#         )
#         post.save()

#         # Add the post instance to the context dictionary
#     context = {
#         'post': post,
#         'categories': categories
#     }


#     # Render the admin page with categories

#     return render(request, 'post.html', context)


# from django.http import FileResponse
# import os


# def serve_media(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     wrapper = FileResponse(open(file_path, 'rb'))
#     response = HttpResponse(wrapper, content_type='image/jpeg')
#     response['Content-Length'] = os.path.getsize(file_path)
#     return response








# def create_post(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         category_id = request.POST.get('category')
#         image = request.FILES.get('image')
#         # category = Category.objects.get(id=category_id)
#         category_name = request.POST['category']
#         category, created = Category.objects.get_or_create(name=category_name)
#         created_at=request.POST.get('created_at')
#         author = User.objects.get(username=request.session['user'])
#         post = Post(author=author, title=title, content=content, category=category, image=image, created_at=created_at)
#         post.save()
#     return render(request,'admin_post.html',)
import bleach




#testing

from django.core.paginator import Paginator

def post_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(page_number)

    for post in page_obj.object_list:
      post.author_name = 'Admin' if request.session.get('user') == 'admin' else post.author.username 

    # admin_username = request.session.get('user',  'Unknown')  # Retrieve the admin's username from the session
    # current_author = request.user.username if request.user.is_authenticated else request.session.get('admin_user')
    for post in posts:
        print('POST IMAGE', post.image.url)  # Print the image URL
          # Check if author_name is being populated
          

            
    # admin_username = request.session.get('user')  # Get the admin's username from the session
    # author_username = request.user.username if request.user.is_authenticated else 'Guest'
    image_urls = [post.image.url for post in posts]
    context = {
        'posts': page_obj.object_list,  # Use page_obj.object_list instead of posts
        'category': category,
        'image_urls': image_urls,
        'page_obj':page_obj,
        'url_path': request.path  # Pass the URL path to the template
        #  'author_name': admin_username
    }
    for i in posts:
        print(i.author.username)
        # Check the context
    return render(request, 'postlist_by_category.html', context)


#post_list_by_category orginal code

#def post_list_by_category(request, category_slug, page_number=1):
    
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page('page', 1)
    admin_username = request.session.get('user',  'Unknown')  # Retrieve the admin's username from the session
    # current_author = request.user.username if request.user.is_authenticated else request.session.get('admin_user')
    for post in posts:
        print('POST IMAGE', post.image.url)  # Print the image URL
        post.author_name = admin_username

    # admin_username = request.session.get('user')  # Get the admin's username from the session
    # author_username = request.user.username if request.user.is_authenticated else 'Guest'
    image_urls = [post.image.url for post in posts]
    context = {
        'posts': page_obj.object_list,  # Use page_obj.object_list instead of posts
        'category': category,
        'image_urls': image_urls,
        'page_obj':page_obj,
        'url_path': request.path  # Pass the URL path to the template
        #  'author_name': admin_username
    }
    for i in posts:
        print(i.author.username)
    return render(request, 'travel-post-category.html', context)

import markdown2


def post_detail(request, category_slug, post_id):
    category = get_object_or_404(Category, slug=category_slug)
    post = get_object_or_404(Post, id=post_id, category=category)
    post.clicks += 1  # Increment the clicks field
    post.save()  # Save the changes
    content = post.content  # Assuming post.content holds the HTML content
    formatted_content = markdown2.markdown(content)
    admin_username = request.session.get('user',  'Unknown')
    post.author_name = admin_username
    context = {
        'post': post,
        'category': category,
        'content': formatted_content
        }
    return render(request, 'postdetails.html', context)



# def travel_post_details(request, category_slug):
#     category = get_object_or_404(Category, slug=category_slug)
#     posts = Post.objects.filter(category=category)
#     context = {
#         'posts': posts,
#         'category': category
#     }
#     return render(request, 'travel_postdetails.html', context)
    

# def post_list_by_category(request, category_name):
#     posts = Post.objects.filter(category__name=category_name)
#     return render(request, 'travel-post-category.html', {'posts': posts})


# def post_detail(request, category_slug, post_slug):
#     post = get_object_or_404(Post, category__slug=category_slug, slug=post_slug)
#     return render(request, 'postdetails.html', {'post': post})


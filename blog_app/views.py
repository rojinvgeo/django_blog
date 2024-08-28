from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.conf import settings

# Create your views here.

def blog(request):
    travel_category = Category.objects.get(slug='travel')
    technology_category=Category.objects.get(slug='technology')
    business_category=Category.objects.get(slug='business')
    health_category=Category.objects.get(slug='health')
    fashion_category=Category.objects.get(slug='fashion')

    specific_categories = [travel_category, 
                           technology_category,
                           business_category,
                           health_category,
                           fashion_category,
                           ]
    return render(request, 'index.html',{'specific_categories': specific_categories})


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
    
    

def create_post(request):
    categories = Category.objects.all()
    author_username = request.session.get('user')
    print(f"Session user: {author_username}")
    if 'user' not in request.session:
        return HttpResponse("You must be logged in to create a post", status=403)
    post = None  # Define post variable here

    if request.session['user'] == 'admin':
        # Admin is creating the post, so proceed with admin-specific logic
        pass
    else:
        # Regular user is creating the post, so proceed with user-specific logic
        pass

    # Rest of your code here...

    # Since you don't have a User model, we'll use the auth_name directly
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        print(f"Category ID: {category_id}")
        image = request.FILES.get('image')
        created_at = request.POST.get('created_at')

        # if not category_id or not category_id.isdigit():
        #     return HttpResponse("Invalid category ID", status=400)

        # category_id = int(category_id)

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse("Category not found", status=404)

       
        # Create and save the Post instance
        post = Post(
            # auth_name=author_username,  # Use the session username directly
            title=title,
            content=content,
            category=category,
            image=image,
            created_at=created_at,
            author=request.user 
        )
        post.save()

        # Add the post instance to the context dictionary
    context = {
        'post': post,
        'categories': categories
    }

        # return HttpResponse('success') 

    # Render the admin page with categories
    # categories = Category.objects.all()
    return render(request, 'admin_post.html', context)


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


#testing

from django.core.paginator import Paginator

def post_list_by_category(request, category_slug, page_number=1):
    
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)
    admin_username = request.session.get('user',  'Unknown')  # Retrieve the admin's username from the session
    # current_author = request.user.username if request.user.is_authenticated else request.session.get('admin_user')
    for post in posts:
        print('POST IMAGE', post.image.url)  # Print the image URL
        post.author_name = admin_username

    # admin_username = request.session.get('user')  # Get the admin's username from the session
    # author_username = request.user.username if request.user.is_authenticated else 'Guest'
    image_urls = [post.image.url for post in posts]
    context = {
        'posts': posts,
        'category': category,
        'image_urls': image_urls,
        'page_obj':page_obj,
        'url_path': request.path  # Pass the URL path to the template
        #  'author_name': admin_username
    }
    for i in posts:
        print(i.author.username)
    return render(request, 'travel-post-category.html', context)




def post_detail(request, category_slug, post_id):
    category = get_object_or_404(Category, slug=category_slug)
    post = get_object_or_404(Post, id=post_id, category=category)
    admin_username = request.session.get('user',  'Unknown')
    post.author_name = admin_username
    context = {
        'post': post,
        'category': category,
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
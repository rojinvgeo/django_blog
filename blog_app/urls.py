from django.urls import path
from . import views

urlpatterns = [
    path('',views.blog, name='blog'),
    path('blog/admin_signin',views.admin_login,name='blog/admin_signin'),
    path('blog/admin',views.blog_admin, name='blog/admin'),
    path('blog/admin/create_post',views.create_post, name='blog/admin/create_post'),
    # path('blog/category/<str:category_name>/', views.post_list_by_category, name='post_list_by_category'),
    # path('blog/category/<str:category_slug>/', views.post_list_by_category, name='post_list_by_category'),
    path('blog/category/<slug:category_slug>/', views.post_list_by_category, name='post_list_by_category'),
    path('blog/category/<slug:category_slug>/<int:post_id>/', views.post_detail, name='post_details'),
    
    # path('blog/category/<slug:category_slug>/post', views.travel_post_details, name='travel_post_details')
    # path('media/<path:path>', views.serve_media, name='serve_media'),
]

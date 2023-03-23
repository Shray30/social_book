"""register URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from custom_user import views
from django.conf import settings
from django.conf.urls.static import static
from djoser.views import TokenCreateView
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('signup', views.sign_Up_Page, name='signUpPage'),
    path('login/', views.login_Page, name='login'),
    # path('home/', views.home_Page, name='homePage'),    
    path('logout/', views.logout_Page, name='logout'),
    path('login1/', views.login_Page, name='login1'),
    path('index/', views.index_Page, name='index_Page'),
    path('', views.register, name='register'),
    path('table/', views.table, name='table'),
    path('upload/', views.upload, name='upload_books'),
    # path('media/', views.book_list, name='book_list'),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    # path('books/', bookList.as_view())
    path('media/', views.bookList, name='books'),
    path('api/books/', views.bookList_API, name='books_API'),
    path('verify/', views.code_view, name='verify_view'),
    path('table2/<str:pk>/', views.update_public_vis, name='update_public_vis')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
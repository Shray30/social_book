from django.shortcuts import redirect
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from custom_user.models import Book, CustomUser
from django.http import HttpResponse

def books_view_wrapper(view_func):
    def wrapper(request):
        print("inside wrapper")
        current_user = request.user
        print(current_user)
        user_data = CustomUser.objects.filter(email=current_user).values()
        print(user_data[0]['id'])
        user_id = user_data[0]['id']
        book_count = Book.objects.filter(user_id=user_id).count()
        print(book_count)
        if (book_count > 0):
            return view_func(request)
        else:
            return redirect('upload_books')
    print("wrapper returned")
    return wrapper

# def books_view_wrapper_API(view_func):
#     @api_view(['GET'])
#     @authentication_classes([TokenAuthentication])
#     @permission_classes([IsAuthenticated])
#     def wrapper(request):
#         print("inside wrapper")
#         current_user = request.user
#         print(current_user)
#         user_data = CustomUser.objects.filter(email=current_user).values()
#         print(user_data[0]['id'])
#         user_id = user_data[0]['id']
#         book_count = Book.objects.filter(user_id=user_id).count()
#         if (book_count > 0):
#             return view_func()
#         else:
#             return redirect('upload_books')
#     return wrapper
import json
from django.shortcuts import redirect, render, HttpResponse
import requests
from custom_user.models import CustomUser, Book, Code
from django.contrib.auth import authenticate, login, logout
from custom_user.managers import CustomUserManager
from sqlalchemy import JSON, MetaData, Table, create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from custom_user.wrappers import books_view_wrapper
from custom_user.forms import CodeForm
from .serializers import MyModelSerializer
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from django.core.mail import send_mail 
# Create your views here.
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            return HttpResponse('Password Mismatch!!')
        else:
            response = requests.post('http://127.0.0.1:8000/api/v1/users/', data={'email': email, 'password': password1})
            print(response)
            en = CustomUser.objects.get(email=email)
            is_staff = request.POST.get('is_staff')
            is_active = request.POST.get('is_active')
            public_visibility = request.POST.get('public_visibility')
            address = request.POST.get('Address')
            birthdate = request.POST.get('birthdate')
            number = request.POST.get('Phone_Number')
            en.public_visibility = public_visibility
            en.address = address
            en.birthdate = birthdate
            en.number = number
            en.save()
            return redirect('login1')
        # else:
        #     en = CustomUser(email=email, password=password1, public_visibility=public_visibility, address=address, birthdate=birthdate, number=number)
        #     # my_User = User.objects.create_user(user_Name, email, password1)
        #     # my_User.save()
        #     en.save()
        #     return render(request, 'login1.html')
    return render(request, 'register.html')

def upload(request):
    print(request.user)
    current_user = request.user
    if request.method == 'POST':
        current_user = request.user
        print(current_user)
        uploaded_file = request.FILES['book']
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        visibility = request.POST.get('visibility')
        cost = request.POST.get('cost')
        year_of_publish = request.POST.get('year_published')
        user_data = CustomUser.objects.filter(email=current_user).values()
        user_id = user_data[0]['id']
        en = Book(title=title, author=author, book=uploaded_file, description=description, visibility=visibility, cost=cost, year_of_published=year_of_publish, user_id=user_id)
        en.save()
        return redirect('index_Page')
    return render(request, 'upload_books.html')

def login_Page(request):  
    if request.method == 'POST':
        print("hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        print(email, pass1)
        mydata = CustomUser.objects.filter(email=email).values()
        print(mydata[0]['email'])
        response = requests.post('http://127.0.0.1:8000/api/v1/token/login/', data={'email': email, 'password': pass1})
        print(response.json())
        user = authenticate(email=email, password=pass1)
        print(user)
        if user is not None:
            login(request, user)   
            print(request.user) 
            send_mail(
                'Testing Mail',
                'You have successfully logged in',
                'fortestme2310@gmail.com',
                [email],
                fail_silently=False
            )
            return render(request, 'index.html')
        else:
            print("Not authenticated")
        # if mydata[0]['email'] == email and mydata[0]['password'] == pass1:
        # return redirect('verify_view')
        # return render(request, 'index.html')
        # else:
            return HttpResponse('Authentication Failed!!')
        # user = authenticate(email=email, password=pass1)
        # if user is not None:
        #     login(request, user)
        #     # return redirect('index_Page')
        
    else: 
        engine = create_engine("postgresql+psycopg2://postgres:postgre123@localhost:5432/postgres")
        metadata = MetaData()
        metadata.bind = engine
        users_table = Table('custom_user_customuser', metadata, autoload_with=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        data = session.query(users_table).all()
        mail = []
        address = []
        number = []
        for n in data:
            mail.append(n.email)
            address.append(n.address)
            number.append(n.number)
        dic = {"Email": mail, "Address": address, "Number": number} 
        df = pd.DataFrame(dic)
        filtered_df = df[(df['Address'] == "kothrud") & (df['Email'].str.startswith('s'))]
        df['Address'].replace('fd', 'Wakad', inplace=True)
        dic2 = {"Email": ['abhishek@gmail.com', 'aryan@gmail.com'], "Address": ['Pune', 'Pune'], "Number": [7896541220, 7412589635]}
        df2 = pd.DataFrame(dic2)
        new_df = df.append(df2, ignore_index=True)
        print(new_df)
        return render(request, 'login1.html',)

def logout_Page(request):
    logout(request)
    return redirect('login')

def index_Page(request):
    return render(request, 'index.html')

def table(request):
    # table_data = CustomUser.objects.all()
    table_data = CustomUser.objects.filter(public_visibility=1)
    context = {
        'table_data': table_data
    }
    for n in table_data:
        print(n.email)
    return render(request, 'authors_and_sellers.html', context)

# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def book_list(request):
#     print(request.user)
#     data = Book.objects.all()
#     return render(request, 'book_list.html', {
#         'data': data
#     })

# class bookList(APIView):
#     print("xyz")
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

@books_view_wrapper
def bookList(request):
    print("Iam joddd")
    current_user = request.user
    print(current_user)
    user_data = CustomUser.objects.filter(email=current_user).values()
    user_id = user_data[0]['id']
    my_objects = Book.objects.filter(user_id=user_id)
    print(my_objects)
    serializer = MyModelSerializer(my_objects, many=True)
    return render(request, 'book_list.html', {
        'data': my_objects
    })

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookList_API(request):
    print("Iam joddd")
    current_user = request.user
    print(current_user)
    user_data = CustomUser.objects.filter(email=current_user).values()
    user_id = user_data[0]['id']
    my_objects = Book.objects.filter(user_id=user_id)
    serializer = MyModelSerializer(my_objects, many=True)
    return render(request, 'book_list.html', {
        'data': my_objects
    })

def code_view(request):
    form = CodeForm(request.POST or None)
    # user_data = CustomUser.objects.filter(email=request.user).values()
    # user_id = user_data[0]['id']
    # if user_id:
    #     user = Code.objects.filter(user_id=user_id)
    #     user_code = user[0]['number']
    pk = request.session.get('PK')
    print(pk)
    if pk:
        user = CustomUser.objects.get(pk=pk) 
        code = user.code
        if not request.POST:
            print(code)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            if str(code) == num:
                code.save()
                login(request, user)
                return redirect('index_Page')
            else:
                pass
    return render(request, 'verify_view.html', {
        'form': form
    })
    
def update_public_vis(request, pk):
    print("insideeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    # user_id = request.POST.get('curr_id')
    # print(user_id)
    print(pk)
    user = CustomUser.objects.get(id=pk)
    user.public_visibility = not user.public_visibility
    print(user.public_visibility)
    user.save()
    # if request.method == 'POST':
        
    return redirect('index_Page')
import jwt as jwt
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import response, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.core.cache import cache

# from fundoo_app import api
# from django.views.decorators.http import require_POST

from rest_framework.settings import api_settings
# from django.contrib.auth.models import User
from self import self

from .Coustom_Decorator import custom_login_required
from .models import Profile, Notes, Labels, MapLabel
from .tokens import account_activation_token
from .forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.shortcuts import render, HttpResponse, redirect
from rest_framework import generics

from . import models
# from . import serializers
from .redis_services import redis_info

from django.contrib.auth import get_user_model

User = get_user_model()


# def home(request):
#     return render(request, 'fundoo/home.html')  # renders the login page


def dash_board1(request):
    return render(request, 'fundoo/dash_board1.html')


# def createnote(request):
#     return render(request, 'notes/createnote.html')


def index(request):
    return render(request, 'fundoo/index.html')  # renders the index page


def logout(request):
    redis_info.flush_all(self)
    return render(request, 'fundoo/logout.html')  # renders the index page


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # registration by post method
        if form.is_valid():  # checking for a validations
            user = form.save(commit=False)  # saving the form after validation
            user.is_active = False  # initializing user active false
            user.save()  # save the form to db
            # current_site = get_current_site(request)
            message = render_to_string('fundoo/account_active_email.html', {
                'user': user,
                'domain': 'http://127.0.0.1:8000/',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })  # encoding the information and attaching the token to header

            mail_subject = 'Activate your account..'  # mail subject is activate mail account
            to_email = form.cleaned_data.get('email')  # sending mail to the user entered mail address
            email = EmailMessage(mail_subject, message, to=[to_email])  # with message sending to the email
            email.send()
            messages.success(request, f'Please confirm your email to complete Registration process')
            # once sent confirm mail
            # return redirect('fundoo/account_active_sent_email.html')

            return HttpResponse(
                "please confirm your email address to complete registration process..")  # giving response link has been sent
    else:
        form = UserRegistrationForm()  # re register correctly

    return render(request, 'fundoo/register.html', {'form': form})  # rendering back to register form


def user_login(request):
    res = {
        'message': 'Something went wrong',
        'data': {},
        'success': False
    }
    try:
        username = request.POST.get('username')  # getting information from post method
        password = request.POST.get('password')  # getting information from post method

        if username is None or password is None:  # fields should not be blank
            raise Exception("username and password must be filled,should not be None...\n")
        user = authenticate(username=username, password=password)  # authenticating fields values
        print('username', user, username, password)  # printing the information
        if user:  # if a valid user
            if user.is_active:  # and user is active
                login(request, user)  # login into the page
                payload = {
                    'username': username,  # payload information
                    'password': password  # payload information
                }
                # generating jwt_token using algorithm HS256
                jwt_token = {'token': jwt.encode(payload, "secret_key", algorithm='HS256').decode()}
                j_token = jwt_token['token']
                res['message'] = "Welcome You Are Logged Successfully.."  # printing the message
                res['success'] = True  # initialize to True
                # cache.set('token', "token")  # printing the data in  cache set
                redis_info.set_token(self, 'token', j_token)
                res['data'] = j_token  # storing data token
                print(res)  # printing the result
                return render(request, 'fundoo/dash_board1.html',
                              {"token": res})  # after successful login render to index.
            else:
                return HttpResponse(
                    messages.success(request, "your account is inactive"))  # else print account is inactive

        else:
            res['message'] = 'username or password is not correct'  # username or password invalid entry
            messages.error(request, 'invalid username or password')  # printing invalid entry
            return render(request, 'fundoo/login.html', context=res)  # render back to login page

    except Exception as e:  # handling exception
        print(e)
        return render(request, 'fundoo/login.html', context=res)


def get_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    print(payload)
    print(jwt_encode_handler(payload))

    return jwt_encode_handler(payload)


def user_profile(request):
    """
     This method is to create profile for user
    :param request:take Http request
    :return: redirect to profile page
    """
    print(" my profile ")
    photos = Profile.objects.all()
    # If HTTP Method POST. That means the form was submitted by a user
    if request.method == 'POST':
        # A form bound to the POST data and create instance of form by user request
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.profile)
        # If all validation rules pass
        if u_form.is_valid() and p_form.is_valid():
            # save form
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has Been Updated Successfully ')
            return redirect('fundoo/dash_board1.html')  # home
    else:
        # An unbound form
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form, 'photos': photos
    }
    return render(request, 'fundoo/login.html', context)


def activate(request, uidb64, token):
    """
    :param request: Http request
    :param uidb64: user's id encoded in base 64
    :param token: generated token for user
    :return: http response with text message
    """
    try:
        # takes user id and generates the base64 code
        uid = force_text(urlsafe_base64_decode(uidb64))
        # get user for given uid
        print(uid)
        user = User.objects.get(pk=uid)
        print(user)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        # check user is not null and has a token
    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True  # make user active
        user.save()  # save user
        login(request, user)  # make request for login
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account.')
        return redirect('user_login')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        # messages.success(request, f'Activation link is invalid!.')
        return HttpResponse('Activation link is invalid!')
    # return redirect('user_login')


@custom_login_required
@login_required
def home(request):
    allnotes = Notes.objects.all().order_by('-created_time')
    all_labels = Labels.objects.all().order_by('-created_time')

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint( allnotes)
    context = {  # 'title':title,
        # 'description':description
        'allnotes': allnotes, 'all_labels': all_labels}

    return render(request, 'notes/note_section.html', context)


def home1(request):
    response_data = {}
    allnotes = Notes.objects.all().order_by('-created_time')
    response_data['message'] = serializers.serialize('json', allnotes)
    return JsonResponse(response_data)


from django.http import JsonResponse
from django.core import serializers


@custom_login_required
def createnote(request):
    if request.method == 'POST':

        # get username and password from submitted form
        title = request.POST.get('title')
        print("title:", title)

        description = request.POST.get('description')
        print("description:", description)

        color = request.POST.get('color')
        print("color:", color)

        is_archived = request.POST.get('is_archive')
        print("is_archived:", is_archived)

        image = request.POST.get('image')
        print("image:", image)

        is_pinned = request.POST.get('is_pinned')
        print("is_pinned:", is_pinned)

        notes = Notes(title=title, description=description, color=color, is_archived=is_archived, image=image,
                      is_pinned=is_pinned)

        print(notes)
        # title and description should not be null
        if title != "" and description != "":
            # save it to database
            is_exists = Notes.objects.filter(title=title).exists()

            if is_exists is not True:
                notes.save()
            return redirect('home')
        # order notes according to it's creation time
    allnotes = Notes.objects.all().order_by('-created_time')
    context = {  # 'title':title, # 'description':description
        'allnotes': allnotes}
    return render(request, 'notes/note_section.html', context)


def deletenote(request, pk):
    if request.method == 'GET':
        # get the note with requested id
        note = Notes.objects.get(pk=pk)
        print(note.trash)
        if note.trash == False:
            note.trash = True
            note.save()
            return redirect('home')
        else:
            note.is_deleted = True
            # delete note
            note.delete()
            return redirect('show_trash')

    allnotes = Notes.objects.all().order_by('-created_time')

    context = {  # 'title':title, # 'description':description
        'allnotes': allnotes}

    return render(request, 'notes/show_trash.html', context)


def setcolor(request):
    if request.method == 'POST':
        color = request.POST.get('color')
        id = request.POST.get('id')
        note = Notes.objects.get(id=id)
        note.color = request.POST.get('color')
        print(color)
        print(id)
        note.save()

    allnotes = Notes.objects.all().order_by('-created_time')
    # all_labels = Labels.objects.all().order_by('-created_time')
    # map_labels = MapLabel.objects.all().order_by('-created_time')
    print(allnotes)
    response_data = {}
    response_data['message'] = serializers.serialize('json', allnotes)
    return JsonResponse(response_data)


def ispinned(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        note = Notes.objects.get(id=id)
        if note.is_pinned == False:
            note.is_pinned = True
            note.save()
        else:
            note.is_pinned = False
            note.save()

        response_data = {}
        allnotes = Notes.objects.all().order_by('-created_time')
        response_data['message'] = serializers.serialize('json', allnotes)
        return JsonResponse(response_data)


def isarchieve(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        note = Notes.objects.get(id=id)

        if note.is_archived == False:
            note.is_archived = True
            note.save()
        else:
            note.is_archived = False
            note.save()

        response_data = {}
        allnotes = Notes.objects.all().order_by('-created_time')
        response_data['message'] = serializers.serialize('json', allnotes)
        return JsonResponse(response_data)


def show_archive(request):
    allnotes = Notes.objects.all().order_by('-created_time')
    # all_labels = Labels.objects.all().order_by('-created_time')
    # map_labels = MapLabel.objects.all().order_by('-created_time')
    print(allnotes)
    context = {  # 'title':title,
        # 'description':description
        'allnotes': allnotes}
    return render(request, 'notes/show_archive.html', context)


def show_trash(request):
    allnotes = Notes.objects.all().order_by('-created_time')
    # all_labels = Labels.objects.all().order_by('-created_time')
    # map_labels = MapLabel.objects.all().order_by('-created_time')
    print(allnotes)
    context = {  # 'title':title,
        # 'description':description
        'allnotes': allnotes}
    return render(request, 'notes/show_trash.html', context)


def copynote(request, pk):
    if request.method == 'GET':
        # get note with given id
        note = Notes.objects.get(pk=pk)
        # set title of requested id to new note
        title = note.title
        color = note.color
        trash = note.trash
        is_archived = note.is_archived
        image = note.image
        is_pinned = note.is_pinned
        # set description of requested id to new note
        description = note.description
        # create ojbect of new copy
        newcopy = Notes(title=title, description=description, color=color, trash=trash, is_archived=is_archived,
                        image=image, is_pinned=is_pinned)
        # save newcopy to database
        newcopy.save()
        allnotes = Notes.objects.all().order_by('-created_time')
        all_labels = Labels.objects.all().order_by('-created_time')
        map_labels = MapLabel.objects.all().order_by('-created_time')
        print(allnotes)
        context = {  # 'title':title,
            # 'description':description
            'allnotes': allnotes, 'all_labels': all_labels, 'map_labels': map_labels}
    return render(request, 'notes/note_section.html', context)


def restore(request, pk):
    if request.method == 'GET':
        # get the note with requested id
        note = Notes.objects.get(pk=pk)
        if note.trash == True:
            note.trash = False
            note.save()

        return redirect('home')

    allnotes = Notes.objects.all().order_by('-created_time')
    all_labels = Labels.objects.all().order_by('-created_time')
    map_labels = MapLabel.objects.all().order_by('-created_time')
    print(allnotes)
    context = {  # 'title':title,
        # 'description':description
        'allnotes': allnotes, 'all_labels': all_labels, 'map_labels': map_labels}
    return render(request, 'notes/note_section.html', context)


def create_label(request):
    if request.method == 'POST':

        # get note id and label name from submitted form
        label_name = request.POST.get('labels')
        print(label_name)
        label = Labels(label_name=label_name)
        # label names should not be null
        if label_name != "":
            # save it to database
            label.save()
            return redirect('home')
        # order notes according to it's creation time
    all_labels = Labels.objects.all().order_by('-created_time')

    context = {  # 'title':title,
        # 'description':description
        'all_labels': all_labels}
    return render(request, 'notes/note_section.html', context)


# method to delete label
def delete_label(request, pk):
    if request.method == 'GET':
        # get label id
        label = Labels.objects.get(pk=pk)
        # delete label
        label.delete()
        return redirect('home')
        # order notes according to it's creation time
    allnotes = Notes.objects.all().order_by('-created_time')
    print(allnotes)
    context = {  # 'title':title,
        # 'description':description
        'allnotes': allnotes}
    return render(request, 'notes/note_section.html', context)


# method to update label
def update_label(request, pk):
    if request.method == 'POST':
        # get note with requested id
        label = Labels.objects.get(pk=pk)
        # set new tile to requested id
        label.label_name = request.POST.get('label_name')
        print(label.label_name)
        # set new description to requested id

        if label.label_name != "":
            # save note
            label.save()
            return redirect('home')
    allnotes = Notes.objects.all().order_by('-created_time')
    context = {  # 'title':title,
        # 'description':description
        'allnotes': allnotes}
    return render(request, 'notes/note_section.html', context)

# def addLabelOnNote(request):
#     if request.method == 'POST':
#
#         label_id = request.POST.get('label_id')
#         note_id = request.POST.get('note_id')
#         print(label_id)
#         print(note_id)
#
#         note = Notes.objects.get(id=note_id)
#         print(note)
#         label = Labels.objects.get(id=label_id)
#         # print(label)
#         #
#         # note_label=label.label_name
#         # print(label.label_name)
#
#         # note.labels.append(note_label)
#         # # note.labels = note_label
#         # note.save()
#
#         # print(label.label_name)
#         # print(note.title)
#
#
#         maplabel=MapLabel.objects.filter(note_id=note,label_id=label)
#         print(maplabel)
#         if len(maplabel) == 0:
#             obj = MapLabel(note_id=note, label_id=label)
#             obj.save()
#
#         return redirect('readallnotes')
#     return render(request,'notes/create-note.html')
#
#
# def get_label_notes(request, pk):
#         label = Labels.objects.get(pk=pk)
#         if label:
#             # print("value", label)
#             # n_id = label.note_id
#             try:
#                 L = MapLabel.objects.filter(label_id=label)
#                 # print('test', L)
#             except:
#                 return render(request, 'notes/show_label.html',[])
#
#             note_list = []
#             note_obj = []
#             for i in range(len(L)):
#                 obj = L[i]
#                 note_obj = Notes.objects.filter(title=obj)
#                 print(note_obj, '-->note_obj')
#
#                 note_list.append(note_obj)
#
#             print(note_list)
#             list=[]
#             for j in range(len(note_list)):
#                 for k in range(len(note_list[j])):
#                     print((note_list[j][k]))
#                     list.append((note_list[j][k]))
#
#             all_labels = Labels.objects.all().order_by('-created_time')
#             map_labels = MapLabel.objects.all().order_by('-created_time')
#
#             context = {'list': list, 'all_labels': all_labels,'map_labels':map_labels}
#             print(type(all_labels))
#             print(list)
#         return render(request, 'notes/show_label.html', context=context)


# def copynote(request, pk):
#     if request.method == 'GET':
#         # get note with given id
#         note = Notes.objects.get(pk=pk)
#         # set title of requested id to new note
#         title = note.title
#         color = note.color
#         trash = note.trash
#         is_archived = note.is_archived
#         image = note.image
#         is_pinned = note.is_pinned
#         # set description of requested id to new note
#         description = note.description
#         # create ojbect of new copy
#         newcopy = Notes(title=title, description=description, color=color, trash=trash, is_archived=is_archived,
#                         image=image, is_pinned=is_pinned)
#         # save newcopy to database
#         newcopy.save()
#         allnotes = Notes.objects.all().order_by('-created_time')
#         all_labels = Labels.objects.all().order_by('-created_time')
#         map_labels = MapLabel.objects.all().order_by('-created_time')
#         print(allnotes)
#         context = {  # 'title':title,
#             # 'description':description
#             'allnotes': allnotes, 'all_labels': all_labels, 'map_labels': map_labels}
#     return render(request, 'notes/note_section.html', context)
#
#
# def restore(request, pk):
#     if request.method == 'GET':
#         # get the note with requested id
#         note = Notes.objects.get(pk=pk)
#         if note.trash == True:
#             note.trash = False
#             note.save()
#
#         return redirect('home')
#
#     allnotes = Notes.objects.all().order_by('-created_time')
#     all_labels = Labels.objects.all().order_by('-created_time')
#     map_labels = MapLabel.objects.all().order_by('-created_time')
#     print(allnotes)
#     context = {  # 'title':title,
#         # 'description':description
#         'allnotes': allnotes, 'all_labels': all_labels, 'map_labels': map_labels}
#     return render(request, 'notes/note_section.html', context)

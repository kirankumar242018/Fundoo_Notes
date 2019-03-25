from PIL import Image
from django import forms
# from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# from .models import CustomUser
# User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    # email = forms.EmailField()  # takes email fields
    email = forms.RegexField(regex=r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                             required=True)

    class Meta:  # gives the information of the user registration form
        model = Profile  # assigns model to user
        fields = ['username', 'email', 'password1', 'password2']  # fields of a class

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()

        return user


class LoginForm(forms.ModelForm):
    email = forms.EmailField()  # takes email fields

    class Meta:  # gives the information of the Login form
        model = Profile  # assigns model to user
        fields = ['username', 'password']  # fields of a class


# profile pic forms

class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('image', 'x', 'y', 'width', 'height',)

    """ X coordinate, Y coordinate, Height and Width of the Cropping Box  of User Profile"""

    def save(self):
        photo = super(ProfileUpdateForm, self).save()

        x = self.cleaned_data.get('x')  # X coordinate
        y = self.cleaned_data.get('y')  # Y coordinate
        w = self.cleaned_data.get('width')  # width of cropping box
        h = self.cleaned_data.get('height')  # height of cropping box

        image = Image.open(photo.file)  # opens image file using Pillow library
        cropped_image = image.crop((x, y, w + x, h + y))  # crops image with x,y,w,h
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)  # resize cropped image.
        resized_image.save(photo.image.path)
        return photo


# create form for user update
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['username', 'email']





# echo "COPYING NEW JAR FILE FROM JENKINS INSTANCE TO DEPLOYMENT INSTANCE"
# #cp -rf /var/lib/jenkins/workspace/jenkinsCICD/fundoo_app /home/ubuntu/
# scp -r /var/lib/jenkins/workspace/jenkinsCICD/fundoo_app ubuntu@172.31.21.137:/home/ubuntu/
# #sudo systemctl start nginx
# #sudo systemctl start gunicorn













# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):  # gives the information of the custom user creation form
#         # pass
#         model = Profile  # takes the model of Custom User
#         fields = ('username', 'email')  # fields of a class
#
#
# class CustomUserChangeForm(UserChangeForm):
#     class Meta:  # gives the information of the custom user change form
#         # pass
#         model = Profile  # takes the model of Custom User
#         fields = UserChangeForm.Meta.fields  # fields of a class User change form

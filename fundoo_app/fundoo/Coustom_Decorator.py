from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from self import self
from .redis_services import redis_info
import jwt
from .models import Profile


def custom_login_required(function=None, login_url=''):
    try:
        def is_login(request):

            token = redis_info.get_token(self, 'token')  # gets the token from redis cache
            print('this is my token:',token)

            token = token.decode(encoding='utf-8')  # decodes the token ( from Bytes to str )
            decoded_token = jwt.decode(token, 'secret_key',
                                       algorithms=['HS256'])  # decodes JWT token and gets the values Username etc
            user = Profile.objects.get(username=decoded_token['username']).pk  # gets the user from username
            # request.user = user

            return Profile.objects.filter(pk=user).exists()  # if user is present in DB.

        actual_decorator = user_passes_test(is_login)  # user_passes_test to check if some test passes or not

        if function:
            return actual_decorator(function)
        else:
            return redirect(reverse('user_login'))
            # return actual_decorator


    except (ObjectDoesNotExist, AttributeError, Exception) as e:
        print(e)
        return redirect(reverse('user_login'))

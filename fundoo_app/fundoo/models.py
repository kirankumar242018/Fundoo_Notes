from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse


class AccountManager(BaseUserManager):

    def create_user(self, username, email, password, firstname, lastname, **kwargs):
        # Ensure that an email address is set
        if not email:
            raise ValueError('Users must have a valid e-mail address')

        # Ensure that a username is set
        if not username:
            raise ValueError('Users must have a valid username')

        account = self.model(
            username=username,
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname
        )
        account.is_staff = False
        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):

        username = kwargs.get('username', None)
        firstname = kwargs.get('firstname', None)
        lastname = kwargs.get('lastname', None)

        if not username:
            raise ValueError('Users must have a valid username')

        if not firstname:
            raise ValueError('Users must have a First Name')

        if not lastname:
            raise ValueError('Users must have a Last Name')

        if password is None:
            raise TypeError('Superusers must have a password.')

        account = self.create_user(username, email, password, firstname, lastname, )
        account.is_superuser = True
        account.is_staff = True
        account.is_admin = True
        account.save()

        return account


class Profile(AbstractBaseUser, PermissionsMixin):
    # Each `User` needs a human-readable unique identifier that we can use to
    # represent the `User` in the UI. We want to index this column in the
    # database to improve lookup performance.
    username = models.CharField(unique=True, max_length=50)

    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(unique=True)

    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)

    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp representing when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)

    # date_created = models.DateTimeField(auto_now_add=True)
    # date_modified = models.DateTimeField(auto_now=True)

    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    # image = models.ImageField(upload_to='profile_pics', blank="TRUE", null="TRUE")
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(default=False)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    # is_active = models.BooleanField(default=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'firstname', 'lastname']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = AccountManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. If the user's real name,
        not stored we return their username instead.
        """
        return ' '.join(self.firstname, self.lastname)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    """
        This function is depricated.
    """

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


# Notes Models
class Notes(models.Model):
    # note_id = models.IntegerField(default=None,null=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    remainder = models.DateTimeField(default=None, null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    color = models.CharField(default=None, max_length=50, blank=True, null=True)
    image = models.ImageField(default=None, null=True)
    trash = models.BooleanField(default=False)
    is_pinned = models.NullBooleanField(blank=True, null=True, default=None)
    # label = models.CharField(max_length=50)
    labels = ArrayField(models.CharField(max_length=150, null=True, default=None), null=True, default=None)
    collaborate = models.ManyToManyField(Profile, related_name='collaborated_user', null=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')


# model to create label
class Labels(models.Model):
    label_name = models.CharField(max_length=150)
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.label_name


class MapLabel(models.Model):
    note_id = models.ForeignKey(Notes, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    label_id = models.ForeignKey(Labels, on_delete=models.CASCADE, null=True, blank=True, db_constraint=False)
    created_time = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.note_id)

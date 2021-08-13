from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class AccountManager(BaseUserManager):
	def create_user(self, username, firstname, lastname, email, date_of_birth, password = None):
		if not username:
			raise ValueError("EMAIL IS REQUIRED!")
		
		if not firstname:
			raise ValueError("USERNAME IS REQUIRED!")
		
		if not lastname:
			raise ValueError("LASTNAME IS REQUIRED!")
		
		if not email:
			raise ValueError("EMAIL IS REQUIRED!")
		
		if not date_of_birth:
			raise ValueError("DATE OF BIRTH IS REQUIRED!")
	
		user = self.model(
			username = username, firstname = firstname, lastname = lastname, 
			email = self.normalize_email(email), date_of_birth = date_of_birth
			)
		
		user.set_password(password)
		user.save(using = self._db)
		return user
	

	def create_superuser(self, username, firstname, lastname, email, date_of_birth, password = None):
		user = self.create_user(
			 username = username, firstname = firstname, lastname = lastname, 
			 email = self.normalize_email(email), date_of_birth = date_of_birth
		)

		user.is_admin = True
		user.is_superuser = True
		user.is_staff = True

		user.set_password(password)
		user.save(using = self._db)
		return user
		
		

class Account(AbstractBaseUser):
	username = models.CharField(verbose_name = "username", max_length = 255, unique = True)
	firstname = models.CharField(verbose_name = "firstname", max_length = 255)
	lastname = models.CharField(verbose_name = "lastname", max_length = 255)
	email = models.EmailField(verbose_name = "email", max_length = 255, unique = True)
	date_of_birth = models.DateField()

	friends = models.ManyToManyField('Account',blank=True)

	date_joined = models.DateTimeField(verbose_name = "date_joined", auto_now_add = True)
	last_login = models.DateTimeField(verbose_name = "last_login", auto_now = True)

	is_admin = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)

	USERNAME_FIELD = "username"
	REQUIRED_FIELDS = ['firstname', 'lastname', 'email', 'date_of_birth']
	objects = AccountManager()


	def __str__(self):
		return str(self.username)

	def has_perm(self, perm, obj = None):
		return True
	
	def has_module_perms(self, app_label):
		return True


class FriendRequest(models.Model):
	sender_account = models.ForeignKey(Account, related_name="sender_account", on_delete=models.CASCADE)
	receiver_account = models.ForeignKey(Account, related_name="receiver_account", on_delete=models.CASCADE)


	def __str__(self):
		return (f'{self.sender_account.username} to {self.receiver_account}')


class PublicMessage(models.Model):
    sender = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
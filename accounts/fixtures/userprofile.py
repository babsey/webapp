from django.contrib.auth.models import User
from accounts.models import UserProfile, Group

userAdmin = User.objects.get(pk=1)
userAdmin.first_name = 'Big'
userAdmin.last_name = 'Boss'
userAdmin.save()

profileAdmin,created = UserProfile.objects.get_or_create(user_id=userAdmin.pk)
if created: print('Profile for admin created.')

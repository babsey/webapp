from accounts.models import UserProfile, Group

groupAdmin,created = Group.objects.get_or_create(**{
    'member_title': u'Admin',
    'priority': 1,
    'slug': u'Admin',
    'title': u'Admin',
})
if created: print('Forum group for admin created.')

profileAdmin = UserProfile.objects.get(id=1)
profileAdmin.forum_group_id = groupAdmin.pk
profileAdmin.save()

_,created = Group.objects.get_or_create(**{
    'member_title': u'Moderator',
    'priority': 2,
    'slug': u'Moderator',
    'title': u'Moderator',
})
if created: print('Forum group for moderator created.')

_,created = Group.objects.get_or_create(**{
    'is_default': True,
    'member_title': u'Member',
    'priority': 3,
    'slug': u'Member',
    'title': u'Member',
})
if created: print('Forum group for member created.')

_,created = Group.objects.get_or_create(**{
    'is_anonymous': True,
    'member_title': u'Guest',
    'priority': 4,
    'slug': u'Guest',
    'title': u'Guest',
})
if created: print('Forum group for guest created.')

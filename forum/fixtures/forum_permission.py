from accounts.models import Group
from forum.models import Forum, Permission

forumGeneral,created = Forum.objects.get_or_create(name='General', description='This is a general forum.')
if created: print('Forum category `General` created.')

_,created = Permission.objects.get_or_create(**{
    'can_add_own_post': True,
    'can_add_own_topic': True,
    'can_change_group_post': True,
    'can_change_group_topic': True,
    'can_change_own_post': True,
    'can_change_own_topic': True,
    'can_close_group_topic': True,
    'can_close_own_topic': True,
    'can_delete_group_post': True,
    'can_delete_group_topic': True,
    'can_delete_own_post': True,
    'can_delete_own_topic': True,
    'can_move_group_post': True,
    'can_move_group_topic': True,
    'can_split_group_topic': True,
    'can_stick_group_topic': True,
    'forum_id': forumGeneral.pk,
    'group_id': Group.objects.get(member_title='Admin').id,
})
if created: print('Permission for admin created.')

_,created = Permission.objects.get_or_create(**{
    'can_add_own_post': True,
    'can_add_own_topic': True,
    'can_change_group_post': True,
    'can_change_group_topic': True,
    'can_change_own_post': True,
    'can_change_own_topic': True,
    'can_close_group_topic': True,
    'can_close_own_topic': True,
    'can_delete_group_post': True,
    'can_delete_group_topic': True,
    'can_delete_own_post': True,
    'can_delete_own_topic': True,
    'can_move_group_post': True,
    'can_move_group_topic': True,
    'can_split_group_topic': True,
    'can_stick_group_topic': True,
    'forum_id': forumGeneral.pk,
    'group_id': Group.objects.get(member_title='Moderator').id,
})
if created: print('Permission for moderator created.')

_,created = Permission.objects.get_or_create(**{
    'can_add_own_post': True,
    'can_add_own_topic': True,
    'can_change_own_post': True,
    'can_change_own_topic': True,
    'can_close_own_topic': True,
    'can_delete_own_post': True,
    'can_delete_own_topic': True,
    'forum_id': forumGeneral.pk,
    'group_id': Group.objects.get(member_title='Member').id,
})
if created: print('Permission for member created.')

_,created = Permission.objects.get_or_create(**{
    'forum_id': forumGeneral.pk,
    'group_id': Group.objects.get(member_title='Guest').id,
})
if created: print('Permission for guest created.')


forumGeneral,created = Forum.objects.get_or_create(name='Team', description='This is a category for team.')
if created: print('Forum category `Team` created.')

_,created = Permission.objects.get_or_create(**{
    'can_add_own_post': True,
    'can_add_own_topic': True,
    'can_change_group_post': True,
    'can_change_group_topic': True,
    'can_change_own_post': True,
    'can_change_own_topic': True,
    'can_close_group_topic': True,
    'can_close_own_topic': True,
    'can_delete_group_post': True,
    'can_delete_group_topic': True,
    'can_delete_own_post': True,
    'can_delete_own_topic': True,
    'can_move_group_post': True,
    'can_move_group_topic': True,
    'can_split_group_topic': True,
    'can_stick_group_topic': True,
    'forum_id': forumGeneral.pk,
    'group_id': Group.objects.get(member_title='Admin').id,
})
if created: print('Permission for admin created.')

_,created = Permission.objects.get_or_create(**{
    'can_add_own_post': True,
    'can_add_own_topic': True,
    'can_change_group_post': True,
    'can_change_group_topic': True,
    'can_change_own_post': True,
    'can_change_own_topic': True,
    'can_close_group_topic': True,
    'can_close_own_topic': True,
    'can_delete_group_post': True,
    'can_delete_group_topic': True,
    'can_delete_own_post': True,
    'can_delete_own_topic': True,
    'can_move_group_post': True,
    'can_move_group_topic': True,
    'can_split_group_topic': True,
    'can_stick_group_topic': True,
    'forum_id': forumGeneral.pk,
    'group_id': Group.objects.get(member_title='Moderator').id,
})
if created: print('Permission for moderator created.')

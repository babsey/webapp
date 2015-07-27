from accounts.models import UserProfile
from forum.models import Forum, Topic, Post

profileAdmin = UserProfile.objects.get(user__id=1)
forumGeneral = Forum.objects.get(id=1)
forumTeam = Forum.objects.get(id=1)

topic,created = Topic.objects.get_or_create(**{
    'forum_id': forumGeneral.pk,
    'name': 'It worked!',
})

open_post,created = Post.objects.get_or_create(**{
    'topic_id': topic.pk,
    'profile_id': profileAdmin.pk,
    'message': 'Congratulation on your first django-based, bootstrapped forum.',
    'message_html': 'Congratulation on your first django-based, bootstrapped forum.',
})

post,created = Post.objects.get_or_create(**{
    'topic_id': topic.pk,
    'profile_id': profileAdmin.pk,
    'message': 'This topic is already closed.',
    'message_html': 'This topic is already closed.',
})

topic.first_post_id = open_post.pk
topic.last_post_id = post.pk
topic.posts_count = 3
topic.is_closed = True
topic.save()

topic,created = Topic.objects.get_or_create(**{
    'forum_id': forumTeam.pk,
    'name': 'Tutorial',
})

open_post,created = Post.objects.get_or_create(**{
    'topic_id': topic.pk,
    'profile_id': profileAdmin.pk,
    'message': 'This is a tutorial for moderator or administrator.',
    'message_html': 'This is a tutorial for moderator or administrator.',
})

post,created = Post.objects.get_or_create(**{
    'topic_id': topic.pk,
    'profile_id': profileAdmin.pk,
    'message': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
    'message_html': 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.',
})

topic.first_post_id = open_post.pk
topic.last_post_id = post.pk
topic.posts_count = 2
topic.is_closed = True
topic.is_sticky = True
topic.save()

from django.contrib.sites.models import Site

site = Site.objects.get(id=1)
site.domain = '127.0.0.1:8000'
site.name = 'localhost'
site.save()

from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

urls = ['/', '/about/', '/faq/', '/contact/', '/network/', '/network/1/1/solution/']
titles = ['nuSPIC Home', 'About nuSPIC', 'FAQ', 'Contact', 'Competition', 'Hodgkin-Huxley Solution']
files = ['mainpage', 'about', 'faq', 'contact', 'network', 'hodgkin-huxley_solution']

for idx in range(len(urls)):
    with open('webapp/fixtures/templates/%s.html' %files[idx], 'r') as f:
        content = ''.join(f.readlines())
        flatpage,created = FlatPage.objects.get_or_create(**{
            'url': urls[idx],
            'title': titles[idx],
            'content': content
        })
        flatpage.sites.add(Site.objects.get(pk=1))
        flatpage.save()

from django.contrib import admin
from models import Network
from reversion.admin import VersionAdmin

class NetworkAdmin(VersionAdmin):
    """
    A childclass of VersionAdmin, its neccessary to create versions.
    Check, if 'reversion' module is in INSTALLED_APP.
    """
    
    list_display = (
        '__unicode__',
        #'neurons',
        #'inputs',
        #'outputs'
        )
    list_filter = ['SPIC_id']

try:
    admin.site.register(Network, NetworkAdmin)
except:
    admin.site.register(Network)
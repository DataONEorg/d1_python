import os
import sys

# Discover the path of this module
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

os.environ['DJANGO_SETTINGS_MODULE'] = 'service.gmn.settings'

#sys.path.append(_here('.'))
# Add the service folder to the search path.
sys.path.append(_here('.'))
sys.path.append(_here('..'))

#import d1wsgihandler
#application = d1wsgihandler.D1WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

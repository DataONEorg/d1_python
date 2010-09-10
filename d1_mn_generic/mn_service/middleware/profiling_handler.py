from django.http import HttpResponse
import hotshot, hotshot.stats
import sys, StringIO, os


class ProfileMiddleware():
  def __init__(self):
    pass

  def process_view(self, request, view, *args, **kwargs):
    for item in request.META['QUERY_STRING'].split('&'):
      if item.split('=')[0] == 'profile': # profile in query string
        # catch the output, must happen before stats object is created
        # see https://bugs.launchpad.net/webpy/+bug/133080 for the details
        std_old, std_new = sys.stdout, StringIO.StringIO()
        sys.stdout = std_new

        # now let's do some profiling
        request.session['profile'] = 1 #just to set the sessionid variable in cookie.
        tmpfile = '/tmp/%s' % request.COOKIES['sessionid']
        prof = hotshot.Profile(tmpfile)

        # make a call to the actual view function with the given arguments
        response = prof.runcall(view, request, *args[0], **args[1])
        prof.close()

        # and then statistical reporting
        stats = hotshot.stats.load(tmpfile)
        stats.strip_dirs()
        stats.sort_stats('time')

        # do the output
        stats.print_stats(1.0)

        # restore default output
        sys.stdout = std_old

        # delete file
        os.remove(tmpfile)

        return HttpResponse('<pre>%s</pre>' % std_new.getvalue())

    return None

# # -*- coding: utf-8 -*-
#
# # This work was created by participants in the DataONE project, and is
# # jointly copyrighted by participating institutions in DataONE. For
# # more information on DataONE, see our web site at http://dataone.org.
# #
# #   Copyright 2009-2016 DataONE
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #   http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# """Performance profiling middleware
#
# When this profiling middleware is enabled, a client can request a detailed
# profiling report by adding a header with the name HTTP_VENDOR_PROFILE_PYTHON.
# GMN will then process the request as normal, but return the profiling report
# instead of the actual result.
# """
#
# import os
# import io
# import sys
#
# # import hotshot
# # import hotshot.stats
#
# import django.conf
# import django.core.exceptions
# # Django.
# from django.http import HttpResponse
#
#
# class ProfilingHandler:
#   def __init__(self, next_in_chain_func):
#     # Disable this middleware layer if Django is not running in debug mode.
#     if not django.conf.settings.DEBUG:
#       raise django.core.exceptions.MiddlewareNotUsed
#     self.next_in_chain_func = next_in_chain_func
#
#   def __call__(self, request):
#     self.next_in_chain_func(request)
#
#   # noinspection PyUnusedLocal
#   def process_view(self, request, view_func, view_args, view_kwargs):
#   # def __call__(self, request, view_func, *view_args, **view_kwargs):
#     # This middleware layer is disabled if Django is not running in debug mode
#     # (see __init__()).
#
#     # If profiling is not requested, resume normal processing.
#     if 'HTTP_VENDOR_PROFILE_PYTHON' not in request.META:
#       # Returning None causes he regular view handler to be called.
#       return None
#
#     # Call view with profiling.
#
#     # Catch the output, must happen before stats object is created.
#     # See https://bugs.launchpad.net/webpy/+bug/133080 for the details.
#     std_old, std_new = sys.stdout, io.StringIO()
#     sys.stdout = std_new
#
#     # Path for storing the profiling data.
#     tmpfile = os.tempnam()
#
#     # # Profile the view.
#     # prof = hotshot.Profile(tmpfile)
#     # prof.runcall(view, request, *args[0], **args[1])
#     # prof.close()
#     #
#     # # Parse the profiler results and generate report.
#     # stats = hotshot.stats.load(tmpfile)
#     # stats.strip_dirs()
#     # stats.sort_stats('time')
#     # stats.print_stats(1.0)
#
#     # Restore default output.
#     sys.stdout = std_old
#
#     # Delete the profiling data.
#     os.remove(tmpfile)
#
#     # Return the profiler report. This prevents the regular view
#     # handler from being called.
#     return HttpResponse('<pre>%s</pre>' % std_new.getvalue(), 'text/plain')

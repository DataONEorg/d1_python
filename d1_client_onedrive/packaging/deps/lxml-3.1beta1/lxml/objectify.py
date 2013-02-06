def __bootstrap__():
   global __bootstrap__, __loader__, __file__
   
   import sys, pkg_resources, imp, platform
   
   uname = platform.uname()
   
   if uname[0] == 'Darwin':
       __file__ = pkg_resources.resource_filename(__name__,
                                                'resources/macosx/objectify.dylib')
   elif uname[0] == 'Linux':
       
     if uname[4] == 'x86_64':  
         __file__ = pkg_resources.resource_filename(__name__,
                                                'resources/linux/x86_64/objectify.so')
     else:
         raise Exception("Unknown supported: "+str(uname))
       
   elif uname[0] == 'Windows':
       
       if uname[4] == 'AMD64':
           __file__ = pkg_resources.resource_filename(__name__,
                                                'resources/windows/amd64/objectify.pyd')
       else:
         raise Exception("Unknown supported: "+str(uname))
     
   else:
       raise Exception("Unknown supported: "+str(uname))
   
  
   __loader__ = None; del __bootstrap__, __loader__
   imp.load_dynamic(__name__,__file__)
__bootstrap__()

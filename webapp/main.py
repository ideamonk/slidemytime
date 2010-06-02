#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db

from models import Screengrabs
import helpers

class MainHandler(webapp.RequestHandler):
    def get(self,imagename):
        if imagename!="":
            try:
                q = Screengrabs.all()
                q.filter("imagename =",imagename)
                screengrabs = q.fetch(1)
                for screengrab in screengrabs:
                    if screengrab.imgdata:
                        self.response.headers['Content-Type'] = "image/jpeg"
                        self.response.out.write(screengrab.imgdata)
                        return
            except:
                pass
        
        # render banner page
        helpers.render (self, 'index.html', {})

    def post(self,foobar):
      #TODO: protect uploads <--> trust b/w clients and servers <--> Oauth,
      # secret, etc
        imgdata = self.request.get("img")
        screengrabs = Screengrabs()
        screengrabs.imgdata = db.Blob(imgdata)
        randomname = helpers.shortify() 
        screengrabs.imagename = randomname
        screengrabs.put()
        self.response.out.write("[ '%s', '%s' ]" % 
                                         (screengrabs.key(), randomname))

class CleanHandler(webapp.RequestHandler):
    # TODO: TBD
    def get(self):
        q = Screengrabs.all()
        results = q.fetch(100)
        for result in results:
            result.delete()
        return

def main():
    application = webapp.WSGIApplication(
        [
            ('/cleaner', CleanHandler),
            (r'/(.*)', MainHandler)
        ], debug=False)
    wsgiref.handlers.CGIHandler().run(application)



if __name__ == '__main__':
    main()

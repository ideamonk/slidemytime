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
from google.appengine.api import users

from models import Screengrabs, SlideStats, Machines
import helpers

import datetime

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
        if users.is_current_user_admin():
            self.redirect("/home")

        user = users.get_current_user()
        values = { 'login_url': users.create_login_url(self.request.uri) }
        values.update( {'is_not_logged_in': user == None} )
        values.update( {'is_admin':False} )
        if user:
          values.update( {'nick':user.nickname()} )
        helpers.render(self, 'index.html', values)

    def post(self,foobar):
        #TODO: protect uploads <--> trust b/w clients and servers <--> Oauth,
        # secret, etc
        # Hobbes` oneliner
        # echo "http://slidemytime.appspot.com/"` curl -sF "img=@foo.png;type=image/png" http://slidemytime.appspot.com/posthere`

        imgdata = self.request.get("img")
        self.response.out.write( len(imgdata) )
        return
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



class HomeHandler(webapp.RequestHandler):
    def get(self, pagename=None):
        if not users.is_current_user_admin():
            self.redirect("/")

        values={}
        values.update( {'logout_url':users.create_logout_url("/")} )

        if pagename in ['','/', None]:
            # ---------------------------------------------------------------
            #    Overview Page
            # ---------------------------------------------------------------
            values.update( helpers.get_storage_stats() )

            # storage stats
            total_micro = int((float(values['total_kbytes']) / 1024**2)*100)
            values.update( {'total_micro': range(total_micro)} )
            values.update( {'remaining_micro': range(100-total_micro)} )

            # misc over stats
            values.update( {'total_snaps': Screengrabs.all().count()} )

            try:
                date_start = Screengrabs.all().order('date').fetch(1)[0].date
            except:
                date_start = 'an unknown time in the past'

            try:
                date_stop = Screengrabs.all().order('-date').fetch(1)[0].date
            except:
                date_stop = 'an unknown time in the future'

            date_diff = date_stop-date_start
            values.update( {'total_days':date_diff.days})
            values.update( {'total_hours':date_diff.seconds/3600})
            values.update( {'total_minutes':(date_diff.seconds/60)%60})

            values.update( {'date_start':date_start.strftime('%F %H:%M:%S')} )
            values.update( {'date_stop':date_stop.strftime('%F %H:%M:%S')} )

            helpers.render(self, "overview.html",values)
            return



def main():
    application = webapp.WSGIApplication(
        [
            ('/cleaner', CleanHandler),
            ('/home(.*)', HomeHandler),
            (r'/(.*)', MainHandler)
        ], debug=False)
    wsgiref.handlers.CGIHandler().run(application)



if __name__ == '__main__':
    main()

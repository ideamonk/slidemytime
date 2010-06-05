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
            q = Screengrabs.all()
            if len(imagename) == 6:
                q.filter("imagename =",imagename[1:])
            else:
                q.filter("imagename =", imagename)

            screengrabs = q.fetch(1)
            for screengrab in screengrabs:
                if screengrab.imgdata:
                    self.response.headers['Content-Type'] = "image/jpeg"
                    if len(imagename)==6:
                        self.response.out.write(screengrab.thumbdata)
                    else:
                        self.response.out.write(screengrab.imgdata)
                    return
            #except:
            #    pass

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
        thumbdata = self.request.get("thumb")
        passphrase = self.request.get("passphrase")

        machines = Machines.all().filter("passphrase =",passphrase).fetch(1)
        for machine in machines:
            if machine.enabled:
                screengrabs = Screengrabs()
                screengrabs.imgdata = db.Blob(str(imgdata))
                screengrabs.thumbdata = db.Blob(thumbdata)
                screengrabs.machine = str(machine.key())
                randomname = helpers.shortify()
                screengrabs.imagename = randomname
                screengrabs.size = len(imgdata) + len(thumbdata)
                screengrabs.put()
                slide_stat = SlideStats.all().fetch(1)[0]
                slide_stat.total_snaps += 1
                slide_stat.total_size += screengrabs.size/1024
                slide_stat.put()
                self.response.out.write("[ '%s', '%s' ]" %
                                    (screengrabs.key(), randomname))



class CleanHandler(webapp.RequestHandler):
    # TODO: TBD
    def get(self):
        if not users.is_current_user_admin():
            self.redirect("/")

        q = Screengrabs.all()
        results = q.fetch(1000)
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
            slide_stat = SlideStats.all().fetch(1)[0]

            values.update( {'total_size':slide_stat.total_size} )

            # storage stats
            total_micro = int((float(values['total_size']) / 1024**2)*100)
            values.update( {'total_micro': range(total_micro)} )
            values.update( {'remaining_micro': range(100-total_micro)} )

            # misc over stats
            values.update( {'total_snaps': slide_stat.total_snaps} )

            try:
                date_start = Screengrabs.all().order('date').fetch(1)[0].date
            except:
                pass

            try:
                date_stop = Screengrabs.all().order('-date').fetch(1)[0].date
            except:
                pass

            try:
                date_diff = date_stop-date_start
                values.update( {'total_days':date_diff.days})
                values.update( {'total_hours':date_diff.seconds/3600})
                values.update( {'total_minutes':(date_diff.seconds/60)%60})
                values.update( {'date_start':date_start.strftime('%F %H:%M:%S')} )
                values.update( {'date_stop':date_stop.strftime('%F %H:%M:%S')} )
            except:
                values.update( {'date_stop':'a time unknown'} )
                values.update( {'date_start':'a time never known'} )

            helpers.render(self, "overview.html",values)
            return

        if pagename in ['/machines','/machines/']:
            # ---------------------------------------------------------------
            #    Machines Page
            # ---------------------------------------------------------------
            total_machines = Machines.all().count()
            values.update ( {'total_machines': total_machines} )

            if total_machines>0:
                values.update({'machines_start':Machines.all().order('created').fetch(1)[0].created})
                values.update( {'machines':Machines.all().fetch(1000)} )
            else:
                values.update({'machines_start':'a time unknown'})

            helpers.render(self, "machines.html",values)
            return

        if pagename in ['/machines/delete/','/machines/delete']:
            #
            #    Machines_delete
            #
            _key=self.request.get('key')
            machine = db.get(_key)
            machine.delete()
            self.redirect("/home/machines")

        if pagename in ['/machines/disable/','/machines/disable']:
            #
            #    Machines_disable
            #
            _key=self.request.get('key')
            machine = db.get(_key)
            machine.enabled=False
            db.put(machine)
            self.redirect("/home/machines")

        if pagename in ['/machines/enable/','/machines/enable']:
            #
            #    Machines_enable
            #
            _key=self.request.get('key')
            machine = db.get(_key)
            machine.enabled=True
            machine.put()
            self.redirect("/home/machines")

        if pagename in ['/history','/history/']:
            # ---------------------------------------------------------------
            #    History Page
            # ---------------------------------------------------------------
            slide_count=100
            try:
                slide_count = int(self.request.get('count'))
            except ValueError:
                self.redirect ('/home/history?count=100')

            if slide_count<1:
                self.redirect ('/home/history?count=100')

            screengrabs = Screengrabs.all().fetch(slide_count)
            if len(screengrabs) < slide_count:
                slide_count = len(screengrabs)

            values.update ( {'screengrabs':screengrabs} )
            values.update ( {'slide_count':slide_count} )

            helpers.render(self, "history.html",values)
            return

    def post(self, pagename=None):
        if not users.is_current_user_admin():
            self.redirect("/")

        if pagename == '/machines/add':
            # ---------------------------------------------------------------
            #    Machines_add
            # ---------------------------------------------------------------
            name = self.request.get('name')
            machine = Machines(name=name, enabled=True, passphrase=helpers.gimme_garbage(12))
            machine.put()

            self.redirect('/home/machines')



def main():
    # First run check
    if SlideStats.all().count() == 0:
        s = SlideStats()
        s.total_snaps = 0
        s.total_size = 0
        s.put()

    application = webapp.WSGIApplication(
        [
            ('/cleaner', CleanHandler),
            (r'/home(.*)', HomeHandler),
            (r'/(.*)', MainHandler)
        ], debug=False)
    wsgiref.handlers.CGIHandler().run(application)



if __name__ == '__main__':
    main()

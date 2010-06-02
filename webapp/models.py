from google.appengine.ext import db

class Screengrabs(db.Model):
   imgdata = db.BlobProperty()
   imagename = db.StringProperty()
   date = db.DateTimeProperty(auto_now_add=True)

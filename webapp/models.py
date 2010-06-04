from google.appengine.ext import db

class Screengrabs(db.Model):
   imgdata = db.BlobProperty()
   imagename = db.StringProperty()
   date = db.DateTimeProperty(auto_now_add=True)
   size = db.IntegerProperty()

class SlideStats(db.Model):
    total_snaps = db.IntegerProperty()
    total_size = db.IntegerProperty()

class Machines(db.Model):
    name = db.StringProperty()
    enabled = db.BooleanProperty()
    passphrase = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
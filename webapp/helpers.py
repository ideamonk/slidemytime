''' misc helper code '''
import random
import os
from google.appengine.ext.webapp import template
from google.appengine.ext.db import stats

T_PATH = os.path.join(os.path.dirname(__file__),'views')

def shortify():
    ''' some estimates on 4 letter shorties
        -----------------------------------
        >>> len('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        62
        >>> 62**4                            # 4 letter shorturl
        14776336                             # these many images
        >>> ((62**4) * 2)                    # each after 2 minutes say...
        29552672                             # can work for these many minutes
        >>> ((62**4) * 2) / 60 / 24
        20522                                # can sustain for these many days
        >>> ((62**4) * 2) / 60 / 24 / 365    # how many year?
        56                                   # 56 years good enough ?!
        # want more? take snap every 5 minutes = 140 years

        Format - i****
    '''
    return 'i' + ''.join(random.sample('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', 4))

def render(req, view, values):
    view_path = os.path.join(T_PATH, view)
    req.response.out.write( template.render(view_path,values) )

def get_storage_stats():
    global_stat = stats.GlobalStat.all().get()
    total_bytes = global_stat.bytes if global_stat else -1
    return {
            'total_bytes':total_bytes,
            }

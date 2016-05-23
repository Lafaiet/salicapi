import time
from Log import Log


class Timer(object):
    def __init__(self, action = None, verbose=False):
        self.verbose = verbose
        self.action = action or "default"

    def __enter__(self):
        self.start = time.time()
        if self.verbose:
            Log.debug('Starting action \"%s\"' % (self.action))
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            Log.debug('elapsed time for action \"%s\": %f ms' % (self.action, self.msecs))



if __name__ == "__main__":

    with Timer(action = 'sleeping', verbose = True):
        print 'Waiting...'
        time.sleep(2)

    #print "=> elapsed: %s s" % t.secs
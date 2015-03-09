#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from multiprocessing import Process
from multiprocessing import Pool

from multi_geocoder import *

if __name__=='__main__':
    print "Parent process pid = %s" % (os.getpid())
    pool = Pool(6)
    for p in range(6):
        pool.apply_async(geocoder, args=(p+10,))
    print "Waiting for all subprocesses done..."
    pool.close()
    pool.join()
    print "All subprocesses done."

# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-26 19:25:52
# @Last Modified by:   edward
# @Last Modified time: 2016-07-26 20:45:47
from _bytes import src as AUDIO_SRC
import os
import mp3play
import threading
import time


class Clock(object):
    def __init__(self, name, *args, **kw):
        super(Clock, self).__init__(*args, **kw)
        self.filename = name
        self._started = False
        self._thd = None
        if not os.path.exists(name):
            with open(name, 'wb') as outfile:
                outfile.write(AUDIO_SRC)
                outfile.flush()

    def _task(self):
        mp3 = mp3play.load(self.filename) 
        mp3.play() 
        self._started = True
        # Let it play for up to 30 seconds, then stop it. 
        s = mp3.seconds()
        while not self._thd.stopped() and s > 0:
            time.sleep(0.1)
            s -= 0.1
        mp3.stop()
        self._started = False

    def Play(self, thd):
        if self._started is False:
            self._thd = thd
            t = threading.Thread(target=self._task)
            t.setDaemon(True)
            t.start()
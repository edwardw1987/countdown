# -*- coding: utf-8 -*-
# @Author: edward
# @Date:   2016-07-26 19:25:52
# @Last Modified by:   edward
# @Last Modified time: 2016-07-27 11:00:02
from _bytes import src as AUDIO_SRC
import os
from wx.media import MediaCtrl


class Clock(MediaCtrl):
    # state: 0 stop 1 pause 2 play
    def setThread(self, thd):
        self._thread = thd

    def getThread(self):
        return getattr(self, '_thread', None)

def setup(frame, filename):
    def _initMp3(name):
        if not os.path.exists(name):
            with open(name, 'wb') as outfile:
                outfile.write(AUDIO_SRC)
                outfile.flush()
    _initMp3(filename)
    frame.clock = Clock(frame, fileName=filename)
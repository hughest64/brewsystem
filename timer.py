import time

"""
TODO:

Add subclasses for mash and boil\
- boil:
   - parse beer xml file to pull a list?, dict? of
     hop additons. (time, name, amount).
     possibly pop a new alert window for each additon in main file.
"""

class Timer(object):

    def __init__(self):

        self.mn = 0
        self.sec = 0
        self.status = False

    def Set(self, mn, sec):
        """ Setting the timer. """
        # ints are used for the countdown
        self.mn = mn
        self.sec = sec
        # vaues stored away for Reset() method
        self.resetMn = mn
        self.resetSec = sec

    def Run(self):
        """ The actual count down. """
        if self.sec == 0:
            self.mn -= 1
            self.sec = 59

        else:
            self.sec -= 1

        #time.sleep(1) # for now use wx.Timer() object to control the delay !!!

    def Display(self):
        """
        Returns a dict of int mn, int sec, string 'mn:sec'
        """
        if self.mn < 10:
            strMn = '0' + str(self.mn)
        else:
            strMn = str(self.mn)

        if self.sec < 10:
           strSec = '0' + str(self.sec)
        else:
           strSec = str(self.sec)

        disp = (strMn + ':' + strSec)
        timerVals = {'mn':self.mn, 'sec':self.sec, 'display':disp}
        return timerVals

    def IsRunning(self):
        """ A flag for starting and stopping the timer. """
        if self.status:
            self.status = False
        else:
            self.status = True

    def RunStatus(self):
        """ Returns the current run status of the timer. """
        return self.status

    def Reset(self):
        """ Resets the timer to previous self.Set value. """
        # make sure the timer is stopped
        if self.status:
            self.status = False
        # reset mn/sec values
        self.Set(self.resetMn, self.resetSec)

# just some tests here
if __name__ == '__main__':

    timer = Timer()
    timer.Set(0, 10)
    vals = timer.Display()
    print vals['mn'], vals['sec'], vals['display']
    timer.Start()
    while vals['mn'] >= 0 and timer.Status():
        # display the count on the frame
        print vals['display']
        # decrement the timer
        timer.Run()
        vals = timer.Display()
    #timer.Reset()

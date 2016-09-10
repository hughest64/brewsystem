import wx # wxpython is being used for our gui
from timer import * # the brewing Timer class
"""
TODO: !!!
- add box for timer display
- add hop add parsing to timer(boil) !!!
- layout management and style
"""
### CONSTANTS ###
SIZE = ((640, 480))
TITLE = 'Brewsys'
TIMER = Timer()

class SetTimer(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(SetTimer, self).__init__(*args, **kwargs)

        #buttons
        svbtn = wx.Button(self, label='Save', pos=(20, 120))
        clbtn = wx.Button(self, label='Close', pos=(100, 120))

        #static text labels
        st1 = wx.StaticText(self, label='Min', pos=(50, 20))
        st2 = wx.StaticText(self, label='Sec', pos=(50, 70))

        #spin boxes for setting the timer mn/sec vals
        self.sc1 = wx.SpinCtrl(self, value='0', pos=(80, 15),
                               size=(60, -1), min=0, max=120)
        self.sc2 = wx.SpinCtrl(self, value='0', pos=(80, 65),
                               size=(60, -1), min=0, max=59)

        #button bindings
        svbtn.Bind(wx.EVT_BUTTON, self.OnSave)
        self.Bind(wx.EVT_BUTTON, self.OnSaveClick)
        clbtn.Bind(wx.EVT_BUTTON, self.OnCancel)

        self.SetSize((250, 250))
        self.SetTitle("Set Timer")
        self.Centre()

    def ShowTime(self, e):
        """ Show the window """
        self.sc1.SetValue(0)
        self.sc2.SetValue(0)
        self.Show(True)

    def OnSave(self, e):
        """
        Apply the new timer values, close the window,
        and propigate the event to the class.
        """
        mn = self.sc1.GetValue()
        sec = self.sc2.GetValue()
        TIMER.Set(mn, sec)
        e.Skip()
        self.Hide()

    def OnSaveClick(self, e):
        """ Propigate the event to the World class """
        e.Skip()

    def OnCancel(self, e):
        """ Close the window without making changes """
        self.Hide()

class World(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        # initialize the window and user interface
        self.InitUI()

    def InitUI(self):
        """ Set up the interface """
        panel = SetTimer(self)

        # buttons
        self.stbtn = wx.Button(self, label='Start', pos=(200,125))
        rbtn = wx.Button(self, label='Reset', pos=(275,125))
        cbtn = wx.Button(self, label='Close', pos=(350,125))

        # the menu system
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fitemOne = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        fitemTwo = fileMenu.Append(wx.ID_ANY, 'Set', 'Set the timer')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # an object to draw the timer in the window client area
        self.dc = wx.ClientDC(self)
        font = wx.Font(30, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.dc.SetFont(font)

        # intializing the wx.Timer()
        self.wxtimer = wx.Timer(self)
        settimer = SetTimer(self)

        # event bindings
        self.Bind(wx.EVT_MENU, self.OnClose, fitemOne)
        self.Bind(wx.EVT_MENU, settimer.ShowTime, fitemTwo)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.wxtimer)
        self.stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)
        rbtn.Bind(wx.EVT_BUTTON, self.OnReset)
        self.Bind(wx.EVT_BUTTON, self.OnSaveClick)

        # set display details
        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)

        # draw the initial timer
        self.vals = TIMER.GetDisplay()
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnRefresh(self, e):
        """ Reset the display. """
        self.vals = TIMER.GetDisplay()
        self.dc.Clear()
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnTimer(self, e):
        """ Decrement and redraw the timer """
        if self.vals['mn'] >= 0 and TIMER.GetStatus():
            # decrement the timer
            TIMER.Run()
            # redraw the display
            self.OnRefresh(e)
            # stop once we are at '00:00'
            if self.vals['display'] == '00:00':
                TIMER.Stop()
                self.wxtimer.Stop()
                self.stbtn.SetLabel('Start')

    def OnRunning(self, e):
        """ Start and stop the timer. """
        # start the timer unless we are a '00:00'
        if not TIMER.GetStatus() and self.vals['display'] != '00:00':
            self.stbtn.SetLabel('Pause')
            self.wxtimer.Start(1000)
            TIMER.Start()
        # stop the timer
        else:
            TIMER.Stop()
            self.wxtimer.Stop()
            self.stbtn.SetLabel('Start')

    def OnReset(self, e):
        """ Reset the timer """
        self.stbtn.SetLabel('Start')
        TIMER.Reset()
        self.OnRefresh(e)

    def OnSaveClick(self, e):
        """ Received wx.EVT_BUTTON event from SetTimer class. """
        self.OnRefresh(e)
        e.Skip()

    def OnClose(self, e):
        """ close the app """
        self.Close(True)



# run the app
if __name__ == '__main__':
    wo = wx.App()
    World(None)
    wo.MainLoop()

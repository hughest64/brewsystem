import wx # wxpython is being used for our gui
from timer import * # the brewing Timer class
"""
TODO: !!!
- add box for timer display
- menu option to set timer time (dialog box?)
- add hop add parsing to timer(boil) !!!
"""
### CONSTANTS ###
SIZE = ((640, 480))
TITLE = 'Brewsys'
TIMER = Timer()

class World(wx.Frame):  #Creating our Window

    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        # initialize the window and user interface
        self.InitUI()

    def InitUI(self):
        """ Set up the interface """
        #panel = SetTimer(self)

        # buttons
        self.stbtn = wx.Button(self, label='Start', pos=(200,150))
        rbtn = wx.Button(self, label='Reset', pos=(275,150))
        cbtn = wx.Button(self, label='Close', pos=(350,150))

        # creating the menu system
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

        #intializing the timer
        TIMER.Set(0, 10) # this needs it's own method and binding !!!
        self.wxtimer = wx.Timer(self)
        #settimer = SetTimer(self)

        # event bindings
        self.Bind(wx.EVT_MENU, self.OnClose, fitemOne)
        #self.Bind(wx.EVT_MENU, settimer.ShowTime, fitemTwo)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.wxtimer)
        self.stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)
        rbtn.Bind(wx.EVT_BUTTON, self.OnReset)

        # setting display details
        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)

        # draw the initial timer
        self.vals = TIMER.GetDisplay()
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnRefresh(self, e):
        self.vals = TIMER.GetDisplay()
        self.dc.Clear()
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnTimer(self, e):
        """ method to draw the timer """
        if self.vals['display'] == '00:00':
            TIMER.Stop()
            self.wxtimer.Stop()
            self.stbtn.SetLabel('Start')

        elif self.vals['mn'] >= 0 and TIMER.GetStatus():
            # decrement the timer
            TIMER.Run()
            self.OnRefresh(e)

    def OnRunning(self, e):
        """ Start and stop the timer. """
        #if self.vals['Display'] == '00:00':

        if not TIMER.GetStatus() and self.vals['display'] != '00:00':
            self.stbtn.SetLabel('Pause')
            self.wxtimer.Start(1000)
            TIMER.Start()

        else:
            TIMER.Stop()
            self.wxtimer.Stop()
            self.stbtn.SetLabel('Start')

    def OnSet(self, mn, sec, e):
        #print mn, sec
        TIMER.Set(mn, sec)
        self.OnRefresh(e)
        #self.vals = TIMER.GetDisplay()
        #self.dc.Clear()
        #self.dc.DrawText(self.vals['display'], 260, 50)

    def OnReset(self, e):
        """ reset the timer """
        self.stbtn.SetLabel('Start')
        TIMER.Reset()
        self.OnRefresh(e)

    def OnClose(self, e):
        """ close the app """
        self.Close(True)



# run the app
if __name__ == '__main__':
    wo = wx.App()
    World(None)
    wo.MainLoop()

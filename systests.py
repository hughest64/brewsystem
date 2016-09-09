import wx # wxpython is being used for our gui
from timer import * # the brewing Timer class
"""
TODO: !!!
- add box for timer display
- make start button toggle to change label when running
- menu option to set timer time (dialog box?)
- add hop add parsing to timer(boil) !!!
"""
### CONSTANTS ###
SIZE = ((640, 480))
TITLE = 'Brewsys'

class World(wx.Frame):  #Creating our Window

    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        # initialize the window and user interface
        self.InitUI()

    def InitUI(self):
        """ Set up the interface """
        panel = wx.Panel(self)

        # buttons
        stbtn = wx.Button(self, label='Start', pos=(200,150))
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
        self.timer = Timer()
        self.timer.Set(0, 10) # this needs it's own method and binding !!!
        self.ti = wx.Timer(self)

        # event bindings
        self.Bind(wx.EVT_MENU, self.OnClose, fitemOne, fitemTwo)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.ti)
        stbtn.Bind(wx.EVT_BUTTON, self.OnRunning)
        cbtn.Bind(wx.EVT_BUTTON, self.OnClose)
        rbtn.Bind(wx.EVT_BUTTON, self.OnReset)

        # setting display details
        self.SetSize(SIZE)
        self.SetTitle(TITLE)
        self.Centre()
        self.Show(True)

        # draw the initial timer
        self.vals = self.timer.GetDisplay()
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnTimer(self, e):
        """ method to draw the timer """
        if self.vals['mn'] >= 0 and self.timer.GetStatus():
            # decrement the timer
            self.timer.Run()
            self.vals = self.timer.GetDisplay()
            # clear the previous value and draw the new
            self.dc.Clear()
            self.dc.DrawText(self.vals['display'], 260, 50)

    def OnRunning(self, e):
        """ Start and stop the timer. """
        if not self.timer.GetStatus():
            self.ti.Start(1000)
            self.timer.Start()

        else:
            self.timer.Stop()
            self.ti.Stop()

    def OnReset(self, e):
        """ reset the timer """
        self.timer.Reset()
        self.vals = self.timer.GetDisplay()
        self.dc.Clear()
        self.dc.DrawText(self.vals['display'], 260, 50)

    def OnClose(self, e):
        """ close the app """
        self.Close(True)

# run the app
if __name__ == '__main__':
    wo = wx.App()
    World(None)
    wo.MainLoop()

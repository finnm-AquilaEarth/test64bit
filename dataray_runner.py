import wx
import wx.lib.activex
import csv
import comtypes.client
import zaber_control as zb
import os

output_number = 0
distance = 100
beam_size = 5
number_of_images = distance / beam_size
port = "COM4"  # Adjust for your system

# Class that handles events for ActiveX controls
class EventSink(object):
    def __init__(self, app):
        self.app = app

class MyApp(wx.App):
    def OnStart(self, e=None):
        print("Test Started")
        self.run_automated_clicks(10)


    def OnClick(self, e=None):
        print("!!Write Event!!")
        rb_selection = self.rb.GetStringSelection()
        if rb_selection == "WinCam":
            data = self.gd.ctrl.GetWinCamDataAsVariant()
            data = [[x] for x in data]
        else:
            datax = self.px.ctrl.GetProfileDataAsVariant()
            datay = self.py.ctrl.GetProfileDataAsVariant()
            # Combine datax and datay into a 2D matrix representation
            # Assuming `datax` and `datay` have the same length and represent a square image
            # Adjust the length check based on the actual size of your data
            matrix_size = int(len(datax)**0.5)  # Assumes a square image
            data = [datax[i * matrix_size:(i + 1) * matrix_size] for i in range(matrix_size)]
        
        output_dir = "C:/Users/Finn/Documents/test64bit/dataray_outputs"
        filename = f"C:/Users/Finn/Documents/test64bit/dataray_outputs/dataray_output_{self.output_number}.csv"
        self.output_number += 1

        # Ensure the output directory exists, create if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)


        with open(filename, 'w') as fp:
            w = csv.writer(fp, delimiter=',')
            w.writerows(data)

        zb.move_device_by_distance(10,port)

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(parent=None, id=wx.ID_ANY, size=(900, 900), 
                              title='Python Interface to DataRay')
        self.output_number = 0
        self.button_297_clicked = False  # Flag to track if ButtonID 297 has been clicked

        # Panel
        p = wx.Panel(self.frame, wx.ID_ANY)
        # Get Data
        self.gd = wx.lib.activex.ActiveXCtrl(p, 'DATARAYOCX.GetDataCtrl.1')
        self.frame.Show()

        # EventSink for main data control
        sink = EventSink(self)
        self.sink = comtypes.client.GetEvents(self.gd.ctrl, sink)

        # ActiveX control with ButtonID 297
        b1 = wx.lib.activex.ActiveXCtrl(parent=p, size=(200, 50), pos=(7, 0),
                                             axID='DATARAYOCX.ButtonCtrl.1')
        b1.ctrl.ButtonID = 297

        # EventSink for ButtonID 297
        b1_sink = EventSink(b1)
        comtypes.client.GetEvents(b1.ctrl, b1_sink)  # Attach event sink to ActiveX control

        # Additional Buttons
        b2 = wx.lib.activex.ActiveXCtrl(parent=p, size=(100, 25), pos=(5, 55),
                                        axID='DATARAYOCX.ButtonCtrl.1')
        b2.ctrl.ButtonID = 171
        b3 = wx.lib.activex.ActiveXCtrl(parent=p, size=(100, 25), pos=(110, 55),
                                        axID='DATARAYOCX.ButtonCtrl.1')
        b3.ctrl.ButtonID = 172
        b4 = wx.lib.activex.ActiveXCtrl(parent=p, size=(100, 25), pos=(5, 85),
                                        axID='DATARAYOCX.ButtonCtrl.1')
        b4.ctrl.ButtonID = 177
        b4 = wx.lib.activex.ActiveXCtrl(parent=p, size=(100, 25), pos=(110, 85),
                                        axID='DATARAYOCX.ButtonCtrl.1')
        b4.ctrl.ButtonID = 179

        # Pictures and Profiles
        tpic = wx.lib.activex.ActiveXCtrl(parent=p, size=(250, 250), 
                                          axID='DATARAYOCX.ThreeDviewCtrl.1', pos=(500, 250))
        self.px = wx.lib.activex.ActiveXCtrl(parent=p, size=(300, 200),
                                             axID='DATARAYOCX.ProfilesCtrl.1', pos=(0, 600))
        self.px.ctrl.ProfileID = 22
        self.py = wx.lib.activex.ActiveXCtrl(parent=p, size=(300, 200),
                                             axID='DATARAYOCX.ProfilesCtrl.1', pos=(600, 600))
        self.py.ctrl.ProfileID = 23
        wx.lib.activex.ActiveXCtrl(parent=p, axID='DATARAYOCX.CCDimageCtrl.1',
                                   size=(250, 250), pos=(250, 250))

        # Custom controls
        t = wx.StaticText(p, label="File:", pos=(5, 115))
        self.rb = wx.RadioBox(p, label="Data:", pos=(5, 140), choices=["Profile", "WinCam"])
        self.cb = wx.ComboBox(p, pos=(5, 200), choices=["Profile_X", "Profile_Y", "Both"])
        self.cb.SetSelection(0)

        #Setup write button
        myb = wx.Button(p, label="Write", pos=(5, 225))
        myb.Bind(wx.EVT_BUTTON, self.OnClick)

        #Setup start test button
        start = wx.Button(p, label = "Start Test", pos=(5, 250))
        start.Bind(wx.EVT_BUTTON, self.OnStart)

        self.gd.ctrl.StartDriver()
        self.button_297_clicked = True
        # wx.CallLater(10000, self.run_automated_clicks, 10)

    def run_automated_clicks(self, x):
        if self.button_297_clicked:  # Ensure ButtonID 297 was triggered first
            for _ in range(x):
                wx.CallLater(10, self.OnClick)

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()

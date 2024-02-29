import pcbnew
import wx
import os

class PluginSettings:
    def __init__(self):
        self.corner_radius = pcbnew.FromMM(3)
        self.padding_left = pcbnew.FromMM(0)
        self.padding_right = pcbnew.FromMM(0)
        self.padding_top = pcbnew.FromMM(0)
        self.padding_bottom = pcbnew.FromMM(0)

class BoardOutlinePluginDialog(wx.Dialog):
    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, title='Board outline generator')
        self.Bind(wx.EVT_CLOSE, self.OnCancel, id=self.GetId())

        # Create a panel
        panel = wx.Panel(self)

        # Create boxes
        vbox = wx.BoxSizer(wx.VERTICAL)
        item_grid = wx.FlexGridSizer(0, 2, 3, 5)
        item_grid.AddGrowableCol(1)

        # Create the numerical options
        item_grid.Add(wx.StaticText(panel, label='Corner radius (mm)'), 1, wx.ALIGN_CENTRE_VERTICAL)
        self.corner_radius = wx.SpinCtrlDouble(panel, style=wx.SP_ARROW_KEYS, min=0.1, inc=0.1, value='3.0')
        self.corner_radius.SetDigits(2)
        item_grid.Add(self.corner_radius, 1, wx.EXPAND)

        item_grid.Add(wx.StaticText(panel, label='Left padding (mm)'), 1, wx.ALIGN_CENTRE_VERTICAL)
        self.padding_left = wx.SpinCtrlDouble(panel, style=wx.SP_ARROW_KEYS, min=0.0, inc=0.1, value='0.0')
        self.padding_left.SetDigits(2)
        item_grid.Add(self.padding_left, 1, wx.EXPAND)

        item_grid.Add(wx.StaticText(panel, label='Right padding (mm)'), 1, wx.ALIGN_CENTRE_VERTICAL)
        self.padding_right = wx.SpinCtrlDouble(panel, style=wx.SP_ARROW_KEYS, min=0.0, inc=0.1, value='0.0')
        self.padding_right.SetDigits(2)
        item_grid.Add(self.padding_right, 1, wx.EXPAND)

        item_grid.Add(wx.StaticText(panel, label='Top padding (mm)'), 1, wx.ALIGN_CENTRE_VERTICAL)
        self.padding_top = wx.SpinCtrlDouble(panel, style=wx.SP_ARROW_KEYS, min=0.0, inc=0.1, value='0.0')
        self.padding_top.SetDigits(2)
        item_grid.Add(self.padding_top, 1, wx.EXPAND)

        item_grid.Add(wx.StaticText(panel, label='Bottom padding (mm)'), 1, wx.ALIGN_CENTRE_VERTICAL)
        self.padding_bottom = wx.SpinCtrlDouble(panel, style=wx.SP_ARROW_KEYS, min=0.0, inc=0.1, value='0.0')
        self.padding_bottom.SetDigits(2)
        item_grid.Add(self.padding_bottom, 1, wx.EXPAND)

        # Create two buttons
        button_box = wx.BoxSizer(wx.HORIZONTAL)
        btn_cancel = wx.Button(panel, label='Cancel')
        self.Bind(wx.EVT_BUTTON, self.OnCancel, id=btn_cancel.GetId())
        button_box.Add(btn_cancel, 1, wx.RIGHT, 10)
        btn_create = wx.Button(panel, label='Generate outline')
        self.Bind(wx.EVT_BUTTON, self.OnCreate, id=btn_create.GetId())
        button_box.Add(btn_create, 1)

        # Add the items to the vbox
        vbox.Add(item_grid, 1, wx.EXPAND | wx.ALIGN_CENTRE | wx.ALL, 10)
        vbox.Add(button_box, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)
        # Make the vbox
        panel.SetSizer(vbox)
        vbox.Fit(self)
        self.Centre()

    def OnCancel(self, event):
        self.EndModal(0)

    def OnCreate(self, event):
        self.EndModal(1)

    def GetSettings(self):
        settings = PluginSettings()
        settings.corner_radius = pcbnew.FromMM(self.corner_radius.GetValue())
        settings.padding_left = pcbnew.FromMM(self.padding_left.GetValue())
        settings.padding_right = pcbnew.FromMM(self.padding_right.GetValue())
        settings.padding_top = pcbnew.FromMM(self.padding_top.GetValue())
        settings.padding_bottom = pcbnew.FromMM(self.padding_bottom.GetValue())
        return settings

    def LoadSettings(self, settings):
        self.corner_radius.SetValue(pcbnew.ToMM(settings.corner_radius))
        self.padding_left.SetValue(pcbnew.ToMM(settings.padding_left))
        self.padding_right.SetValue(pcbnew.ToMM(settings.padding_right))
        self.padding_top.SetValue(pcbnew.ToMM(settings.padding_top))
        self.padding_bottom.SetValue(pcbnew.ToMM(settings.padding_bottom))
##!/bin/env python
#import wx
#class MyFrame(wx.Frame):

#    def __init__(self):
#        wx.Frame.__init__(self, None, -1, "My Frame", size=(300, 300))
#        panel = wx.Panel(self, -1)
#        panel.Bind(wx.EVT_MOTION,  self.OnMove)
#        wx.StaticText(panel, -1, "Pos:", pos=(10, 12))
#        self.posCtrl = wx.TextCtrl(panel, -1, "", pos=(40, 10))

#    def OnMove(self, event):
#        pos = event.GetPosition()
#        self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))

#if __name__ == '__main__':
#    app = wx.PySimpleApp()
#    frame = MyFrame()
#    frame.Show(True)
#    app.MainLoop()

#!/usr/bin/env python

"""Hello, wxPython! program."""

import wx
import business

class Frame(wx.Frame):   #2 wx.Frame子类
    """Frame class that displays an image."""

    def __init__(self,parent=None, id=-1,
                 pos=wx.DefaultPosition,
                 title='Hello, wxPython!',
                 size=wx.DefaultSize): #3图像参数
        """Create a Frame instance and display image."""
        wx.Frame.__init__(self, parent, id, title, pos, size)
#4 显示图像
        panel = wx.Panel(self) #创建画板
        button_submit = wx.Button(panel, label=u"提交", pos=(400, 50),size=(100, 30)) 
        button_reset = wx.Button(panel, label=u"重置", pos=(400, 100),size=(100, 30)) 
        button_view = wx.Button(panel, label=u"查看", pos=(400, 150),size=(100, 30)) 
        #temp = image.ConvertToBitmap()
        #bmp_size = temp.GetWidth(), temp.GetHeight()
        self.bmp = wx.StaticBitmap(parent=panel, pos=(40,40))

        self.tips_ctrl = wx.StaticText(panel, -1, "Start", pos=(40, 170))
        self.code_ctrl = wx.TextCtrl(panel, -1, "", pos=(200, 50),size=(150,30),style=wx.TE_PROCESS_ENTER)
        self.code_ctrl.SetFocus()
        
        #绑定按钮的单击事件
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, button_submit)
        self.Bind(wx.EVT_BUTTON, self.OnReset, button_reset)
        self.Bind(wx.EVT_BUTTON, self.OnView, button_view)
        #绑定窗口的关闭事件
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnSubmit,self.code_ctrl)

        self.register = business.SohuMailbox()
        self.refresh()
 
    def refresh(self):
        self.register.get_next()
        image = wx.Image('code.png', wx.BITMAP_TYPE_ANY)
        temp = image.ConvertToBitmap()
        self.bmp.SetBitmap(temp)

    def OnSubmit(self, event):
        code = self.code_ctrl.GetLineText(0)
        ret,info = self.register.submit(code)
        if ret:
            self.tips_ctrl.SetLabel("success!!")
        else:
            self.tips_ctrl.SetLabel(info)
        self.refresh()
 
    def OnReset(self,event):
        pass

    def OnView(self,event):
        pass

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnKeyPress(self,event):
        pass

class App(wx.App):  #5 wx.App子类
    """Application class."""

    def OnInit(self):
        #image = wx.Image('wxPython.jpg', wx.BITMAP_TYPE_ANY)
        self.frame = Frame(size=wx.Size(600,400))
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True



def main():  #7
    app = App()
    app.MainLoop()

if __name__ == '__main__':
     main()
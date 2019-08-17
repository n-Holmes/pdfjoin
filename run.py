from src.joiner import concatenate
import src.app
import wx


if __name__ == "__main__":
    app = wx.App(False)
    frame = src.app.MainFrame()
    app.MainLoop()

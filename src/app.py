"""Visual elements for the app."""

import os
from stat import ST_CTIME, ST_MTIME, ST_SIZE
from time import localtime, strftime

from ObjectListView import ObjectListView, ColumnDefn
import wx

from .helpers import file_size_format


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        self.window.update_display(filenames)
        return True


class FileInfo:
    def __init__(self, path, date_created, date_modified, size):
        self.name = os.path.basename(path)
        self.path = path
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size


class MainPanel(wx.Panel):
    """The main window of the app.  Placed within the frame.
    
    Args:
        parent: A `wx.Frame` instance.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.file_list = []

        file_drop_target = FileDropTarget(self)
        self.list_view = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.list_view.SetDropTarget(file_drop_target)
        self.set_files()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_view, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def update_display(self, file_list):
        for path in file_list:
            stats = os.stat(path)
            creation_time = strftime("%d/%m/%Y %I:%M %p", localtime(stats[ST_CTIME]))
            modified_time = strftime("%d/%m/%Y %I:%M %p", localtime(stats[ST_MTIME]))
            file_size = file_size_format(stats[ST_SIZE])

            self.file_list.append(
                FileInfo(path, creation_time, modified_time, file_size)
            )
            self.list_view.SetObjects(self.file_list)

    def set_files(self):
        self.list_view.SetColumns(
            [
                ColumnDefn("Name", "left", 220, "name"),
                ColumnDefn("Date created", "left", 150, "date_created"),
                ColumnDefn("Date modified", "left", 150, "date_modified"),
                ColumnDefn("Size", "left", 100, "size"),
            ]
        )
        self.list_view.SetObjects(self.file_list)


class MainFrame(wx.Frame):
    """The Frame to hold the app."""

    def __init__(self):
        wx.Frame.__init__(
            self, parent=None, title="Drag 'n' Drop Files", size=(800, 600)
        )
        panel = MainPanel(self)
        self.Show()

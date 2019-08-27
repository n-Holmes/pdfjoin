"""Visual elements for the app."""

import os
from stat import ST_CTIME, ST_MTIME, ST_SIZE
from time import localtime, strftime

from ObjectListView import ObjectListView, ColumnDefn
import wx

from .helpers import file_size_format
from .joiner import concatenate


class FileDropTarget(wx.FileDropTarget):
    """Makes the window responsive to file drops."""

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        self.window.add_files(filenames)
        return True


class FileInfo:
    """Simple data class as a model for ObjectListView."""

    def __init__(self, path, date_created, date_modified, size):
        self.name = os.path.basename(path)
        self.path = path
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size


class FilePanel(wx.Panel):
    """The visual element responsible for receiving and displaying information on files.
    
    Args:
        parent: A `wx.Frame` instance.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.file_list = []

        self.list_view = ObjectListView(
            self, style=wx.LC_REPORT | wx.SUNKEN_BORDER, sortable=False
        )
        self._set_files()

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.list_view, 1, wx.EXPAND)
        self._control_setup(main_sizer)
        self.SetSizer(main_sizer)

    def _set_files(self):
        """Configure the ObjectListView."""
        self.list_view.SetDropTarget(FileDropTarget(self))
        self.list_view.SetEmptyListMsg("Drop files here")
        self.list_view.SetColumns(
            [
                ColumnDefn("Name", "left", 220, "name"),
                ColumnDefn("Date created", "left", 130, "date_created"),
                ColumnDefn("Date modified", "left", 130, "date_modified"),
                ColumnDefn("Size", "left", 70, "size"),
            ]
        )
        self.list_view.SetObjects(self.file_list)

    def _control_setup(self, parent):
        button_funcs = {
            "up": ("Move Up", self._move_up),
            "down": ("Move Down", self._move_down),
            "join": ("Join!", self._join),
        }
        buttons = {}
        for name, (text, func) in button_funcs.items():
            buttons[name] = wx.Button(self, wx.ID_ANY, text)
            buttons[name].Bind(wx.EVT_BUTTON, func)

        list_controls = wx.BoxSizer(wx.HORIZONTAL)
        list_controls.AddMany((buttons["up"], buttons["down"]))

        file_controls = wx.BoxSizer(wx.HORIZONTAL)
        file_controls.Add(wx.StaticText(self, 0, "Output Path: "))
        self.path_entry = wx.TextCtrl(self, 0, "joined_file.pdf", size=(200, -1))
        self.path_entry.SetInsertionPoint(0)
        file_controls.AddMany((self.path_entry, buttons["join"]))

        parent.Add(list_controls, 0, wx.CENTER)
        parent.Add(file_controls, 0, wx.CENTER)

    def add_files(self, file_list):
        for path in file_list:
            _, extension = os.path.splitext(path)
            if extension != ".pdf":
                continue

            stats = os.stat(path)
            creation_time = strftime("%d/%m/%Y %I:%M %p", localtime(stats[ST_CTIME]))
            modified_time = strftime("%d/%m/%Y %I:%M %p", localtime(stats[ST_MTIME]))
            file_size = file_size_format(stats[ST_SIZE])

            self.file_list.append(
                FileInfo(path, creation_time, modified_time, file_size)
            )
            self.list_view.SetObjects(self.file_list)

    def _move_selected_item(self, step):
        """Move the currently selected item up or down the list."""
        current_selection = self.list_view.GetSelectedObject()
        if not current_selection:
            return

        index = self.file_list.index(current_selection)
        new_index = (index + step) % len(self.file_list)

        self.file_list.insert(new_index, self.file_list.pop(index))
        self._set_files()
        self.list_view.Select(new_index)

    def _move_up(self, event):
        """Event handler to move an item up the list one space."""
        self._move_selected_item(-1)

    def _move_down(self, event):
        """Event handler to move an item down the list one space."""
        self._move_selected_item(1)

    def _join(self, event):
        out_path = self.path_entry.GetLineText(0)
        concatenate((file.path for file in self.file_list), out_path)


class MainFrame(wx.Frame):
    """The window of the app."""

    def __init__(self):
        wx.Frame.__init__(self, parent=None, title="pdfjoin", size=(570, 400))
        panel = FilePanel(self)
        self.Show()

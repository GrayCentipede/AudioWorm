import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

"""
A class for the window that will be displaying errors.
To generate HTML documentation for this module use the command:

    pydoc -w src.ui.ErrorWindow

"""

class ErrorWindow(Gtk.Window):
    """
    ErrorWindow only shows the error message and it only has one button and an emoticon.
    """

    def __init__(self, message):
        """
        Creates the window with the given message.

        :param message: The message to display
        """

        Gtk.Window.__init__(self, title="Error")
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(8)
        self.add(self.grid)
        self.message_label = Gtk.Label()
        self.message_label.set_text(message)
        self.emoticon = Gtk.Image.new_from_icon_name('face-sick-symbolic', Gtk.IconSize.DIALOG)
        self.ok_button = Gtk.Button('Ok')
        self.ok_button.connect('clicked', self.close)

        self.grid.attach(self.emoticon, 0, 0, 1, 1)
        self.grid.attach_next_to(self.message_label, self.emoticon, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.ok_button, self.emoticon, Gtk.PositionType.BOTTOM, 2, 1)

        self.show_all()

    def close(self, button):
        """
        Closes the window.

        :param button: The button that was clicked
        """
        
        self.destroy()

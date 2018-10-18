import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class ErrorWindow(Gtk.Window):

    def __init__(self, message):
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
        self.destroy()

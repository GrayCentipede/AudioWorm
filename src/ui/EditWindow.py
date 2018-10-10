import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

class EditWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Busqueda")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.save_button = Gtk.Button('Save Changes')

        self.available_group = Gtk.ListStore(int, str)
        self.available_group.append([0, 'New group'])

        self.combo_box = Gtk.ComboBox.new_with_model_and_entry(self.available_group)
        self.combo_box.set_entry_text_column(1)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale( filename='./assets/default_album_icon.png',
                                                          width=64, height=64,
                                                          preserve_aspect_ratio=True)

        self.album_image = Gtk.Image.new_from_pixbuf(pixbuf)

        self.labels = [Gtk.Label('Artist'),
                       Gtk.Label('Album'),
                       Gtk.Label('Song'),
                       Gtk.Label('Year'),
                       Gtk.Label('Track'),
                       Gtk.Label('Person/Group'),
                       Gtk.Label('Group:')]

        self.entries = [Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry(), Gtk.Entry()]
        self.entries[0].set_text('...')
        self.entries[1].set_text('...')
        self.entries[2].set_text('...')
        self.entries[3].set_text('...')
        self.entries[4].set_text('...')

        self.button_is_person = Gtk.RadioButton.new_with_label_from_widget(None, "Group")
        self.button_is_person.connect("toggled", self.on_button_toggled, "1")

        self.button_is_group = Gtk.RadioButton.new_from_widget(self.button_is_person)
        self.button_is_group.set_label("Person")
        self.button_is_group.connect("toggled", self.on_button_toggled, "2")

        self.button_is_unknown = Gtk.RadioButton.new_with_mnemonic_from_widget(self.button_is_person, "Unknown")
        self.button_is_unknown.connect("toggled", self.on_button_toggled, "3")

        self.grid.attach(self.album_image, 0, 0, 1, 7)
        self.grid.attach_next_to(self.labels[0], self.album_image, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.save_button, self.album_image, Gtk.PositionType.BOTTOM, 5, 1)
        self.grid.attach_next_to(self.entries[0], self.labels[0], Gtk.PositionType.RIGHT, 3, 1)
        self.grid.attach_next_to(self.labels[1], self.labels[0], Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entries[1], self.labels[1], Gtk.PositionType.RIGHT, 3, 1)
        self.grid.attach_next_to(self.labels[2], self.labels[1], Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entries[2], self.labels[2], Gtk.PositionType.RIGHT, 3, 1)
        self.grid.attach_next_to(self.labels[3], self.labels[2], Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entries[3], self.labels[3], Gtk.PositionType.RIGHT, 3, 1)
        self.grid.attach_next_to(self.labels[4], self.labels[3], Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.entries[4], self.labels[4], Gtk.PositionType.RIGHT, 3, 1)
        self.grid.attach_next_to(self.labels[5], self.labels[4], Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.button_is_group, self.labels[5], Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.button_is_person, self.button_is_group, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.button_is_unknown, self.button_is_person, Gtk.PositionType.RIGHT, 1, 1)
        self.grid.attach_next_to(self.labels[6], self.labels[5], Gtk.PositionType.BOTTOM, 1, 1)
        self.grid.attach_next_to(self.combo_box, self.labels[6], Gtk.PositionType.RIGHT, 1, 1)

        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)

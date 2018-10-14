import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

class EditWindow(Gtk.Window):
    def __init__(self, song):
        Gtk.Window.__init__(self, title="Busqueda")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.save_button = Gtk.Button('Save Changes')
        self.save_button.connect('clicked', self.close_window)

        self.available_group = Gtk.ListStore(int, str)
        self.available_group.append([0, 'New group'])

        self.combo_box = Gtk.ComboBox.new_with_model_and_entry(self.available_group)
        self.combo_box.set_entry_text_column(1)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale( filename='./assets/default_album_icon.png',
                                                          width=64, height=64,
                                                          preserve_aspect_ratio=True)

        self.album_image = Gtk.Image.new_from_pixbuf(pixbuf)

        self.labels = [Gtk.Label('Artist'),        #self.labels[0]
                       Gtk.Label('Album'),         #self.labels[1]
                       Gtk.Label('Song'),          #self.labels[2]
                       Gtk.Label('Year'),          #self.labels[3]
                       Gtk.Label('Track'),         #self.labels[4]
                       Gtk.Label('Genre'),         #self.labels[5]
                       Gtk.Label('Person/Group'),  #self.labels[6]
                       Gtk.Label('Group:'),        #self.labels[7]
                       Gtk.Label('Stage name:'),   #self.labels[8]
                       Gtk.Label('Real name:'),    #self.labels[9]
                       Gtk.Label('Birth Date:'),   #self.labels[10]
                       Gtk.Label('Death Date:'),   #self.labels[11]
                       Gtk.Label('Group Name:'),   #self.labels[12]
                       Gtk.Label('Start Date:'),   #self.labels[13]
                       Gtk.Label('End Date:')]     #self.labels[14]

        self.entries = [Gtk.Entry(),  #Artist entry       - self.entries[0]
                        Gtk.Entry(),  #Album entry        - self.entries[1]
                        Gtk.Entry(),  #Song entry         - self.entries[2]
                        Gtk.Entry(),  #Year entry         - self.entries[3]
                        Gtk.Entry(),  #Track entry        - self.entries[4]
                        Gtk.Entry(),  #Genre entry        - self.entries[5]
                        Gtk.Entry(),  #Person/Group entry - self.entries][6]
                        Gtk.Entry(),  #Stage name entry   - self.entries[7]
                        Gtk.Entry(),  #Real name entry    - self.entries[8]
                        Gtk.Entry(),  #Birth date entry   - self.entries[9]
                        Gtk.Entry(),  #Death date entry   - self.entries][10]
                        Gtk.Entry(),  #Group name entry   - self.entries[11]
                        Gtk.Entry(),  #Start date entry   - self.entries[12]
                        Gtk.Entry()]  #End date entry     - self.entries[13]

        self.entries[0].set_text(song[1])
        self.entries[1].set_text(song[2])
        self.entries[2].set_text(song[0])
        self.entries[3].set_text(song[3])
        self.entries[4].set_text(song[4])
        self.entries[5].set_text(song[5])

        self.button_is_unknown = Gtk.RadioButton.new_with_mnemonic_from_widget(None, "Unknown")
        self.button_is_unknown.connect("toggled", self.on_button_toggled, "1")

        self.button_is_person = Gtk.RadioButton.new_with_label_from_widget(self.button_is_unknown, "Person")
        self.button_is_person.connect("toggled", self.on_button_toggled, "2")

        self.button_is_group = Gtk.RadioButton.new_with_label_from_widget(self.button_is_unknown, "Group")
        self.button_is_group.connect("toggled", self.on_button_toggled, "3")


        self.grid.attach(self.album_image, 0, 0, 1, 10)
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
        self.grid.attach_next_to(self.entries[5], self.labels[5], Gtk.PositionType.RIGHT, 3, 1)

        # When the performer is type 'UNKNOWN'
        if (song[-1] == 2):
            self.grid.attach_next_to(self.labels[6], self.labels[5], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.button_is_group, self.labels[6], Gtk.PositionType.RIGHT, 1, 1)
            self.grid.attach_next_to(self.button_is_person, self.button_is_group, Gtk.PositionType.RIGHT, 1, 1)
            self.grid.attach_next_to(self.button_is_unknown, self.button_is_person, Gtk.PositionType.RIGHT, 1, 1)
            self.grid.attach_next_to(self.labels[7], self.labels[6], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.combo_box, self.labels[7], Gtk.PositionType.RIGHT, 1, 1)

        # When the performer is type 'PERSON'
        elif (song[-1] == 0):
            self.grid.attach_next_to(self.labels[8], self.labels[5], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[7], self.labels[8], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[9], self.labels[8], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[8], self.labels[9], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[10], self.labels[9], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[9], self.labels[10], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[11], self.labels[10], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[10], self.labels[11], Gtk.PositionType.RIGHT, 3, 1)

        # When the performer is type 'UNKNOWN'
        else:
            self.grid.attach_next_to(self.labels[12], self.labels[5], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[11], self.labels[12], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[13], self.labels[12], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[12], self.labels[13], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[14], self.labels[13], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[13], self.labels[14], Gtk.PositionType.RIGHT, 3, 1)


        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)

    def close_window(self, button):
        self.destroy()

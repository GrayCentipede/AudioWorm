import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

from ..Manager import Manager

class EditWindow(Gtk.Window):

    manager = None
    active = '2'
    type = None
    parent_window = None
    entry = None

    def __init__(self, song, parent_window, album_image):
        self.entry = song
        self.manager = Manager()
        self.parent_window = parent_window

        Gtk.Window.__init__(self, title="Busqueda")
        self.set_border_width(10)

        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(4)
        self.grid.set_column_spacing(8)
        self.add(self.grid)

        self.save_button = Gtk.Button('Save Changes')
        self.save_button.connect('clicked', self.close_window)

        self.available_group = Gtk.ListStore(int, str)
        available_groups = self.manager.get_all_groups()
        available_groups_id = []
        for group in available_groups:
            id = group[0]
            name = group[1]
            self.available_group.append([id, name])
            available_groups_id.append(id)
        self.available_group.append([-1, 'None'])

        self.combo_box = Gtk.ComboBox.new_with_model_and_entry(self.available_group)
        self.combo_box.set_entry_text_column(1)

        self.album_image = Gtk.Image.new_from_pixbuf(album_image)

        self.labels = [Gtk.Label('Artist'),        #self.labels[0]
                       Gtk.Label('Album'),         #self.labels[1]
                       Gtk.Label('Song'),          #self.labels[2]
                       Gtk.Label('Year'),          #self.labels[3]
                       Gtk.Label('Track'),         #self.labels[4]
                       Gtk.Label('Genre'),         #self.labels[5]
                       Gtk.Label('Person/Group'),  #self.labels[6]
                       Gtk.Label('Group:'),        #self.labels[7]
                       Gtk.Label('Real name:'),    #self.labels[8]
                       Gtk.Label('Birth Date:'),   #self.labels[9]
                       Gtk.Label('Death Date:'),   #self.labels[10]
                       Gtk.Label('Start Date:'),   #self.labels[11]
                       Gtk.Label('End Date:')]     #self.labels[12]

        self.entries = [Gtk.Entry(),  #Artist entry       - self.entries[0]
                        Gtk.Entry(),  #Album entry        - self.entries[1]
                        Gtk.Entry(),  #Song entry         - self.entries[2]
                        Gtk.Entry(),  #Year entry         - self.entries[3]
                        Gtk.Entry(),  #Track entry        - self.entries[4]
                        Gtk.Entry(),  #Genre entry        - self.entries[5]
                        Gtk.Entry(),  #Person/Group entry - self.entries[6]
                        Gtk.Entry(),  #Real name entry    - self.entries[7]
                        Gtk.Entry(),  #Birth date entry   - self.entries[8]
                        Gtk.Entry(),  #Death date entry   - self.entries[9]
                        Gtk.Entry(),  #Start date entry   - self.entries[10]
                        Gtk.Entry()]  #End date entry     - self.entries[11]

        self.entries[0].set_text(song[1])
        self.entries[1].set_text(song[2])
        self.entries[2].set_text(song[0])
        self.entries[3].set_text(song[3])
        self.entries[4].set_text(song[4])
        self.entries[5].set_text(song[5])

        self.button_is_unknown = Gtk.RadioButton.new_with_mnemonic_from_widget(None, "Unknown")
        self.button_is_unknown.connect("toggled", self.on_button_toggled, "2")

        self.button_is_person = Gtk.RadioButton.new_with_label_from_widget(self.button_is_unknown, "Person")
        self.button_is_person.connect("toggled", self.on_button_toggled, "0")

        self.button_is_group = Gtk.RadioButton.new_with_label_from_widget(self.button_is_unknown, "Group")
        self.button_is_group.connect("toggled", self.on_button_toggled, "1")


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
        if (song[8] == 2):
            self.type = 'UNKNOWN'
            self.grid.attach_next_to(self.labels[6], self.labels[5], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.button_is_group, self.labels[6], Gtk.PositionType.RIGHT, 1, 1)
            self.grid.attach_next_to(self.button_is_person, self.button_is_group, Gtk.PositionType.RIGHT, 1, 1)
            self.grid.attach_next_to(self.button_is_unknown, self.button_is_person, Gtk.PositionType.RIGHT, 1, 1)

        # When the performer is type 'PERSON'
        elif (song[8] == 0):
            self.type = 'PERSON'
            person_info = self.manager.get_person(song[1])
            real_name = '' if person_info[0] is None else person_info[0]
            birth_date = '' if person_info[1] is None else person_info[1]
            death_date = '' if person_info[2] is None else person_info[2]

            person_group = self.manager.get_group_person_is_in(song[7])

            if (person_group is None):
                self.combo_box.set_active(len(self.available_group)-1)
            else:
                self.combo_box.set_active(available_groups_id.index(person_group[0]))


            self.entries[7].set_text(real_name)
            self.entries[8].set_text(birth_date)
            self.entries[9].set_text(death_date)

            self.grid.attach_next_to(self.labels[8], self.labels[5], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[7], self.labels[8], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[9], self.labels[8], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[8], self.labels[9], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[10], self.labels[9], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[9], self.labels[10], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[7], self.labels[10], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.combo_box, self.labels[7], Gtk.PositionType.RIGHT, 1, 1)

        # When the performer is type 'GROUP'
        else:
            self.type = 'GROUP'
            group_info = self.manager.get_group(song[1])
            start_date = '' if  group_info[0] is None else group_info[0]
            end_date = '' if group_info[1] is None else group_info[1]

            self.persons_liststore = Gtk.ListStore(str)

            persons = self.manager.get_persons_in_group(song[1])

            for person in persons:
                self.persons_liststore.append(person)

            self.persons_treeview = Gtk.TreeView.new_with_model(self.persons_liststore)
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn('Persons in the group', renderer, text = 0)
            column.set_expand(True)
            self.persons_treeview.append_column(column)

            self.entries[10].set_text(start_date)
            self.entries[11].set_text(end_date)

            self.grid.attach_next_to(self.labels[11], self.labels[5], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[10], self.labels[11], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.labels[12], self.labels[11], Gtk.PositionType.BOTTOM, 1, 1)
            self.grid.attach_next_to(self.entries[11], self.labels[12], Gtk.PositionType.RIGHT, 3, 1)
            self.grid.attach_next_to(self.persons_treeview, self.entries[0], Gtk.PositionType.RIGHT, 10, 11)


        self.show_all()

    def on_button_toggled(self, button, name):
        if button.get_active():
            self.active = name
            state = "on"
        else:
            state = "off"

    def close_window(self, button):
        artist = self.entries[0].get_text()
        album =self.entries[1].get_text()
        title = self.entries[2].get_text()
        year = self.entries[3].get_text()
        track = self.entries[4].get_text()
        genre = self.entries[5].get_text()

        if (self.type == 'UNKNOWN'):
            status = self.active
        elif (self.type == 'PERSON'):
            status = '0'
        elif (self.type == 'GROUP'):
            status = '1'

        self.manager.update_performer(performer_id = self.entry[7], performer_name = artist,
                                      new_status = status)
        self.manager.update_album(album_id = self.entry[9], album_name = album, album_year = year)
        self.manager.update_song(song_id = self.entry[10], title = title, year = year, track = track,
                                 genre = genre)

        if (self.type == 'UNKNOWN'):
            if (self.active == '0'):
                self.manager.insert_person(artist)

            elif (self.active == '1'):
                self.manager.insert_group(artist)

        elif (self.type == 'PERSON'):
            real_name = self.entries[7].get_text()
            birth_date = self.entries[8].get_text()
            death_date = self.entries[9].get_text()

            index = self.combo_box.get_active()
            model = self.combo_box.get_model()
            item = model[index]
            group_id, group_name = item[0], item[1]

            self.manager.update_person(artist, real_name, birth_date, death_date)

            if (group_id != -1):
                try:
                    self.manager.add_person_to_group(self.entry[1], group_id)
                except Exception as e:
                    print(e)

        elif (self.type == 'GROUP'):
            start_date = self.entries[10].get_text()
            end_date = self.entries[11].get_text()

            self.manager.update_group(artist, start_date, end_date)

        self.parent_window.seed_treeview()

        self.destroy()

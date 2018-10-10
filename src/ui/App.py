import gi
import gtk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

songs_list = [(str(i), str(i), str(i), str(i), str(i), str(i)) for i in range(100)]

class SearchWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Busqueda")
        self.set_border_width(10)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Gtk.ListBox()
        self.page1.set_border_width(10)

        self.general_entry = Gtk.Entry()
        self.general_entry.set_placeholder_text('Artist: A1. Song: S1.')

        self.search_button = Gtk.Button('Search')
        self.search_button_adv = Gtk.Button('Search')

        self.labels = [Gtk.Label('General Search'),
                       Gtk.Label('Advanced Search'),
                       Gtk.Label('Performer'),
                       Gtk.Label('Album'),
                       Gtk.Label('Song')]

        self.page1.add(self.labels[0])
        self.page1.add(self.general_entry)
        self.page1.add(self.search_button)

        self.notebook.append_page(self.page1, Gtk.Label('General'))

        self.page2 = Gtk.ListBox()
        self.page2.set_border_width(10)

        self.performer_entry = Gtk.Entry()
        self.album_entry = Gtk.Entry()
        self.song_entry = Gtk.Entry()

        self.page2.add(Gtk.Label('Busqueda Avanzada'))
        self.page2.add(Gtk.Label('Artista/Grupo'))
        self.page2.add(self.performer_entry)
        self.page2.add(Gtk.Label('Album'))
        self.page2.add(self.album_entry)
        self.page2.add(Gtk.Label('Rola'))
        self.page2.add(self.song_entry)
        self.page2.add(self.search_button_adv)

        self.notebook.append_page(self.page2, Gtk.Label('Avanzada'))

        self.show_all()

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


class App(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="AudioWorm")
        self.set_default_size(1200, 720)
        self.set_border_width(10)

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(4)
        self.grid.set_column_spacing(4)
        self.add(self.grid)

        #Creating the ListStore model
        self.songs_liststore = Gtk.ListStore(str, str, str, str, str, str)
        for software_ref in songs_list:
            self.songs_liststore.append(list(software_ref))

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.songs_liststore)
        for i, column_title in enumerate(["Song", "Performer", "Album", "Track", "Year", "Genre"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_expand(True)
            self.treeview.append_column(column)

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for options in ["Edit", "Play", "Next"]:
            button = Gtk.Button(options)
            button.set_sensitive(False)
            self.buttons.append(button)

        self.buttons[0].connect('clicked', self.open_edit_window)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.buttons[0], 0, 0, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

        self.label_1 = Gtk.Label("Song: ... \n"
                                 "Performer: ... \n")
        self.label_2 = Gtk.Label("Album: ... \n"
                                 "Year ... \n")

        self.grid.attach_next_to(self.label_1, self.buttons[-1], Gtk.PositionType.RIGHT, 2, 1)
        self.grid.attach_next_to(self.label_2, self.label_1, Gtk.PositionType.RIGHT, 2, 1)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_text("0:00 - 0:00")
        self.progressbar.set_show_text(True)
        self.progressbar.set_fraction(1/60)

        self.grid.attach_next_to(self.progressbar, self.label_2, Gtk.PositionType.RIGHT, 2, 1)

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale( filename='./assets/default_album_icon.png',
                                                          width=58, height=58,
                                                          preserve_aspect_ratio=True)

        self.album_image = Gtk.Image.new_from_pixbuf(pixbuf)

        self.grid.attach_next_to(self.album_image, self.progressbar, Gtk.PositionType.RIGHT, 2, 1)

        self.search = Gtk.Button('Search')
        self.search.connect('clicked', self.open_search_window)
        self.grid.attach_next_to(self.search, self.album_image, Gtk.PositionType.RIGHT, 1, 1)

        self.load = Gtk.Button('Load Music')
        self.grid.attach_next_to(self.load, self.search, Gtk.PositionType.RIGHT, 1, 1)

        self.grid.attach_next_to(self.scrollable_treelist, self.buttons[0], Gtk.PositionType.BOTTOM, 13, 12)
        self.scrollable_treelist.add(self.treeview)

        select = self.treeview.get_selection()
        select.connect("changed", self.show_data)


    def open_search_window(self, win):
        subw = SearchWindow()

    def open_edit_window(self, win):
        sube = EditWindow()

    def show_data(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            for button in self.buttons:
                button.set_sensitive(True)
            print("You selected", model[treeiter][0])


win = App()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

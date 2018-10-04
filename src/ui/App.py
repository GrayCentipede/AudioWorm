import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

songs_list = [(str(i), str(i), str(i), str(i), str(i), str(i)) for i in range(100)]

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
        for options in ["Previous", "Play", "Next"]:
            button = Gtk.Button(options)
            self.buttons.append(button)

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
        self.grid.attach_next_to(self.search, self.album_image, Gtk.PositionType.RIGHT, 1, 1)

        self.grid.attach_next_to(self.scrollable_treelist, self.buttons[0], Gtk.PositionType.BOTTOM, 12, 12)
        self.scrollable_treelist.add(self.treeview)


win = App()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

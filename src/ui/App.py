import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

from time import sleep
from threading import Thread

from ..MinerController import MinerController
from ..Player import Player

from .EditWindow import EditWindow
from .SearchWindow import SearchWindow

class App(Gtk.Window):

    miner_controller = None
    selected_song = None
    player = None
    playing = False
    changed = False
    total_time = None
    current_time = None

    player_thread = None

    def __init__(self):
        self.miner_controller = MinerController(self)
        self.selected_song = None
        self.player = Player()

        Gtk.Window.__init__(self, title="AudioWorm")
        self.set_default_size(1200, 720)
        self.set_border_width(10)

        #Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        # self.grid.set_row_homogeneous(True)
        self.grid.set_row_spacing(4)
        self.grid.set_column_spacing(4)
        self.add(self.grid)

        self.spinner = Gtk.Spinner()

        #Creating the ListStore model
        self.songs_liststore = Gtk.ListStore(str, str, str, str, str, str, str, int, int, int, int)

        #creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.songs_liststore)
        for i, column_title in enumerate(["Song", "Performer", "Album", "Year", "Track", "Genre"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_expand(True)
            self.treeview.append_column(column)

        #creating buttons to filter by programming language, and setting up their events
        self.buttons = list()
        for options in ["Edit", "Play", "Stop"]:
            button = Gtk.Button()
            button.set_sensitive(False)
            self.buttons.append(button)

        self.buttons[0].connect('clicked', self.open_edit_window)
        edit_image = Gtk.Image.new_from_icon_name('document-properties-symbolic', Gtk.IconSize.BUTTON)
        self.buttons[0].set_image(edit_image)
        self.buttons[1].connect('clicked', self.play_song)
        play_image = Gtk.Image.new_from_icon_name('media-playback-start-symbolic', Gtk.IconSize.BUTTON)
        self.buttons[1].set_image(play_image)
        self.buttons[2].connect('clicked', self.stop_song)
        stop_img = Gtk.Image.new_from_icon_name('media-playback-stop-symbolic', Gtk.IconSize.BUTTON)
        self.buttons[2].set_image(stop_img)

        width = 0.8 * self.buttons[0].get_allocation().width
        height = 0.8 * self.buttons[0].get_allocation().height

        self.buttons[0].set_size_request(width, height)

        #setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.buttons[0], 0, 0, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)

        self.label_1 = Gtk.Label("Song: ... \n"
                                 "Performer: ... \n")
        self.label_1.set_line_wrap(True)
        self.label_1.set_xalign(0)
        self.label_1.set_max_width_chars(50)
        self.label_2 = Gtk.Label("Album: ... \n"
                                 "Year ... \n")
        self.label_2.set_line_wrap(True)
        self.label_2.set_xalign(0)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_text("0:00 - 0:00")
        self.progressbar.set_show_text(True)

        pixbuf2 = GdkPixbuf.Pixbuf.new_from_file_at_scale( filename='./assets/default_album_icon.png',
                                                          width=200, height=200,
                                                          preserve_aspect_ratio=True)

        self.album_image2 = Gtk.Image.new_from_pixbuf(pixbuf2)

        self.search = Gtk.Button()
        self.search.connect('clicked', self.open_search_window)
        edit_img = Gtk.Image.new_from_icon_name('edit-find-symbolic', Gtk.IconSize.BUTTON)
        self.search.set_image(edit_img)
        self.grid.attach_next_to(self.search, self.buttons[-1], Gtk.PositionType.RIGHT, 1, 1)

        self.load = Gtk.Button()
        self.load.connect('clicked', self.load_database)
        load_img = Gtk.Image.new_from_icon_name('folder-download-symbolic', Gtk.IconSize.BUTTON)
        self.load.set_image(load_img)
        self.grid.attach_next_to(self.load, self.search, Gtk.PositionType.RIGHT, 1, 1)

        self.grid.attach_next_to(self.scrollable_treelist, self.buttons[0], Gtk.PositionType.BOTTOM, 10, 2)
        self.scrollable_treelist.add(self.treeview)

        self.grid.attach_next_to(self.album_image2, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 2, 2)

        self.grid.attach_next_to(self.label_1, self.album_image2, Gtk.PositionType.RIGHT, 5, 1)
        self.grid.attach_next_to(self.label_2, self.label_1, Gtk.PositionType.BOTTOM, 5, 1)
        self.grid.attach_next_to(self.progressbar, self.label_1, Gtk.PositionType.RIGHT, 2, 1)

        select = self.treeview.get_selection()
        select.connect("changed", self.show_data)

        self.player_thread = Thread( target = self.update_progress_bar, daemon=True)
        self.player_thread.start()

        self.progressbar.pulse()

    def load_database(self, widget):
        self.spinner.start()
        self.miner_controller.load_miner()
        self.miner_controller.add_rows()
        self.spinner.stop()
        self.load.set_sensitive(False)

    def seed_treeview(self):
        self.spinner.start()
        self.miner_controller.add_rows()
        self.spinner.stop()

    def open_search_window(self, win):
        subw = SearchWindow(parent_window = self)

    def open_edit_window(self, win):
        sube = EditWindow(song = self.selected_song, parent_window = self)

    def play_song(self, widget):
        if (self.selected_song is not None):
            if (not self.playing or self.changed):
                if (self.changed):
                    year = '' if self.selected_song[3] is None else self.selected_song[3]
                    self.player.stop()
                    self.player.load(self.selected_song[6])
                    self.label_1.set_text("Song: "+ self.selected_song[0] +" \n"
                                          "Performer: "+ self.selected_song[1] +" \n")
                    self.label_2.set_text("Album: "+ self.selected_song[2] +" \n"
                                          "Year: "+ year +" \n")

                self.player.play()
                sleep(0.05)
                self.total_time = self.player.get_length()

                pause_img = Gtk.Image.new_from_icon_name('media-playback-pause-symbolic', Gtk.IconSize.BUTTON)
                self.buttons[1].set_image(pause_img)
                self.playing = True

                self.changed = False

            else:
                self.playing = False
                play_img = Gtk.Image.new_from_icon_name('media-playback-start-symbolic', Gtk.IconSize.BUTTON)
                self.buttons[1].set_image(play_img)
                self.player.pause()

    def stop_song(self, widget):
        self.player.stop()
        self.playing = False
        self.changed = True
        play_img = Gtk.Image.new_from_icon_name('media-playback-start-symbolic', Gtk.IconSize.BUTTON)
        self.buttons[1].set_image(play_img)
        self.label_1.set_text("Song: ... \n"
                              "Performer: ... \n")
        self.label_2.set_text("Album: ... \n"
                              "Year: ... \n")
        self.progressbar.set_text('{} - {}'.format('00:00', '00:00'))


    def show_data(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            for button in self.buttons:
                button.set_sensitive(True)
            self.selected_song = model[treeiter]
            play_img = Gtk.Image.new_from_icon_name('media-playback-start-symbolic', Gtk.IconSize.BUTTON)
            self.buttons[1].set_image(play_img)
            self.changed = True

    def update_progress_bar(self):
        current = 0
        self.current_time = ''
        while (True):
            if (self.playing):
                # self.progressbar.set_fraction(current)
                miliseconds = self.player.player.get_time() / 1000
                mm, ss = divmod(miliseconds, 60)
                self.current_time = "%02d:%02d" % (mm,ss)
                self.progressbar.set_text('{} - {}'.format(self.current_time, self.total_time))
                # current += 1 / self.player.player.get_length()


win = App()
win.set_icon_from_file("./assets/Audioworm_Logo.png")
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

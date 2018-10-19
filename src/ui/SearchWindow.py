import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf

from ..QueryCompiler import QueryCompiler
from ..Manager import Manager

from .ErrorWindow import ErrorWindow

class SearchWindow(Gtk.Window):

    compiler = None
    parent_window = None
    manager = None

    def __init__(self, parent_window):

        self.parent_window = parent_window

        self.compiler = QueryCompiler()
        self.manager = Manager()

        Gtk.Window.__init__(self, title="Busqueda")
        self.set_border_width(10)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        self.page1 = Gtk.ListBox()
        self.page1.set_border_width(10)

        self.general_entry = Gtk.Entry()
        self.general_entry.set_placeholder_text('Artist: A1. Song: S1.')

        self.search_button = Gtk.Button('Search')
        self.search_button.connect('clicked', self.general_search)
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

        self.show_all()

    def general_search(self, button):
        try:
            entry = self.general_entry.get_text()
            if (entry != ''):
                self.compiler.compile(entry)
                query = self.compiler.get_query()
                rows = self.manager.send_query(query)
                self.parent_window.miner_controller.filter(rows)
            else:
                self.parent_window.miner_controller.add_rows()

            self.destroy()
        except Exception as e:
            self.error_win = ErrorWindow(str(e))

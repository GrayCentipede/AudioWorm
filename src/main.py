#from .ui.App import App
#from gi.repository import Gtk

# Getting the absolute path to home directory.
from pathlib import Path
import os

# Setting up the database
from .Miner import Miner

home  = str(Path.home())
miner = Miner(os.path.abspath(home + '/Music'))
miner.mine()

#App()
#Gtk.main()

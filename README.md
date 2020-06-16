<img src="assets/Logo.png" width="400" heigth="200">

# A very simple media player and media library.

## Requirements
* Python >= 3.5.2
* python-vlc >= 3.0.4106
* mutagen >= 1.41.1
* Pillow >= 7.1.2
* Python Gtk+3 >= 3.4
* setuptools
* pydoc
* sqlite3

### Python GTK+3
It is supposed that ```python 3.5+``` has all the ```GTK+3``` libraries installed by default. However if
this is not the case, it can be downloaded following the instructions given in the
official [Python GTK+3 website](https://python-gtk-3-tutorial.readthedocs.io/en/latest/install.html)

### Pydoc & SQLITE3
The following ```pydoc``` and ```sqlite3``` are installed by default since ```python3.2+```.

# Installing via ```PIP3```

If neccesary all the following libraries can be downloaded via ```PIP3```.

### Python VLC
The music player is supported thanks to ```python-vlc```, a library that allows us to reproduce media files
(```MP3, MP4, ...```).

```
pip3 install python-vlc
```
### Mutagen
All the ```MP3 ID3``` tags loaded thanks to ```Mutagen```
```
pip3 install mutagen
```

### Pillow
For image support.
```
pip3 install Pillow
```

# Installing via ```setuptools```
All the before mentioned libraries can be installed by executing the following command:
```
./setup.py install
```
This will add several ```.pth``` files, each of then can be now installed with ```easy-install```

# Build and Run
To build and execute ```AudioWorm``` use the following:
```
python3 -m src.main
```

# Unit Testing
The unit tests can be executed by the following command:
```
./setup.py test
```

# Documentation
All the modules have the possibilty to generate an ```HTML``` that contains the documentation.
Just do the following:
```
pydoc -w FILE.MODULE
```
Where ```MODULE``` is a python module and ```FILE``` the file that contains the module

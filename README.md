# nwb_explorer
GUI tool for NWB files visual exploration and copy of specific fields.

# Installation and usage
Clone the repository or directly download the files. 
```
$ git clone https://github.com/luiztauffer/nwb_explorer.git
```
Change to the directory of the files and call the main script from the command line. If you provide an empty string as argument, a file dialog will open.
```
$ cd path/to/nwb_explorer
$ python nwb_explorer.py '/path/to/file.nwb'
```

The GUI will discriminate the `file.nwb` fields in a tree. Choosing a specific field will print it's content. 

![screenshot1](media/screenshot_1.png)


You have access to an IPython console to investigate the data even further:

![screenshot2](media/screenshot_2.png)

# crossword-construct
An open-source crossword construction program for cruciverbalists :) Totally free to use! I wrote this piggybacking off another project which I started from scratch.
I don't know too much about licensing, but by using this software you agree to not hold me responsible for any problems it causes. But feel free to use it as it is intended
(a program for constructing crosswords) otherwise!

To run the constructor, just do `python main.py <board_size>`. I use python 3.8, but probably anything >=3.5 will work.

You can also resize once you've created the board, so don't worry too much about the initial board size.

Right now I only support entering letters into the board, and entering clues into the right side panel. But, you can save your boards via the "save to file" button, and then 
load them later! The board ALWAYS saves to a file called 'temp.pkl' (so beware about overwriting stuff!). If you then want to load the file, run:
`python main.py <board_size> --load temp.pkl`. (the board size parameter won't do anything here, oops, it'll just load your board). You can load from any fiel, but right now 
the program will always save to temp.pkl (oops) Feel free to hit me with a PR to save to the file you load from if you want this changed... or even just request push access if
you're interested.

I have plans to support more file formats! Which I will put into practice once I actually finish constructing my first board. Happy Cruciverbalizing! :)

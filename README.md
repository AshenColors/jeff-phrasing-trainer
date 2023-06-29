trainer.py outputs a file with translations and stroke hints in the correct format to be used by [Typey Type's custom lesson tool](https://didoesdigital.com/typey-type/lessons/custom/setup). Right now it only outputs simple phrasing, optionally including past tense and/or suffix strokes, with a limit on the number of keys in the ender defined by `base_ending_max_keys`. This is currently super rough, but I hope to polish it up and provide support for the full form phrases as well.

TODO:
- set options via argparse (DONE)
- output to stdout (DONE)
- avoid duplicate entries in any given output (DONE)
- add full form support
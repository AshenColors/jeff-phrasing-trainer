trainer.py outputs a file with translations and stroke hints in the correct format to be used by [Typey Type's custom lesson tool](https://didoesdigital.com/typey-type/lessons/custom/setup). Argument help generated by the program is shown below.

```usage: Generate Typey Type compatile custom lessons to practice phrases made with the jeff-phrasing dictionary for Plover.
       [-h] [-n N] [--min {1,2,3,4,5}] [--max {1,2,3,4,5,6}] [--simple-only | --full-only] [--no-simple-have]
       [--no-past] [--no-suffix-word] [--no-full-structure] [--no-full-middle]

options:
  -h, --help           show this help message and exit
  -n N, --lines N      Number of lesson entries to generate, from 1 to 100, default 20.
  --min {1,2,3,4,5}    Minimum number of keys in the base ender for each phrase.
  --max {1,2,3,4,5,6}  Maximum number of keys in the base ender for each phrase.
  --simple-only        Only generate simple form phrases.
  --full-only          Only generate full form phrases.
  --no-simple-have     Don't allow the F key in simple form. Doesn't affect the ender 'T'.
  --no-past            Don't allow past tense in phrases.
  --no-suffix-word     Don't allow suffix words in phrases.
  --no-full-structure  Don't allow E, U, or F in full form phrases.
  --no-full-middle     Don't allow A, O, or * in full form phrases.
  ```

TODO:
- set options via argparse (DONE)
- output to stdout (DONE)
- avoid duplicate entries in any given output (DONE)
- add full form support (DONE)
- add arguments to choose which forms to include (DONE)
- add arguments to change full form settings as well (DONE)
- add more robust test suite
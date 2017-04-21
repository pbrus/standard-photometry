# Standard-photometry [![GitHub release](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/ver20170316.svg "download")](https://github.com/pbrus/standard-photometry/blob/master/make_std_phot.py) ![Written in Python](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/python.svg "language")

This program allows to make a photometric standardization. It was written in pure Python.

![make_std_phot](http://www.astro.uni.wroc.pl/ludzie/brus/img/github/make-std-phot.gif)

## Installation

Download `make_std_phot.py` wherever you want, then make the script executable. I recommend to download it to any catalog pointed by the `$PATH` variable. Moreover you should have installed *Python 2.7* with the following modules:

 * *scipy*
 * *pylab*
 * *matplotlib*
 * *argparse*

## Usage

To use the program properly you need to prepare a file with data. At the beginning call the script from the terminal window with the `-h` option:
```bash
$ make_std_phot.py -h
```
This will give you a description of all options. If you need to see the program in action immediately, please download `data.lst` file from the repository to your working directory. A basic call doesn't display an interactive window - all computations run in background. The minimum required arguments are names of the input and output files.
```bash
$ make_std_phot.py data.lst results.lst
```
More advanced call involves the rest of options and their combinations. One of them can be:
```bash
$ make_std_phot.py data.lst results.lst -s 2.5 -i 5 -v -e
```
Assume that the output file has name `results.lst`. Each run of the program generates in a working directory the following files:

  * `results.lst`
  * `results.log`
  * `results-equation-NR.png`

where the amount of the images depends on the number of used equations.

I encourage to visit my website to see more detailed description of this program. The current link can be found on my [GitHub profile](https://github.com/pbrus).

## License

**Standard-photometry** is licensed under the [MIT license](http://opensource.org/licenses/MIT).

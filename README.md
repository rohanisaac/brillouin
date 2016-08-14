# brillouin
Brillouin analysis file

- Runs on a folder of DAT files
- Outputs a fit graph per data file
- Outputs 1 csv data file for each folder with filename and 4 shifts, average shift with relevant uncertainties

Requires
--------
1. numpy
2. scipy
3. matplotlib
4. pandas  # can remove soon
5. lmfit  # main fitting routines

Todo
----

1. Make a test case and run on Travis-CI
2. Option for alternative peak shape
3. Make a GUI
4. Pickle fit objects

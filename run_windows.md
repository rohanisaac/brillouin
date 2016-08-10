# Brillouin peak fitting on Windows

## Running peak fitting

1. Double click on  `C:\Brillouin\brillouin-full-automate-gui.py`
2. A command prompt will open, you can safely ignore (but don't close it).
3. Wait till a folder selection dialog appears (this may take a moment, especially if this is the first time running, or you have just edited the file)
4. Select a folder containing the ".DAT" files from the instrument and click OK to run the batch fit on the folder
5. Depending on the number of files, the process may take a while. Once the routine is complete, you the command prompt will disappear.
6. The folder should now be populated with a folder for each spectra, as well as a `output.csv` file in the main folder containing a summary of the results.

## Changing parameters
1. Right click on the file `C:\Brillouin\brillouin-full-automate-gui.py` and click `Edit` or `Edit with IDLE`
2. Enter a new spacing (in cm) or change crossed to `True` or `False` (case sensitive) under the following section in the file
```python
# Set spacing
spacing = 0.54  # cm
crossed = True  # if peaks are crossed
```
3. Save and close the file
4. Run the program as above

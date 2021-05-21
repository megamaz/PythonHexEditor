# Python Hex Editor
A hex editor but in python. When you run the file, you will have to use launch arguments to specify which file you want to look at.\
If it's formatting weird, let me know. Try to find the byte that's messing it up if possible, and open an issue so I can look into it.
# Extra Information
- Requires python 3.8 or above to run.
- Requires modules listed in `requirements.txt` (`pip install -r ./requirements.txt`)
- All controls are listen inside the application.
- There are a couple known bugs;
    1. The `find` command does not put the cursor on found content until the found content is loaded
    1. Having to press enter twice after doing any action
    1. Actions working on window minimized
    1. **If you run into any other issues please let me know.**
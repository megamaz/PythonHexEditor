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
    1. End of files aren't indexed correctly and certain bytes are absent
    1. Highlight breaks down when the first byte isn't highlighted
    1. **If you run into any other issues please let me know.**
# Running
Latest update made running the code much simpler. The batch will now automatically setup a python venv for you, and install the requirements in the `requirements.txt`. Simply drag and drop the file you wish to inspect onto the `run.bat` and it will setup for you. After that, you can use the hex editor as you please.

If you run into issues, I am going to assume you closed the batch file before it finished running, meaning the dependencies didn't install. Delete the venv folder, and rerun the batch. If you do not trust the dependencies, or the method used to install them, you can look through the batch file and see that nohing malicious is being done. 

However, if your issue resides with scripts not being enabled, you can learn about script running and execution policies [HERE](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.4). The direct solution would be to run this in Admin PowerShell: `Set-ExecutionPolicy RemoteSigned`.

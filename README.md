# Melissa Data Name Object Linux Python3 Sample

## Purpose

This is a sample of the Melissa Data Name Object using Python3

The console will ask the user for:

- Name (First Name + Last Name)

And return 

- Prefix
- First Name
- Middle Name
- Last Name
- Suffix
- Gender
- Salutation
- Result Codes

## Tested Environments

- Linux 64-bit Python 3.8.7
- Ubuntu 20.04.05 LTS
- Melissa data files for 2023-01

## Required File(s) and Programs

#### libmdName.so

This is the c++ code of the Melissa Data Object.

#### Data File(s)
- mdName.cfg
- mdName.dat

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

This project is compatible with Python3


#### Install the Python3
Before starting, make sure that Python3 has been correctly installed on your machine and your environment paths are configured. 

You can download Python here: 
https://www.python.org/downloads/

To set up your Path to correctly use the python3 command, execute the following steps:
1) Run Powershell as an administrator 
2) Execute the command: 
`New-Item -ItemType SymbolicLink -Path "Link" -Target "Target"`

    where "Target" is the path to py.exe (by default this should be "C:\Windows\py.exe")\
    and "Link" is the path to py.exe, but "py.exe" is replaced with "python3.exe"\
    For Example:\
    `New-Item -ItemType SymbolicLink -Path "C:\Windows\python3.exe" -Target "C:\Windows\py.exe"`

If you are unsure, you can check by opening a command prompt window and typing the following:
`python3 --version`

![alt text](/screenshots/python_version.PNG)

If you see the version number then you have installed Python3 and set up your environment paths correctly!

----------------------------------------

#### Download this project
```
$ git clone https://github.com/MelissaData/NameObject-Python3-Linux.git
$ cd NameObject-Python3-Linux
```

#### Set up Melissa Updater 


Melissa Updater is a CLI application allowing the user to update their Melissa applications/data. 

- In the root directory of the project, create a folder called `MelissaUpdater` by using the command: 

  `mkdir MelissaUpdater`

- Enter the newly created folder using the command:

  `cd MelissaUpdater`

- Proceed to install the Melissa Updater using the curl command: 

  `curl -L -O https://releases.melissadata.net/Download/Library/LINUX/NET/ANY/latest/MelissaUpdater`

- After the Melissa Updater is installed, you will need to change the Melissa Updater to an executable using the command:

  `chmod +x MelissaUpdater`

- Now that the Melissa Updater is set up, you can now proceed to move back into the project folder by using the command:
  
   `cd ..`

----------------------------------------

#### Different ways to get data file(s)
1.  Using Melissa Updater
	- It will handle all of the data download/path and dll(s) for you. 
2.  If you already have the latest DQS Release (ZIP), you can find the data file(s) and dll(s) in there
	- Use the location of where you copied/installed the data and update the "$DataPath" variable in the powershell script.
	- Copy all the dll(s) mentioned above into the `MelissaDataNameObjectLinuxPython3Sample` project folder.
	
----------------------------------------
### Change Bash Script Permissions
To be able to run the bash script, you must first make it an executable using the command:

`chmod +x MelissaDataNameObjectLinuxPython3Sample.sh`

Then you need to add permissions to the build directory with the command:

`chmod +rwx MelissaDataNameObjectLinuxPython3Sample`

As an indicator, the filename will change colors once it becomes an executable.

You may also need to alter permissions for the python files. To do this navigate into the MelissaDataNameObjectLinuxPython3Sample directory and run these commands: \
 `chmod +rx MelissaDataNameObjectLinuxPython3Sample/MelissaDataNameObjectLinuxPython3Sample.py` \
  `chmod +rx MelissaDataNameObjectLinuxPython3Sample/mdName_pythoncode.py`

## Run Bash Script

Parameters:
- -n or --name: a test name
 	
  This is convenient when you want to get results for a specific name in one run instead of testing multiple names in interactive mode.  

- -l or --license (optional): a license string to test the name object

- -q or --quiet (optional): add to the command if you do not want to get any console output from the Melissa Updater
- Interactive 

	The script will prompt the user for an name, then use the provided name to test Name object. For example:
	```
	$ ./MelissaDataNameObjectLinuxPython3Sample.sh
	```
    For quiet mode:
    ```
    $ ./MelissaDataNameObjectLinuxPython3Sample.sh --quiet
    ```
- Command Line 

	You can pass a name in ```--name``` parameter and a license string in ```--license``` parameter to test Name object. For example:
	```
    $ ./MelissaDataNameObjectLinuxPython3Sample.sh --name "Ray Melissa" 
    $ ./MelissaDataNameObjectLinuxPython3Sample.sh --name "Ray Melissa" --license "<your_license_string>"
    ```
	For quiet mode:
    ```
    $ ./MelissaDataNameObjectLinuxPython3Sample.sh --name "Ray Melissa" --quiet
    $ ./MelissaDataNameObjectLinuxPython3Sample.sh --name "Ray Melissa" --license "<your_license_string>" --quiet
    ```
This is the expected output from a successful setup for interactive mode:

![alt text](/screenshots/output.png)

    
## Troubleshooting

Troubleshooting for errors found while running your sample program.

### Errors:

| Error      | Description |
| ----------- | ----------- |
| ErrorRequiredFileNotFound      | Program is missing a required file. Please check your Data folder and refer to the list of required files above. If you are unable to obtain all required files through the Melissa Updater, please contact technical support below. |
| ErrorDatabaseExpired   | .db file(s) are expired. Please make sure you are downloading and using the latest release version. (If using the Melissa Updater, check powershell script for 'RELEASE_VERSION = {version}'  and change the release version if you are using an out of date release).     |
| ErrorFoundOldFile   | File(s) are out of date. Please make sure you are downloading and using the latest release version. (If using the Melissa Updater, check powershell script for 'RELEASE_VERSION = {version}'  and change the release version if you are using an out of date release).    |
| ErrorLicenseExpired   | Expired license string. Please contact technical support below. |


## Contact Us

For free technical support, please call us at 800-MELISSA ext. 4
(800-635-4772 ext. 4) or email us at tech@MelissaData.com.

To purchase this product, contact Melissa Data sales department at
800-MELISSA ext. 3 (800-635-4772 ext. 3).

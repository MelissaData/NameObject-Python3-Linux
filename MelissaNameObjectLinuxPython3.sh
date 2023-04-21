#!/bin/bash

# Name:    MelissaNameObjectLinuxPython3
# Purpose: Use the Melissa Updater to make the MelissaNameObjectLinuxPython3 code usable

######################### Constants ##########################

RED='\033[0;31m' #RED
NC='\033[0m' # No Color

######################### Parameters ##########################

name=""
license=""
quiet="false"

while [ $# -gt 0 ] ; do
  case $1 in
    -n | --name) 
        name="$2" 

        if [ "$name" == "-l" ] || [ "$name" == "--license" ] || [ "$name" == "-q" ] || [ "$name" == "--quiet" ] || [ -z "$name" ];
        then
            printf "${RED}Error: Missing an argument for parameter \'name\'.${NC}\n"  
            exit 1
        fi 
        ;;
    -l | --license) 
        license="$2"

        if [ "$license" == "-q" ] || [ "$license" == "--quiet" ] || [ "$license" == "-n" ] || [ "$license" == "--name" ] || [ -z "$license" ];
        then
            printf "${RED}Error: Missing an argument for parameter \'license\'.${NC}\n"  
            exit 1
        fi   
        ;;
    -q | --quiet) 
        quiet="true" 
        ;;
  esac
  shift
done

# ######################### Config ###########################
RELEASE_VERSION='2023.04'
ProductName="DQ_NAME_DATA"

# Uses the location of the .sh file 
# Modify this if you want to use 
CurrentPath=$(pwd)
ProjectPath="$CurrentPath/MelissaNameObjectLinuxPython3"
BuildPath="$ProjectPath"
DataPath="$ProjectPath/Data"

if [ ! -d $DataPath ];
then
    mkdir $DataPath
fi

if [ ! -d $BuildPath ];
then
    mkdir $BuildPath
fi

# Config variables for download file(s)
Config_FileName="libmdName.so"
Config_ReleaseVersion=$RELEASE_VERSION
Config_OS="LINUX"
Config_Compiler="GCC48"
Config_Architecture="64BIT"
Config_Type="BINARY"

# ######################## Functions #########################
DownloadDataFiles()
{
    printf "========================== MELISSA UPDATER =========================\n"
    printf "MELISSA UPDATER IS DOWNLOADING DATA FILE(S)...\n"

    ./MelissaUpdater/MelissaUpdater manifest -p $ProductName -r $RELEASE_VERSION -l $1 -t $DataPath 

    if [ $? -ne 0 ];
    then
        printf "\nCannot run Melissa Updater. Please check your license string!\n"
        exit 1
    fi     
    
    printf "Melissa Updater finished downloading data file(s)!\n"
}

DownloadSO() 
{
    printf "\nMELISSA UPDATER IS DOWNLOADING SO(s)...\n"
    
    # Check for quiet mode
    if [ $quiet == "true" ];
    then
        ./MelissaUpdater/MelissaUpdater file --filename $Config_FileName --release_version $Config_ReleaseVersion --license $1 --os $Config_OS --compiler $Config_Compiler --architecture $Config_Architecture --type $Config_Type --target_directory $BuildPath  &> /dev/null
        if [ $? -ne 0 ];
        then
            printf "\nCannot run Melissa Updater. Please check your license string!\n"
            exit 1
        fi
    else
        ./MelissaUpdater/MelissaUpdater file --filename $Config_FileName --release_version $Config_ReleaseVersion --license $1 --os $Config_OS --compiler $Config_Compiler --architecture $Config_Architecture --type $Config_Type --target_directory $BuildPath 
        if [ $? -ne 0 ];
        then
            printf "\nCannot run Melissa Updater. Please check your license string!\n"
            exit 1
        fi
    fi
    
    printf "Melissa Updater finished downloading $Config_FileName!\n"
}

CheckSOs() 
{
    if [ ! -f $BuildPath/$Config_FileName ];
    then
        echo "false"
    else
        echo "true"
    fi
}

########################## Main ############################
printf "\n======================== Melissa Name Object =======================\n                    [ Python3 | Linux | 64BIT ]\n"

# Get license (either from parameters or user input)
if [ -z "$license" ];
then
  printf "Please enter your license string: "
  read license
fi

# Check for License from Environment Variables 
if [ -z "$license" ];
then
  license=`echo $MD_LICENSE` 
fi

if [ -z "$license" ];
then
  printf "\nLicense String is invalid!\n"
  exit 1
fi

# Use Melissa Updater to download data file(s) 
# Download data file(s) 
DownloadDataFiles $license      # comment out this line if using DQS Release

# Set data file(s) path
#DataPath=""      # uncomment this line and change to your DQS Release data file(s) directory 

#if [ ! -d $DataPath ]; # uncomment this section of code if you are using your own DQS Release data file(s) directory
#then
    #printf "\nData path is invalid!\n"
    #exit 1
#fi

# Download SO(s)
DownloadSO $license 

# Check if all SO(s) have been downloaded. Exit script if missing
printf "\nDouble checking SO file(s) were downloaded...\n"

SOsAreDownloaded=$(CheckSOs)

if [ "$SOsAreDownloaded" == "false" ];
then
    printf "\n$Config_FileName not found"
    printf "\nMissing the above data file(s).  Please check that your license string and directory are correct.\n"

    printf "\nAborting program, see above.\n"
    exit 1
fi

printf "\nAll file(s) have been downloaded/updated!\n"

# Start
# Run project
if [ -z "$name" ];
then
    python3 $BuildPath/MelissaNameObjectLinuxPython3.py --license $license  --dataPath $DataPath
else
    python3 $BuildPath/MelissaNameObjectLinuxPython3.py --license $license  --dataPath $DataPath --name "$name"
fi

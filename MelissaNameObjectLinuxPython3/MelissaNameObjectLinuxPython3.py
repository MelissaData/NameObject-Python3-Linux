"""
Name Object automates the handling of name data, making it simple to send personalized
business mail, tailored specifically to the gender of the people in your mailing list,
while screening out vulgar or obviously false names.

High-level flow of this sample:
  1. SETUP     - create an mdName instance, hand it the license string and the path to
                 the data files, then InitializeDataFiles() (one time).
  2. INPUT     - feed a full name in with SetFullName().
  3. PROCESS   - Parse() splits the name; Genderize() and Salutate() derive the gender
                 and salutation from the parsed result.
  4. READ      - pull the individual fields back out with the Get* getters
                 (GetFirstName, GetLastName, GetGender, GetSalutation, ...).
  5. INTERPRET - GetResults() returns comma-separated result codes describing what the
                 object did/found; each code has a human description.

The pieces in this file map onto that flow:
  - run_as_console / parse_arguments : console harness (argument parsing + the interactive loop).
  - NameObject                       : thin wrapper around mdName that owns setup + the call sequence.
  - DataContainer                    : plain holder for one record's input and output.

Where mdName comes from:
  The mdName class lives in mdName_pythoncode.py, a generated Python wrapper over
  libmdName.so that the accompanying MelissaNameObjectLinuxPython3.sh script
  downloads on every run.

Reference:
  Quickstart    : https://docs.melissa.com/on-premise-api/name-object/name-object-quickstart.html
  Release notes : https://releasenotes.melissa.com/on-premise-api/name-object/
  Result codes  : https://docs.melissa.com/on-premise-api/name-object/result-codes.html
"""

import mdName_pythoncode
import os
import sys
import json


class DataContainer:
    """Data holder for a single record: carries the input name in and the result codes out."""
    def __init__(self, name="", result_codes=[]):

        # Input: the full name to process.
        self.name = name

        # Output: comma-separated result codes from GetResults().
        self.result_codes = result_codes

class NameObject:
    """
    Wrapper that owns a single Melissa Name Object instance and encapsulates the two
    things every Melissa object needs: one-time setup (license + data files) and the
    per-record processing sequence. Reuse one instance across many names; do NOT
    re-initialize per name.
    """
    def __init__(self, license, data_path):
        """
        Perform the mandatory one-time setup, in this required order:
          1. SetLicenseString    - authorize the object.
          2. SetPathToNameFiles  - tell it where the data files live.
          3. InitializeDataFiles - load the data into memory.

        Args:
            license: The Melissa license string used to authorize the object.
            data_path: Path to the folder containing the Name Object data files.
        """
        # Set license string and set path to data files
        # The underlying Melissa Name Object instance.
        self.md_name_obj = mdName_pythoncode.mdName()
        self.md_name_obj.SetLicenseString(license)
        # Path to the Name Object data files.
        self.data_path = data_path
        self.md_name_obj.SetPathToNameFiles(data_path)

        # Load the data files. The returned ProgramStatus reports whether initialization succeeded.
        # If you see a different date than expected, check your license string and either download the new data files
        # or use the Melissa Updater program to update your data files.
        p_status = self.md_name_obj.InitializeDataFiles()

        # If an issue occurred, please investigate the common causes.
        # Common causes: an invalid/expired license, or missing/wrong-path data files.
        if (p_status != mdName_pythoncode.ProgramStatus.NoError):
            print("Failed to Initialize Object.")
            print(p_status)
            return
        
        # Diagnostic information, handy for confirming the object loaded the data you expect:

        # Build date of the data files
        print(f"                DataBase Date: {self.md_name_obj.GetDatabaseDate()}")

        # When the license stops working
        print(f"              Expiration Date: {self.md_name_obj.GetLicenseExpirationDate()}")
      
        # This number should match with the file properties of the Melissa Object binary file.
        # If TEST appears with the build number, there may be a license key issue.
        print(f"               Object Version: {self.md_name_obj.GetBuildNumber()}\n")
    

    def execute_object_and_result_codes(self, data):
        """
        Run the full Name Object processing sequence for one name and capture its result
        codes. This is the canonical per-record call pattern to copy into your own
        application:
          ClearProperties -> SetFullName -> Parse -> Genderize -> Salutate -> GetResults

        Args:
            data: The record to process; its full name is read as input.

        Returns:
            A DataContainer carrying the same input plus this run's result codes.
        """
        # Reset any state left over from a previous name. Important when reusing the same
        # object across multiple records so fields from a prior name don't bleed into this one.
        self.md_name_obj.ClearProperties()

        # Supply the raw full-name string to process
        self.md_name_obj.SetFullName(data.name)

        # Split it into prefix/first/middle/last/suffix
        self.md_name_obj.Parse()

        # Infer gender from the parsed first name
        self.md_name_obj.Genderize()

        # Build a salutation from the parsed components
        self.md_name_obj.Salutate()

        # Collect the result codes for this run
        # ResultsCodes explain any issues Name Object has with the object.
        # List of result codes for Name Object
        # https://docs.melissa.com/on-premise-api/name-object/result-codes.html
        result_codes = self.md_name_obj.GetResults()

        return DataContainer(data.name, result_codes)


def parse_arguments():
    """
    Read the supported command-line options and return them as a (license, test_name,
    data_path) tuple.

    Recognized flags (each followed by its value, e.g. "--name Ray Melissa"):
      --license / -l   : the Melissa license string
      --name / -p      : a name to test in one-shot mode
      --dataPath / -d  : path to the Name Object data files

    Returns:
        A (license, test_name, data_path) tuple, each entry empty when its flag
        was not supplied.
    """
    license, test_name, data_path = "", "", ""

    args = sys.argv
    index = 0
    for arg in args:
        
        if (arg == "--license") or (arg == "-l"):
            if (args[index+1] != None):
                license = args[index+1]
        if (arg == "--name") or (arg == "-p"):
            if (args[index+1] != None):
                test_name = args[index+1]
        if (arg == "--dataPath") or (arg == "-d"):
            if (args[index+1] != None):
                data_path = args[index+1]
        index += 1

    return (license, test_name, data_path)

def run_as_console(license, test_name, data_path):
    """
    Set up the Name Object once, then drive the input -> process -> output cycle.

    In interactive mode (no --name) it loops, asking for a new name each pass until the
    user answers "N". In one-shot mode (--name supplied) it runs a single pass and exits.

    Args:
        license: The Melissa license string used to initialize the object.
        test_name: A full name to process in one-shot mode; if empty, the program prompts
            interactively.
        data_path: Path to the Name Object data files.
    """
    print("\n\n=========== WELCOME TO MELISSA NAME OBJECT LINUX PYTHON3 ===========\n")

    # Construct the wrapper. This is where the object is licensed, pointed at the data
    # files, and initialized (see the NameObject constructor above).
    name_object = NameObject(license, data_path)

    should_continue_running = True

    # Gate the program on a successful initialization. If the data files could not be
    # loaded (bad/expired license, missing or wrong-path data files, ...),
    # GetInitializeErrorString() returns the reason instead of "No Error" and we skip
    # the processing loop entirely.
    if name_object.md_name_obj.GetInitializeErrorString() != "No Error":
      should_continue_running = False
      
    while should_continue_running:
        if test_name == None or test_name == "":        
          # Interactive mode: prompt the user for a name.
          print("\nFill in each value to see the Name Object results")
          name = str(input("Name: "))
        else:        
          # One-shot mode: use the name passed on the command line.
          name = test_name

        # Holder for this pass's input and result codes.
        data = DataContainer(name)

        # Print user input
        print("\n============================== INPUTS ==============================\n")
        print(f"\t                Name: {name}")

        # Execute Name Object
        # Runs the parse/genderize/salutate sequence and returns the result codes.
        data_container = name_object.execute_object_and_result_codes(data)

        # Print output
        # Each Get* getter below returns one component the object produced for the most
        # recently processed name. These read directly from the mdName instance, which
        # still holds the results from the Execute call above. Prefix/First/Middle/Last/Suffix
        # come from Parse(), Gender from Genderize(), and Salutation from Salutate().
        print("\n============================== OUTPUT ==============================\n")
        print("\n\tName Object Information:")

        print(f"\t      Prefix: {name_object.md_name_obj.GetPrefix()}")
        print(f"\t  First Name: {name_object.md_name_obj.GetFirstName()}")
        print(f"\t Middle Name: {name_object.md_name_obj.GetMiddleName()}")
        print(f"\t   Last Name: {name_object.md_name_obj.GetLastName()}")
        print(f"\t      Suffix: {name_object.md_name_obj.GetSuffix()}")
        print(f"\t      Gender: {name_object.md_name_obj.GetGender()}")
        print(f"\t  Salutation: {name_object.md_name_obj.GetSalutation()}")
        print(f"\tResult Codes: {data_container.result_codes}")

        # Result codes come back as a single comma-separated string (e.g. "NS01,NS02").
        # Split it and ask the object for a readable description of each code.
        # ResultCodeDescriptionLong requests the long-form text; a short form is also
        # available via ResultCodeDescriptionShort
        rs = data_container.result_codes.split(',')
        for r in rs:
            print(f"        {r}: {name_object.md_name_obj.GetResultCodeDescription(r, mdName_pythoncode.ResultCdDescOpt.ResultCodeDescriptionLong)}")


        is_valid = False

        # In one-shot mode there is nothing more to do after a single pass: mark the
        # input handled and stop the outer loop.
        if not (test_name == None or test_name == ""):
            is_valid = True
            should_continue_running = False    
        # Interactive mode: ask whether to process another name. Keep prompting until we
        # get a valid Y/N. "N" ends the program; "Y" falls through to another pass.
        while not is_valid:
        
            test_another_response = input(str("\nTest another name? (Y/N)\n"))
            

            if not (test_another_response == None or test_another_response == ""):         
                test_another_response = test_another_response.lower()
            if test_another_response == "y":
                is_valid = True
            
            elif test_another_response == "n":
                is_valid = True
                should_continue_running = False            
            else:
            
              print("Invalid Response, please respond 'Y' or 'N'")

    print("\n============== THANK YOU FOR USING MELISSA PYTHON3 OBJECT ===========\n")
    


# ---------------------------- MAIN STARTS HERE ----------------------------

# Read the optional command-line arguments, then hand control to run_as_console, which
# performs the actual Name Object setup and processing.
license, test_name, data_path = parse_arguments()

run_as_console(license, test_name, data_path)
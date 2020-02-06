import threading
import zipfile
import sys
from os import system
from os import path
from timeit import default_timer as timer

class AsyncZip(threading.Thread):
    """Uses ZipFile to zip up a list (even of 1) of files and folders."""
    def __init__(self, infileTupleList, outfile):
        threading.Thread.__init__(self)
        self.infileTupleList = infileTupleList
        self.outfile = outfile
    def run(self):

        with zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED) as f:
            # Unpack the tuple list
            for tup in self.infileTupleList:
                fileName, isFolder = tup
                if isFolder:
                    pass #TODO deal with this later
                else:
                    f.write(fileName)
            zipInfoList = (f.infolist())
        count = len(zipInfoList)
        if count == 1:
            noun = 'file'
        else:
            noun = 'files'
        print(f'\nThe archive contains {count} {noun}:\n')
        for zippedObjectInfo in zipInfoList:
            zippedFileName = zippedObjectInfo.filename
            zippedFileCRC = zippedObjectInfo.CRC
            zipUncompSize = zippedObjectInfo.file_size
            zipCompSize = zippedObjectInfo.compress_size
            zipPercent = int(round((zipCompSize/zipUncompSize)*100))
            print(f'{zippedFileName}')
            print(f'\tCompressed to:  {zipPercent}%')
            print(f'\tOriginal size:  {zipUncompSize} bytes')
            print(f'\tCompressed size:  {zipCompSize} bytes')
            print(f'\tCRC32 hash:  {zippedFileCRC}\n')

def getInput():
    """Takes a user provided list of files and/or folders, as well as the name 
    of the proposed zip archive.  
    
    The validated list and the zip archive name are returned from the function.
    
    The output of the function is a tuple with the list and the zipped archive
    name.  Each entry in the validated list is a tuple with the name of the
    file or folder and a boolean which identifies it as a file (False) or a 
    folder (True)."""
    validatedInput = []
    system('cls')
    # Get input
    userRequest = input('File(s) and/or folders you want to zip (use spaces to'
        + ' seperate filenames):  ')
    zipFileName = input('What do you want to call the archive?  ')
    # Convert input into a list
    fileList = userRequest.split()
    
    # Validate the list:
    # For each item in the list test to see if it is a file or folder and 
    #   append to the validated list a tuple with (name, isFolder)
    #   If a test fails notify the user and exit()
    for name in fileList:
        if path.isdir(name):
            validatedInput.append((name, True))
        elif path.isfile(name):
            validatedInput.append((name, False))
        else:
            print(f'\n{name} is not the name of a file or folder.  Operation '
                + 'aborted.\n')
            sys.exit()
    return (validatedInput, zipFileName)




#TODO implement a list of files
    #TODO def an input function
        # list of args as filenames
        # test the filenames to see if they exist
        # zip the files with AsyncZip
#TODO  or a folder name
#TODO implement TRY blocks on the file operations
#TODO make it into an executable

# TODO 4. Call the input function
zipParam = getInput()
# Unpack the params
listToZip, zippedArchiveName = zipParam
# TODO 4.3 format the list for use in AsyncZip

# TODO 5. Call AsyncZip on the list (even if it is only one)
background = AsyncZip(listToZip, zippedArchiveName)
start = timer()
background.start()
# TODO update this when adding folders
print(f'Zipping {len(listToZip)} files to {zippedArchiveName}...')
background.join()
end = timer()
if len(listToZip) == 1:
    noun = 'file'
else: 
    noun = 'files'
print(f'It took {end - start} seconds to zip the {noun}.')

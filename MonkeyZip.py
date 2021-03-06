"""Uses ZipFile to zip up a list (even of 1) of files and folders.
Empty subfolders are ignored."""
import threading
import zipfile
import sys
import glob

from os import system
from os import path

from time import time

class AsyncZip(threading.Thread):
    def __init__(self, infileList, outfile):
        threading.Thread.__init__(self)
        self.infileList = infileList
        self.outfile = outfile
    def run(self):
        with zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED) as f:
            for item in self.infileList:
                if path.isdir(item):
                    # Subfolder detected, add contents to self.infileList
                    print(f'Opening folder: {item}')
                    dirContents = glob.glob(item + '/*')
                    for subitem in dirContents:
                        self.infileList.append(subitem)
                elif path.isfile(item):
                    f.write(item)
                else:
                    print(f'{item} is not a valid file or folder...ignoring...')  
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
    #   append to the validated list
    #   If a test fails notify the user and exit()
    for name in fileList:
        if path.isdir(name):
            validatedInput.append(name) 
        elif path.isfile(name):
            validatedInput.append(name)
        else:
            print(f'\n{name} is not the name of a file or folder.  Operation '
                + 'aborted.\n')
            sys.exit()
    return (validatedInput, zipFileName)

# Check to see if the user sent arguments from the command line
argCount = len(sys.argv)
if argCount > 1:
    #Get args from argv[1] to argv[len - 2] these are files/folders to zip
    listOfFilesOrFolders = []
    for index in range (1, argCount - 1):
        listOfFilesOrFolders.append(sys.argv[index])
    #Get argv[len -1] this is the zip archive name to be written
    zipFileName = sys.argv[argCount - 1]
    background = AsyncZip(listOfFilesOrFolders, zipFileName)
    start = time()
    background.start()
    print(f'Zipping to {zipFileName}...\n')
    background.join()
    end = time()
    if len(listOfFilesOrFolders) == 1:
        noun = 'file'
    else:
        noun = 'files'
    print(f'It took {end - start} seconds to zip the {noun}.')
else:
    # Call the input function
    zipParam = getInput()
    # Unpack the params
    listToZip, zippedArchiveName = zipParam
    # Call AsyncZip on the list (even if it is only one)
    background = AsyncZip(listToZip, zippedArchiveName)
    start = time()
    background.start()
    print(f'Zipping {len(listToZip)} files or folders to {zippedArchiveName}...')
    background.join()
    end = time()
    if len(listToZip) == 1:
        noun = 'file'
    else: 
        noun = 'files'
    print(f'It took {end - start} seconds to zip the {noun}.')
    

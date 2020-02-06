import threading
import zipfile
import sys
from os import system
from os import path
from timeit import default_timer as timer
#TODO 3. Take input as a list (even if there is only one.)
class AsyncZip(threading.Thread):
    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def run(self):
        with zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED) as f:
            f.write(self.infile)
            zipInfoList = (f.infolist())
        #TODO 2.1 Change output text
        print('Finished background zip of :', self.infile)
        count = len(zipInfoList)
        if count == 1:
            noun = 'file'
        else:
            noun = 'files'
        print(f'The archive contains {count} {noun}:\n')
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
# TODO 1. Define an input function which will allow entry of file or files 
# seperated by commas or spaces.  Check to see if the files exist or if the 
# name is a folder.  Return an error if not.
def getInput():
    validatedInput = []
    system('cls')
    # Get input
    userRequest = input('File(s) and/or folders you want to zip (use spaces to'
        + 'seperate filenames):  ')
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
            print(f'{name} is not the name of a file or folder.  Operation '
                + 'aborted.')
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
# TODO 5. Call AsyncZip on the list (even if it is only one)
background = AsyncZip(fileToZip, zipFileName)
start = timer()
background.start()
print('Zipping {} to {}...'.format(fileToZip, zipFileName))
background.join()
end = timer()
print('It took {} seconds to zip the file.'.format(end - start))

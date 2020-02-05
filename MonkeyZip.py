import threading
import zipfile
from os import system
from timeit import default_timer as timer

class AsyncZip(threading.Thread):
    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def run(self):
        with zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED) as f:
            f.write(self.infile)
            zipInfoList = (f.infolist())
            
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

        
system('cls')
fileToZip = input('File you want to zip:  ')
zipFileName = input('Zipped filename:  ')

#TODO implement a list of files
    #TODO def an input function
        # list of args as filenames
        # test the filenames to see if they exist
        # zip the files with AsyncZip
#TODO  or a folder name
#TODO make it into an executable

background = AsyncZip(fileToZip, zipFileName)
start = timer()
background.start()
print('Zipping {} to {}...'.format(fileToZip, zipFileName))
background.join()
end = timer()
print('It took {} seconds to zip the file.'.format(end - start))

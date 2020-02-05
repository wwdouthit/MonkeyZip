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
            print(f'{zippedFileName}')
            print(f'\tCompression percentage: {(1-zipCompSize/zipUncompSize) * 100}%.')
            print(f'{zippedFileName} was originally {zipUncompSize} bytes.')
            print(f'{zippedFileName} compressed to {zipCompSize} bytes.')
            print(f'The CRC32 hash of {zippedFileName} is {zippedFileCRC}.')

        
system('cls')
fileToZip = input('File you want to zip:  ')
zipFileName = input('Zipped filename:  ')

#TODO get/print the original size, compression size, and crc32 value
    # Fix the url for the repository (still references MonkeyBrat70)
    # Round the percentage to a whole number
    # Reformat the text to indent info with category and value rather than
    #   sentences
#TODO implement a list of files
#TODO  or a folder name
#TODO make it into an executable

background = AsyncZip(fileToZip, zipFileName)
start = timer()
background.start()
print('Zipping {} to {}...'.format(fileToZip, zipFileName))
background.join()
end = timer()
print('It took {} seconds to zip the file.'.format(end - start))

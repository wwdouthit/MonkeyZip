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
        print('Finished background zip of :', self.infile)
system('cls')
fileToZip = input('File you want to zip:  ')
zipFileName = input('Zipped filename:  ')

#TODO get/print the original size, compression size, and crc32 value
#TODO make it into an executable

background = AsyncZip(fileToZip, zipFileName)
start = timer()
background.start()
print('Zipping {} to {}...'.format(fileToZip, zipFileName))

background.join()
end = timer()
print('It took {} seconds to zip the file.'.format(end - start))

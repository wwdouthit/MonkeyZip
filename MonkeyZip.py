import threading
import zipfile
from timeit import default_timer as timer

class AsyncZip(threading.Thread):
    def __init__(self, infile, outfile):
        threading.Thread.__init__(self)
        self.infile = infile
        self.outfile = outfile

    def run(self):
        with zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED) as f:
            f.write(self.infile)
        # f = zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED)
        # f.write(self.infile)
        # f.close()
        print('Finished background zip of :', self.infile)

fileToZip = input('File you want to zip:  ')
zipFileName = input('Zipped filename:  ')

#TODO get/print the original size, compression size, and crc32 value
background = AsyncZip(fileToZip, zipFileName)
start = timer()
background.start()
print('The main program continues to run in the foreground.')

background.join()
end = timer()
print('It took {} seconds to zip the file.'.format(end - start))

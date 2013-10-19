import os
from optparse import OptionParser

from mxsrunner import *

parser = OptionParser()
parser.add_option('-f', dest='filename', help='Maxscript FILENAME')

(options, args) = parser.parse_args()

if __name__ == '__main__':
    mxs = MxsRunner(os.path.dirname(__file__))
    if options.filename:
        mxs.settings.setconfig('Settings', 'Filename', options.filename)

    mxs.run()
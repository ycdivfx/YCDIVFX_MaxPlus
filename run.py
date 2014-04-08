from optparse import OptionParser

import maxpycharm

parser = OptionParser()
parser.add_option('-f', dest='filename', help='Maxscript FILENAME')

(options, args) = parser.parse_args()

if __name__ == '__main__':
    if options.filename:
        cmd = r'python.ExecuteFile @"%s";' % options.filename
        maxpycharm.PyCharm3dsMax.sendCmdToMax(cmd)
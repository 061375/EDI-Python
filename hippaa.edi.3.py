import array
import string
import sys
import getopt

# http://code.activestate.com/recipes/299485-parsing-out-edi-messages/

try:
    # If available use the psyco optimizing routines.  This will speed
    # up execution by 2x.
    import psyco.classes
    base_class = psyco.classes.psyobj
except ImportError:
    base_class = object

alphanums = string.ascii_letters + string.digits

class BadFile(Exception):
    """Raised when file corruption is detected."""

class Parser(base_class):
    """Parse out segments from the X12 raw data files.

    Raises the BadFile exception when data corruption is detected.

    Attributes:
        delimiters
            A string where
            [0] == segment separator
            [1] == element separator
            [2] == sub-element separator
            [3] == repetition separator (if ISA version >= 00405
    """
    def __init__(self, filename=None):
        self.delimiters = ''
        self.errorcount = 0
        if filename:
            self.open_file(filename)

    def __iter__(self):
        """Return the iterator for use in a for loop"""
        return self

    def open_file(self, filename):
        self.fp = open(filename, 'rb')
        self.in_isa = False

    def fix_bytestring(self, tmp):
        # A hack to recreate array.tostring() for PY3
        # here we will determine if each key in our tmp list needs conversion to string from bytes
        # this is because sometimes the key is an integer (mixed)
        # @var string
        r = ''
        for t in tmp:
            try:
                t = t.decode()
            except AttributeError:
                pass
            r = r + t
        return r

    def __next__(self):
        """return the next segment from the file or raise StopIteration

        Here we'll return the next segment, this will be a 'bare' segment
        without the segment terminator.

        We're using the array module.  Written in C this should be very
        efficient at adding and converting to a string.
        """

        # @var array mixed
        seg = []
        if not self.in_isa:
            #We're at the begining of a file or interchange so we need
            #to handle it specially.  We read in the first 105 bytes,
            #ignoring new lines.  After that we read in the segment
            #terminator.
            while len(seg) != 106:
                i = self.fp.read(1)
                #print(i)
                if i == '\0': continue
                if i == '':
                    if len(seg) == 0:
                        # We have reached the end of the file normally.
                        raise StopIteration
                    else:
                        # We have reached the end of the file, this is an error
                        # since we are in the middle of an ISA loop.
                        raise BadFile('Unexpected EOF found')
                if len(seg) < 105:
                    # While we're still gathering the 'main' portion of the
                    # ISA, we ignore NULLs and newlines.
                    if i != '\n':
                        # We're still in the 'middle' of the ISA, we won't
                        # accept NULLs or line feeds.
                        try:
                            seg.append(i.decode())
                        except TypeError:
                            # This should never occur in a valid file.
                            print ('Type error on appending "%s" 1' % i)
                else:
                    # We're at the end of the ISA, we'll accept *any*
                    # character except the NULL as the segment terminator for
                    # now.  We'll check for validity next.
                    if i == '\n':
                        # Since we're breaking some lines at position
                        # 80 on a given line, we need to also check the
                        # first character after the line break to make
                        # sure that the newline is supposed to be the
                        # terminator.  If it is, we just backup to
                        # reset the file pointer and move on.
                        pos = self.fp.tell()
                        next_char = self.fp.read(1)
                        if next_char != 'G':
                            i = next_char
                        else:
                            self.fp.seek(pos)
                    try:
                        seg.append(i)
                    except TypeError:
                        print ('Type error on appending "%s" 2' % i)

            # seg is an array that represetns the ISA (first line)
            # version seg from [] 84 through 89
            self.version = ''.join(seg[84:89])
            # delimeters
            # generally
            # ~ end of line
            # * delimeter within a statement
            # > end of ISA
            self.delimiters = self.fix_bytestring([seg[105],seg[3],seg[104]])
            
            if self.version >= '00405':
                self.delimiters = self.fix_bytestring([seg[105],seg[3],seg[104],seg[83]])

            # Verify that the delimiters are valid.
            for delim in self.delimiters:
                if delim in alphanums:
                    raise BadFile('"%s" is not a valid delimiter' % delim)

            # Set the flag to process everything else as normal segments.
            self.in_isa = True

            # Pop off the segment terminator.
            seg.pop()
            return self.fix_bytestring(seg)
        else:
            #We're somewhere in the body of the X12 message.  We just
            #read until we find the segment terminator and return the
            #segment.  (We still ignore line feeds unless the line feed
            #is the segment terminator.
            
            # commented out next 3 lines at suggestion of another user
            # stops infinite loop however this needs to be addressed as the
            # block is there to handle multiple EDI in one stream

            #if self.delimiters[0] == '\n':
            #    return self.fp.readline()[:-1]
            #else:
                fp_read = self.fp.read
                while 1:
                    i = fp_read(1)
                    i = self.fix_bytestring([i])

                    '''
                        Handle corrupt file
                    '''
                    if i=='':
                        self.errorcount += 1
                    if self.errorcount > 100:
                        raise BadFile('File appears to be corrupt. Possible endless loop detected.')

                    if i == '\0': continue

                    # handles endless loop due to empty lines at end of file
                    if len(self.delimiters) < 1: 
                        sys.exit() # BAD JEREMY - FIX THIS

                    if i == self.delimiters[0]:
                        # End of segment found, exit the loop and return the
                        # segment.
                        segment = self.fix_bytestring(seg)
                        if segment.startswith('IEA'):
                            self.in_isa = False
                        return segment
                    elif i != '\n':
                        try:
                            seg.append(i)
                        except TypeError:
                            raise BadFile('Corrupt characters found in data or unexpected EOF')

'''
    Get the file from the CMD and then run it
'''
def main(argv) :
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
    except getopt.GetoptError:
      print ('hippaa.edi.3.py -i <inputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print ('hippaa.edi.3.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg

    message = Parser('files/' + arg)
    for segment in message:
        if(len(message.delimiters) > 1):
            elements = segment.split(message.delimiters[1])
            # Dispatch based on elements[0]...
            print(elements)

if __name__ == '__main__':
    main(sys.argv[1:])  
    
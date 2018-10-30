import urllib
import urllib2

url = 'http://localforage.localhost/test.php'

# Prepare the data
query_args = { 'v':'this should write to a file' }

# This urlencodes your data (that's why we need to import urllib at the top)
data = urllib.urlencode(query_args)

# Send HTTP POST request
request = urllib2.Request(url, data)

response = urllib2.urlopen(request)
 
html = response.read()

# Print the result
print html
"""
response = urllib2.urlopen('http://192.168.1.77')
#print "Response:", response

# Get the URL. This gets the real URL. 
print "The URL is: ", response.geturl()

# Getting the code
print "This gets the code: ", response.code

# Get the Headers. 
# This returns a dictionary-like object that describes the page fetched, 
# particularly the headers sent by the server
print "The Headers are: ", response.info()

# Get the date part of the header
print "The Date is: ", response.info()['date']

# Get the server part of the header
print "The Server is: ", response.info()['server']

# Get all data
html = response.read()
#print "Get all data: ", html

# Get only the length
print "Get the length :", len(html)

# Showing that the file object is iterable
for line in response:
 print line.rstrip()

# Note that the rstrip strips the trailing newlines and carriage returns before
# printing the output.
"""
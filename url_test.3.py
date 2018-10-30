import urllib.request
with urllib.request.urlopen("http://www.jeremyheminger.com") as url:
    s = url.read()
#I'm guessing this would output the html source code?
print(s)
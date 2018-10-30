import pyodbc 
print(pyodbc.drivers())
cnxn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                      "server=192.168.1.24;"
                      "database=EDI;"
                      "uid=edi;"
                      "pwd=Z.Dy2r7li")

cursor = cnxn.cursor()
cursor.execute('SELECT * FROM ProlineDisplays')

for row in cursor:
    print('row = %r' % (row,))
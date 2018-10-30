from tstpydb import tstpydb

'''
USAGE EXAMPLES
'''

db = tstpydb.tstPyDb('_pyodbc',{
	"driver":"ODBC Driver 13 for SQL Server",
	"server":"192.168.1.24",
	"database":"EDI",
	"user":"edi",
	"password":"Z.Dy2r7li"
})

'''
SELECT
'''
c = db.select('ProlineDisplays',["*"],False).get()
for row in c:
    print('row = %r' % (row,))

print("_________________________________")

'''
EXECUTE - Allows a string SQL to be passed
'''
c = db.execute('SELECT * FROM ProlineDisplays',False).get()
for row in c:
    print('row = %r' % (row,))
print("_________________________________")

'''
UPDATE
'''
db.update('EnviroData',
{
	"temp":"100"
},
{
	"machine":"enviropiI"
})

'''

c = tstpydb.tstPyDb('_pyodbc',{
	"driver":"ODBC Driver 13 for SQL Server",
	"server":"192.168.1.24",
	"database":"EDI",
	"user":"edi",
	"password":"Z.Dy2r7li"
}).select('ProlineDisplays',["*"],False).get()
for row in c:
    print('row = %r' % (row,))
'''
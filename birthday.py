#!/usr/bin/python
try:
    import MySQLdb
    # module has to be downloaded from http://sourceforge.net/projects/mysql-python/
except ImportError:
    print ("To run this program download MySQLdb module from http://sourceforge.net/projects/mysql-python")
    exit()
import cgi
    
def htmlHeader(title):
    print ("Content-type: text/html")
    print ()
    print ("""<HTML>
    <HEAD>
    <TITLE>%s</TITLE>
    </HEAD>
    <BODY>
    <IMG SRC='../icons/python-powered-w-200x80.png' ALIGN="LEFT">
    <IMG SRC='../icons/powered-by-mysql-167x86.png'ALIGN="RIGHT">
    <DIV ALIGN="CENTER">
    <H1>Birthdays Database %s</H1><BR /><HR />""" % (title, title))
    
def htmlFooter():
    print ('<div align="center"><hr /><IMG SRC="../icons/apache_pb.gif">')
    print ('<BR /><font size="4">Created by Keith Wright<br />September 1, 2008</font>')
    formHeader()
    print ('<INPUT TYPE="SUBMIT" VALUE="Show Code"><INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Code">')
    formFooter()
    print ('</div></DIV></BODY></HTML>')

def formHeader():
    print ("""<FORM METHOD="GET" ACTION="birthday.py">""")
    
def formFooter():
    print ("""</FORM>""")
    
def openDb():
    global row, connection, cursor 
    try:
        connection = MySQLdb.connect(host="localhost",user="userbday1",passwd='passbday1',db="birthdays", port=3306)
        cursor = connection.cursor()
    except:
        print ('Error Connecting to the birthdays database!')
        print ('Make sure the MySQL database "birthdays" exists and the user, userbday1, has the correct password and proper privileges.')
        #mysql>  grant all privileges on birthdays.* to userbday1@localhost identified by 'passbday1';
        
def createTable(tblname):
    openDb()
    sqlstring = 'CREATE TABLE ' + tblname + '(FirstName char(20), LastName char(30), BirthDate date);'
    cursor.execute(sqlstring)
    connection.close()
    return sqlstring

def confirmForm(sqlstring):
    formHeader()
    print ('<table border="0"><tr><INPUT TYPE="HIDDEN" NAME="SQL" VALUE="'+sqlstring+'">'+sqlstring+'</tr>')
    print ('<th><INPUT NAME="Confirm" TYPE="SUBMIT" VALUE="Yes"></th>')
    print ('<th><INPUT NAME="Confirm" TYPE="SUBMIT" VALUE="No">')
    print ('<INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Confirm"></th></table>')
    formFooter()
    htmlFooter()
    
def execSQL(sqlstring,confirm=False):
    global rows
    if confirm:        
        confirmForm(sqlstring)
    else:
        print (sqlstring  + '<BR />')
        openDb()
        cursor.execute(sqlstring)
        connection.close()
        rows = cursor.fetchall()
        
def addRecord(fname,lname,bdate):
    sqlstring = "INSERT INTO birthdays(FirstName, LastName, BirthDate) VALUES ('"+fname+"','"+lname+"','"+bdate+"');"
    execSQL(sqlstring, confirm=True)
    return sqlstring
    
def updateRecord(key,fname,lname,bdate):
    sqlstring = "UPDATE birthdays SET FirstName='"+fname+"', LastName='"+lname+"', BirthDate='"+bdate+"' \
    WHERE FirstName='"+key+"';"
    execSQL(sqlstring,confirm=True)
    return sqlstring

def searchAllRecords():
    sqlstring = "SELECT * FROM birthdays;"
    execSQL(sqlstring)
    return sqlstring
    
def sortRecords(field, dir='ASC', SQL='SELECT * FROM birthdays;'):
    #sqlstring = SQL[:-2] +" ORDER BY " + str(field) +" "+ dir + ";"
    # AFTER the existing Order by or after existing Where or database
    if SQL[-2]=='C': # ALREADY SORTED
        sqlstring=SQL[:-1] + ", " + str(field) +" "+ dir + ";"
    else:
        sqlstring=SQL[:-1] + " ORDER BY " + str(field) +" "+ dir + ";"
    execSQL(sqlstring)
    return sqlstring
  
def searchRecord(fname=None,lname=None,bdate=None):
    global rows
    sqlstring = "SELECT * FROM birthdays "
    if not (fname or lname or bdate):
        sqlstring +=";"
    else:
        sqlstring +="WHERE "        
        if fname:
            sqlstring += "FirstName ='" + fname +"' "
            if lname:
                sqlstring += "and LastName ='" + lname +"' "
                if bdate:
                    sqlstring += "and BirthDate ='" + bdate +"' "
            else:
                if bdate:
                    sqlstring += "and BirthDate ='" + bdate +"' "
        elif lname:
                sqlstring += "LastName ='" + lname +"' "
                if bdate:
                    sqlstring += "and BirthDate ='" + bdate +"' "
        else:
            if bdate:
                sqlstring += "BirthDate ='" + bdate +"' "
        sqlstring +=";"
    execSQL(sqlstring)
    return sqlstring
    
def delRecord(fname):
    sqlstring = "DELETE FROM birthdays WHERE (FirstName = '"+fname+"');"
    execSQL(sqlstring, confirm=True)
    return sqlstring
    
def listRecords(sqlstring):
    record = 0
    formHeader()
    print ('<table border="1"><tr><th><INPUT NAME="Field" TYPE="SUBMIT" VALUE="FirstName">')
    print ('<INPUT TYPE="HIDDEN" NAME="SQL" VALUE="'+sqlstring+'">')
    print ('<INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Sort">')
    print ('ASC<INPUT TYPE="RADIO" CHECKED NAME="Direction" VALUE="ASC">')
    print ('DESC<INPUT TYPE="RADIO" NAME="Direction" VALUE="DESC"></th>')
    formFooter()
    formHeader()
    print ('<th><INPUT NAME="Field" TYPE="SUBMIT" VALUE="LastName">')
    print ('<INPUT TYPE="HIDDEN" NAME="SQL" VALUE="'+sqlstring+'">')
    print ('<INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Sort">')
    print ('ASC<INPUT TYPE="RADIO" CHECKED NAME="Direction" VALUE="ASC">')
    print ('DESC<INPUT TYPE="RADIO" NAME="Direction" VALUE="DESC"></th>')
    formFooter()
    formHeader()
    print ('<th><INPUT NAME="Field" TYPE="SUBMIT" VALUE="BirthDate">')
    print ('<INPUT TYPE="HIDDEN" NAME="SQL" VALUE="'+sqlstring+'">')
    print ('<INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Sort">')
    print ('ASC<INPUT TYPE="RADIO" CHECKED NAME="Direction" VALUE="ASC">')
    print ('DESC<INPUT TYPE="RADIO" NAME="Direction" VALUE="DESC"></th>')
    formFooter()
    formHeader()
    print ('<th colspan="2"><INPUT NAME="Field" TYPE="SUBMIT" VALUE="Clear Sort">')
    print ('<INPUT TYPE="HIDDEN" NAME="SQL" VALUE="'+sqlstring+'">')
    print ('<INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Sort"></th></tr>')
    formFooter()
    for row in rows:
        print ('<tr>')
        formHeader()
        print ('<td><INPUT NAME="FirstName" TYPE="TEXT" SIZE="20" MAXLENGTH="20" VALUE="' + \
        row[0] +'"</td>' + \
        '<td><INPUT NAME="LastName" TYPE="TEXT" SIZE="30" MAXLENGTH="30" VALUE="' + \
        row[1] +'"</td>' + \
        '<td><INPUT NAME="BirthDate" TYPE="TEXT" SIZE="10" MAXLENGTH="10" VALUE="' + \
        str(row[2]) +'"</td>')
        print ('<td><INPUT TYPE="SUBMIT" VALUE="Edit">')
        print ('<INPUT TYPE="HIDDEN" NAME="Key" VALUE="'+row[0]+'">',)
        print ('<INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Edit"></td>')
        formFooter()
        formHeader()
        print ('<td><INPUT TYPE="SUBMIT" VALUE="Delete">',)
        print ('<INPUT TYPE="HIDDEN" NAME="Key" VALUE="'+row[0]+'">',)
        print ('<INPUT TYPE="HIDDEN" NAME="Flag" VALUE="Delete"></td>')
        print ('</tr>')
        formFooter()
        record +=1
    else:
        formHeader()
        print ("""
        <td><INPUT NAME="FirstName" TYPE="TEXT" SIZE="20" MAXLENGTH="20"></td>
        <td><INPUT NAME="LastName" TYPE="TEXT" SIZE="30" MAXLENGTH="30"></td>
        <td><INPUT NAME="BirthDate" TYPE="TEXT" SIZE="10" MAXLENGTH="10"></td>
        <td><INPUT TYPE="HIDDEN" NAME="Flag" VALUE="AddSearch">
        <INPUT TYPE="SUBMIT" VALUE="Add" NAME="SUBMIT"></td>
        <td><INPUT TYPE="SUBMIT" VALUE="Search" NAME="SUBMIT"></td>""")
        formFooter()
        print ('</table>',)
    
def showCode():
    print ("Content-type: text/plain")
    print ("")
    f = open("birthday.py")
    for line in f:
        print (line,)
    f.close()
    
def main():
    form = cgi.FieldStorage()
    if not form.has_key('Flag'):
        htmlHeader("Welcome!")
        sqlstring=searchAllRecords()
        listRecords(sqlstring)
        htmlFooter()
    elif form['Flag'].value == 'Sort':
        htmlHeader("Sorted Records")
        if form['Field'].value =='Clear Sort':
            sqlstring=form['SQL'].value
            if not sqlstring[-2]=='s': #not sorted
                sqlstring=sqlstring[:sqlstring.find('ORDER')-1]+";"
            execSQL(sqlstring)
        else:
            sqlstring=sortRecords(form['Field'].value,form['Direction'].value,form['SQL'].value)
        listRecords(sqlstring)
        htmlFooter()
    elif form['Flag'].value =='AddSearch' and form['SUBMIT'].value == 'Add':
        if not (form.has_key('FirstName') and form.has_key('LastName') and form.has_key('BirthDate')):
            htmlHeader("Unable to Add Incomplete Record")
            sqlstring=searchAllRecords()
            listRecords(sqlstring)
            htmlFooter()
        else:
            htmlHeader("Add Record?")
            sqlstring=addRecord(form['FirstName'].value, form['LastName'].value, form['BirthDate'].value)
        
    elif form['Flag'].value =='AddSearch' and form['SUBMIT'].value == 'Search':
        htmlHeader("Searched Record(s)")
        if form.has_key('FirstName'):
            firstname = form['FirstName'].value
            if form.has_key('LastName'):
                lastname = form['LastName'].value
                if form.has_key('BirthDate'):
                    birthdate = form['BirthDate'].value
                    sqlstring=searchRecord(fname=firstname,lname=lastname,bdate=birthdate)
                else:
                    sqlstring=searchRecord(fname=firstname,lname=lastname)
            elif form.has_key('BirthDate'):
                birthdate = form['BirthDate'].value
                sqlstring=searchRecord(fname=firstname,bdate=birthdate)
            else:
                searchRecord(fname=firstname)
        elif form.has_key('LastName'):
                lastname = form['LastName'].value
                if form.has_key('BirthDate'):
                    birthdate = form['BirthDate'].value
                    sqlstring=searchRecord(lname=lastname, bdate=birthdate)
                else:
                    sqlstring=searchRecord(lname=lastname)
        else:
            if form.has_key('BirthDate'):
                birthdate = form['BirthDate'].value
                sqlstring=searchRecord(bdate=birthdate)
            else:
                sqlstring=searchAllRecords()
        listRecords(sqlstring)
        htmlFooter()
    elif form['Flag'].value =='Delete':
        htmlHeader("Delete Record?")
        sqlstring=delRecord(form['Key'].value)
    elif form['Flag'].value =='Edit':
        htmlHeader("Update Record?")
        sqlstring=updateRecord(form['Key'].value, form['FirstName'].value, form['LastName'].value, form['BirthDate'].value)
    elif form['Flag'].value =='Confirm':
        if form['Confirm'].value == 'Yes':
            htmlHeader("Updated Database")
            sqlstring=form['SQL'].value
            execSQL(sqlstring)
        else:
            htmlHeader("Update Aborted")
        sqlstring=searchAllRecords()
        listRecords(sqlstring)
        htmlFooter()
    elif form['Flag'].value =='Code':
        showCode()
    else:
        htmlHeader("What are you doing here?")
        sqlstring=searchAllRecords()
        listRecords(sqlstring)
        htmlFooter()
        
def testDb():
    htmlHeader('Connecting to Database')
    try:
        openDb()
    except:
        print ('Error Connecting to the Birthdays Database!')
    try:
        print (createTable('birthdays'))
        # use above to create table the first time
    except:
        print ('Table Birthdays already exists')
    finally:
        htmlFooter()
    
if __name__ == "__main__":
    testDb()
    main()

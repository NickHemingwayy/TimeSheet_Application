from datetime import *

import os
import _sqlite3
from dotenv import load_dotenv

conn = _sqlite3.connect(r'C:\Users\nhemingway\PycharmProjects\TimeSheet\TimeSheet.db')
cursor = conn.cursor()

load_dotenv()

host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
database = os.getenv('DATABASE')


'''Any and All interactions with the DB are done through here'''


# when user logs in: Check if username is in DB to gain access
def validateLogin(userName):
    cursor.execute('''
                        SELECT username
                        FROM employee
                        WHERE username = ?

                      ''', (userName.lower(),))
    result = cursor.fetchall()
    if len(result) > 0:
        return True
    else:
        return False


# Checks if logged in user has admin privileges (TimeSheet will vary accordingly)
def isAdmin(userName):
    comboListAdmin = []
    cursor.execute('''
                            SELECT isadmin
                            FROM employee
                            WHERE username = ?
                          ''', (userName.lower(),))
    result = cursor.fetchall()

    if len(result) > 0:
        for row in result:
            comboListAdmin += row
        return comboListAdmin
    else:
        return ""


# Takes username and retrieves departments which they belong to
def combo1_1Vals(userName):
    comboListDep = []

    cursor.execute('''
                            SELECT dep_id
                            FROM employee
                            WHERE username = ?
                          ''', (userName.lower()))
    result = cursor.fetchall()
    if len(result) > 0:
        for row in result:
            comboListDep += row
            print(comboListDep)
        return comboListDep
    else:
        return ""


# Takes Selected Department and retrieves Legal Entities
def combo1_2Vals(dep):
    cursor.execute('''
                            SELECT DISTINCT legalEntity
                            FROM process_list
                            WHERE dep =  ?

                          ''', (dep))
    result = cursor.fetchall()
    comboList = []
    if len(result) > 0:
        for row in result:
            comboList += row
        return comboList
    else:
        return ""


# Takes selected Legal Entity and retrieves Tasks
def combo1_3Vals(legalEnt, dep):
    cursor.execute('''
                            SELECT DISTINCT Task
                            FROM process_list
                            WHERE legalEntity = ? AND dep = ?;

                          ''', (legalEnt, dep))
    result = cursor.fetchall()
    comboListTask = []
    if len(result) > 0:
        for row in result:
            comboListTask += row
        return comboListTask
    else:
        return ""


# Takes selected Legal Entity and retrieves Tasks
def combo1_4Vals(task, legalEnt, dep):
    cursor.execute('''
                            SELECT Customer
                            FROM process_list
                            WHERE Task = ?  AND legalEntity = ? AND dep = ?;

                          ''', (task, legalEnt, dep))
    result = cursor.fetchall()
    comboListTask = []
    if len(result) > 0:
        for row in result:
            comboListTask += row
        return comboListTask
    else:
        return ""


# Fills time-off Comboboxes
def TimeOff():
    cursor.execute('''
                                SELECT timeoff_type
                                FROM timeoff

                              ''')
    result = cursor.fetchall()
    comboListTimeOff = []
    if len(result) > 0:
        for row in result:
            comboListTimeOff += row
        return comboListTimeOff
    else:
        return ""


# On submit, all entered fields are pushed to DB under logged in User
def pushToDB(submitLst):
    count = 0
    for i in submitLst:
        dep = str(submitLst[count][0])
        ent = str(submitLst[count][1])
        task = str(submitLst[count][2])
        customer = str(submitLst[count][3])
        hours = str(submitLst[count][4])
        date = str(submitLst[count][5])
        user = str(submitLst[count][6])
        count += 1
        cursor.execute('''
                                    INSERT INTO timesheet (dep_name, legalent_name,task_name, customer, hours, dateworked,employee)
                                    VALUES (?,?,?,?,?,?,?);
    
                                  ''', (dep, ent, task, customer, hours, date, user))
        conn.commit()  # Connection must be committed each time a change has been made to the DB


# Checks for a matching record being submitted by the user. results are returned to TimeSheet to be communicated to user
def checkForRec(submitLst):
    count = 0
    for i in submitLst:
        dep = str(submitLst[count][0])
        ent = str(submitLst[count][1])
        task = str(submitLst[count][2])
        customer = str(submitLst[count][3])
        hours = str(submitLst[count][4])
        date = str(submitLst[count][5])
        user = str(submitLst[count][6])
        count += 1
        cursor.execute('''
                                    SELECT dep_name, legalent_name, task_name, customer, hours, dateworked, employee
                                    FROM timesheet
                                    WHERE dep_name = ? AND legalent_name = ? AND task_name = ? AND customer = ?
                                    AND dateworked = ? AND employee = ?;

                                  ''', (dep, ent, task, customer, date, user))
        result = cursor.fetchall()

    print('Matching result: ' + str(result))
    return result


# Pushed new user credentials to DB from the Add User form
def addUser(submitLst):
    count = 0
    for i in submitLst:
        name = str(submitLst[count][0])
        username = str(submitLst[count][1])
        dep = str(submitLst[count][2])
        adm = str(submitLst[count][3])
        count += 1
        cursor.execute('''
                                    INSERT INTO employee (emp_name, username,dep_id, isadmin)
                                    VALUES (?,?,?,?);
    
                                  ''', (name, username, dep, adm))
    conn.commit()


# Used to check for a user already in DB before creating a new one through the Add User Screen
def checkUser(username):
    cursor.execute('''
                                SELECT COUNT(username)
                                FROM employee
                                WHERE username = ?;

                              ''', (username,))
    result = cursor.fetchall()
    return result[0][0]


# If an Admin chooses to overwrite an existing user, the existing user will be removed before being replaced
#  with the new credentials
def removeUser(username):
    cursor.execute('''
                                DELETE FROM employee
                                WHERE username = ?;

                              ''', (username,))
    conn.commit()


#  gets all department ID's for the Add User Screen
def getDep():
    comboListDep = []

    cursor.execute('''
                            SELECT dep_name
                            FROM department
                          ''')
    result = cursor.fetchall()

    if len(result) > 0:
        for row in result:
            comboListDep += row
        return comboListDep
    else:
        return ""


# retrieves users full name to be displayed on Time Sheet
def getFullName(username):
    cursor.execute('''
                            SELECT emp_name
                            FROM employee
                            WHERE username = ?
                          ''', (username,))
    result = cursor.fetchall()
    return result[0][0]


#  retrieves all DB entries for the current time period on the TimeSheet
def getPrevEntries(startDate, endDate, username):
    cursor.execute('''
                                        SELECT dep_name, legalent_name, task_name, customer, hours, dateworked
                                        FROM timesheet
                                        WHERE employee = ? AND dateworked BETWEEN ? AND ?

                                      ''', (username, startDate,endDate))
    result = cursor.fetchall()
    return result


# Used in Update Record Form: retrieves old record from DB and updates it with the new values provided by Admin
def updateRecords(oldRec, newRec):
    cursor.execute('''
                                            UPDATE timesheet
                                            SET dep_name = ?, legalent_name = ?, task_name = ?, customer = ?, hours = ?, dateworked = ?, employee = ?
                                            WHERE dep_name = ? AND legalent_name = ? AND task_name = ? AND customer = ? AND hours = ? AND dateworked = ? AND employee = ?
                                          ''',
                   (newRec[0], newRec[1], newRec[2], newRec[3], newRec[4], newRec[5], newRec[6], oldRec[0], oldRec[1],
                    oldRec[2], oldRec[3],
                    oldRec[4], oldRec[5], oldRec[6]))
    conn.commit()


# Used in Update Record Form: Deletes selected record on Update Record Form
def deleteRecord(oldRec):
    cursor.execute('''
                                                DELETE FROM timesheet
                                                WHERE dep_name = ? AND legalent_name = ? AND task_name = ? AND customer = ? AND hours = ? AND dateworked = ? AND employee = ?
                                              ''',
                   (oldRec[0], oldRec[1], oldRec[2], oldRec[3], oldRec[4], oldRec[5], oldRec[6]))
    conn.commit()


# Checks for Stat Holidays between two given dates (Start and End of current week)
def checkForStat(startDate, endDate):
    cursor.execute('''
                                            SELECT dates
                                            FROM stats
                                            WHERE dates BETWEEN ? AND ?

                                          ''', (startDate,endDate))
    result = cursor.fetchall()
    return result


def updateRecCombo1(empName):
    comboListDep = []

    cursor.execute('''
                                SELECT dep_id
                                FROM employee
                                WHERE emp_name = ?; 
                              ''', (empName.lower()))
    result = cursor.fetchall()
    if len(result) > 0:
        for row in result:
            comboListDep += row
        return comboListDep
    else:
        return ""

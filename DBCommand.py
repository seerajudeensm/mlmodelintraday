# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:06:54 2019

@author: e3005132
"""
import mysql.connector

class DBCommand:
   
    def connectDB(self):
        
        DBName=mysql.connector.connect(
                             host="localhost",
                             user='root',
                             passwd='password',
                             database='sharedetails'
                             )
        return DBName
    
    def closeDB(self,DBNAme):
        #DBNAme.commit()
        DBNAme.close()
        
        return
 
    def selectDBDate(self,tableName,fieldsInList=[],fromDate='',toDate='',orderInList=[],selectCount=0):
        
        mydba = self.connectDB()
        
        fields = ''
        wheresquery = []
        selectedList = []
        whereFields = ''
        orderFields=''
        
        mycursor = mydba.cursor()
        for field in fieldsInList:
            fields = fields + "," + str(field)
        fields = fields[1:]
        
        if (fromDate !='') and (toDate !='') :
            whereFields = 'datetime >=%s and datetime <=%s'
            wheresquery = [fromDate,toDate]
        if (fromDate !='') and (toDate =='') :
            whereFields = 'datetime >=%s'
            wheresquery = [fromDate]
        if (fromDate =='') and (toDate !='') :
            whereFields = 'datetime <=%s'
            wheresquery = [toDate]

        for order in orderInList:
            column,ascOrDesc = order
            orderFields = orderFields + "," + str(column) + " " + str(ascOrDesc)
        orderFields = orderFields[1:]
        if(orderFields !=''):
            orderFields = " order by " + orderFields 
        try:
            if (whereFields==''):
                command = "SELECT " + fields + " FROM " + tableName + orderFields
                mycursor.execute(command)
                
            else:
                
                command = "SELECT " + fields + " FROM " + tableName + " where " + whereFields + orderFields
#                print(command,wheresquery)
                mycursor.execute(command,tuple(wheresquery))
                print(command,wheresquery)

           
            if (selectCount==0):
                output = mycursor.fetchall()
            else:
                output = mycursor.fetchmany(size=selectCount)
            for oneRow in output:
                selectedList.append(oneRow)
                
        except Exception as error:
            errorDesc = "Error:"  +  repr(error) + command + str(wheresquery)
            raise
            self.logError(tableName,errorDesc)
            
            return selectedList
        finally:
            self.closeDB(mydba)
        return selectedList



    def selectDBSQL(self,sqlstmt,wherequery='',selectCount=1):
        
        mydba = self.connectDB()
        mycursor = mydba.cursor()
        selectedList = []
        try:
            if (wherequery!=''):
                mycursor.execute(sqlstmt,tuple(wherequery))
            else:
                mycursor.execute(sqlstmt)
              
            if (selectCount==0):
                output = mycursor.fetchall()
            else:
                output = mycursor.fetchmany(size=selectCount)
            for oneRow in output:
                selectedList.append(oneRow)
                
#        except Exception as error:
#            raise "Error:"  +  repr(error) + sqlstmt + str(wherequery)
#            return selectedList
        finally:
            self.closeDB(mydba)
        return selectedList




    def selectDB(self,tableName,fieldsInList=[],wheresInList=[],orderInList=[],selectCount=1,fromDate='',toDate=''):
        
        mydba = self.connectDB()
        
        fields = ''
        wheresquery = []
        selectedList = []
        whereFields = ''
        orderFields=''
        
        mycursor = mydba.cursor()
        for field in fieldsInList:
            fields = fields + "," + str(field)
        fields = fields[1:]
        
        for where in wheresInList:
            whereField,whereValue = where
            whereFields = whereFields + " and " + str(whereField) + "=%s" 
            wheresquery.append(whereValue)
            
        if (fromDate !='') and (toDate !='') :
            whereFields = whereFields + " and " + 'datetime >=%s and datetime <=%s'
            wheresquery.append(fromDate)
            wheresquery.append(toDate)
        if (fromDate !='') and (toDate =='') :
            whereFields = whereFields + " and " + 'datetime >=%s'
            wheresquery.append(fromDate)
        if (fromDate =='') and (toDate !='') :
            whereFields = whereFields + " and " + 'datetime <=%s'
            wheresquery.append(toDate)

        whereFields = whereFields[5:]

        for order in orderInList:
            column,ascOrDesc = order
            orderFields = orderFields + "," + str(column) + " " + str(ascOrDesc)
        orderFields = orderFields[1:]
        if(orderFields !=''):
            orderFields = " order by " + orderFields 
        try:
            if (whereFields==''):
                command = "SELECT " + fields + " FROM " + tableName + orderFields
                mycursor.execute(command)
                
            else:
                command = "SELECT " + fields + " FROM " + tableName + " where " + whereFields + orderFields
                mycursor.execute(command,tuple(wheresquery))
                
            if (selectCount==0):
                output = mycursor.fetchall()
            else:
                output = mycursor.fetchmany(size=selectCount)
            for oneRow in output:
                selectedList.append(oneRow)
                
        except Exception as error:
            errorDesc = "Error:"  +  repr(error) + command + str(wheresquery)
            raise
            self.logError(tableName,errorDesc)
            
            return selectedList
        finally:
            self.closeDB(mydba)
        return selectedList
    
    def insertDB(self,mydb,tableName,values,dataLen):
        var = "%s"
        for i in range(0,dataLen):
            var = var + ",%s"
        mycursor = mydb.cursor()
        
        command = "INSERT INTO " + tableName + " VALUES(" + var + ") "
        try:
            mycursor.execute(command,values)
            mydb.commit()
        except Exception  as error:
             if(str(error.__context__).split()[0:2] == ['Duplicate', 'entry']):
                 return True
             else:
                 errorDesc = repr(error) + command + str(values)
                 #print(errorDesc)
                 self.logError(tableName,errorDesc) 
             
        return False

    def updateDB(self,mydb,tableName,fieldsInList,wheresInList):
        
        fields = ''
        wheres = ''
        inputData = []
        
        for field in fieldsInList:
            fieldName,fieldValue = field
            fields = fields + "," + fieldName + " = %s"
            inputData.append(fieldValue)
        fields = fields[1:]
        for where in wheresInList:
            whereName,whereField = where
            wheres = wheres + whereName + " = %s AND "
            inputData.append(whereField)
        
        wheres = wheres[:-5]    
#        print(wheres)
        mycursor = mydb.cursor()
        
        #command = "INSERT INTO " + stockshist + " VALUES(%s, %s, %s, %s, %s, %s,%s)"
        command = "UPDATE " + tableName + " set " + fields + " where " + wheres
        #print(command)
#        print(tableName,command,inputData)
#        print(command)
        try:
            mycursor.execute(command,tuple(inputData))
            mydb.commit()
        except Exception  as error:
             errorDesc = repr(error) + command + str(inputData)
#             print(command + str(inputData))
             self.logError(tableName,errorDesc)

        return False

    def logError(self,stockName,errorDesc):
        
        insertData = (stockName,errorDesc)
        mydblogError=self.connectDB()
        self.insertDB(mydblogError,"stockserror(stocksName,description)",insertData,1)
        self.closeDB(mydblogError)
        #raise
        return

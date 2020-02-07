
# Подключаем библиотеки
import numpy as np #штука для перобразования в массив
import json
import httplib2 
from datetime import date, datetime
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'pythonexcel-test.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# выгружаем данные из sql
import pymssql

def listmerge(lstlst):
    all=[]
    for lst in lstlst:
        for el in lst:
            all.append(el)
    return all

conn = pymssql.connect(host='SQL', user='user_name', password='password')
cur = conn.cursor()

# Делаем SELECT запрос к базе данных, используя обычный SQL-синтаксис
# вводим таблицу
cur.execute("select top 100 * from test.dbo.table")

# Получаем результат сделанного запроса
res_sql = cur.fetchall()
#получаем заголовки 
# вводим имя таблицы в конце
cur.execute("SELECT column_name FROM Reports.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'table' ")
res_sql_column = cur.fetchall()

#print(res_sql_column)

res_sql_column = listmerge(res_sql_column)

res_sql_column = np.array(res_sql_column)  
#print(res_sql_column)
res_sql = np.array(res_sql) 

# преобразовываем даты 

j = 0 
dtj = []
resi2 = []

while j < len(res_sql[0]):   
   i = 0        
   resi = res_sql[:, j] 
   if isinstance(res_sql[i, j], (datetime, date)):  
     while i < len(res_sql):      
      dtj.append(json.dumps(res_sql[i][j], indent=4, sort_keys=True, default=str).replace('"', '') )
      i += 1      
   if isinstance(res_sql[i-1,j], (datetime, date)): resi2.append(dtj)      
   else: resi2.append(res_sql[:, j].tolist())   

   j += 1 

resi2 = np.array(resi2) 
resi2 = resi2.transpose()
resi2 = resi2.tolist()

res_sql = resi2
res_sql_column = res_sql_column.tolist()

conn.close()


# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

spreadsheetId = 'spreadsheetId' #вставляем Id таблицы
sheetId = 0 


#добаление названий
batch_update_values_request_body = {
    "valueInputOption": "RAW", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    "data": [
        {"range":'Лист1!A1:Z1',
         "majorDimension":"ROWS",     # Сначала заполнять строки, затем столбцы
         "values": [res_sql_column] 
         }
    ]
}



results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = batch_update_values_request_body).execute()

#добавление самой таблицы
batch_update_values_request_body = {
    "valueInputOption": "RAW", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    "data": [
        {"range":'Лист1!A2:Z',
         "majorDimension":"ROWS",     # Сначала заполнять строки, затем столбцы
         "values": res_sql
         }
    ]
}



results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = batch_update_values_request_body).execute()



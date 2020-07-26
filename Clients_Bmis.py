import mysql.connector
import pandas as pd

def get_bmis_cat():
    pd.options.mode.chained_assignment = None
    bmi_list,no=[],[]
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
    if mydb.is_connected():
        cursorUSER = mydb.cursor()
        sql_select_query = """SELECT bmi from  patient"""
        cursorUSER.execute(sql_select_query)
        record = cursorUSER.fetchall()
        mydb.commit()
    cursorUSER.close()
    mydb.close()
    for i in range (0, len(record)):
        bmi_list.append(record[i][0])
        no.append(i)
    bmis=pd.DataFrame()
    bmis['Number']=no
    bmis['Bmi']=bmi_list
    cats = ['1', '2', '3', '4', '5', '6', '7', '8']
    bmis['bmi_categorical']=pd.cut(bmis['Bmi'],8,labels=cats)
    categories = pd.DataFrame()
    mins, maxs, counts = [], [], []
    for i in cats:
        counts.append(len(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
        if counts[int(i)-1]==0:
            for j in range(0,int(i)-1):
                b=max(bmis['Bmi'].loc[bmis['bmi_categorical'] == str(j+1)])
                bmis.loc[bmis.Bmi==b,'bmi_categorical']=str(j+2)
    counts.clear()
    for i in cats:
        mins.append(min(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
        maxs.append(max(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
        counts.append(len(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
    categories['Min'] = mins
    categories['Max'] = maxs
    categories['Count'] = counts
    nominal_categories = categories.copy()
    for i in range(0, len(nominal_categories['Count'])):
        nominal_categories['Count'][i] = round(nominal_categories['Count'][i] * 80 / len(bmi_list))
        if nominal_categories['Count'][i] == 0:
           nominal_categories['Count'][i] = 1
    return(nominal_categories)

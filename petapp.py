from PyQt5 import QtWidgets, QtPrintSupport, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import mysql.connector
import pandas as pd
import datetime
import mysql.connector
import sys
from os import path
from PyQt5.uic import loadUiType
from numpy.core import double
from Clients_Bmis import get_bmis_cat
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QLocale

#QLocale.setDefault(QLocale(QLocale.English))

# load ui file
FORM_CLASS,_= loadUiType(path.join(path.dirname('__file__'),'main.ui'))

class PetApp(QMainWindow , FORM_CLASS):
    def __init__(self,parent=None):
        super(PetApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()

    def Handle_Buttons(self):
        self.refreshButton.clicked.connect(self.get_data)
        self.searchButton.clicked.connect(self.search_patient)
        self.clearButton.clicked.connect(self.clear_fields)
        self.patientTable.cellClicked.connect(self.patient_table_cell_was_clicked)
        self.saveButton.clicked.connect(self.add_patient)
        self.saveButton.clicked.connect(self.insert_search)
        self.updateButton.clicked.connect(self.update_patient)
        self.updateButton.clicked.connect(self.insert_search)
        self.deleteButton.clicked.connect(self.delete_patient)
        self.deleteButton.clicked.connect(self.get_data)
        self.searchButton_2.clicked.connect(self.search_fill_patient_details)
        self.updateBmiButton.clicked.connect(self.update_bmi)
        self.updateBmiButton.clicked.connect(self.search_fill_patient_details)
        self.checkAvailabilityButton.clicked.connect(self.check_availability)
        self.availabilityTable.cellClicked.connect(self.availability_table_cell_was_clicked)
        self.confirmButton.clicked.connect(self.book_appointment)
        self.searchButton_3.clicked.connect(self.get_appointments)
        self.appointmentsTable.cellClicked.connect(self.appointment_table_cell_was_clicked)
        self.cancelButton.clicked.connect(self.cancel_appointment)
        self.cancelButton.clicked.connect(self.get_appointments)
        self.calculateButton.clicked.connect(self.calculate_tomorrow_dose)
        self.plotButton.clicked.connect(self.show_graph_1)
        self.plotButton.clicked.connect(self.show_graph_2)
        self.statsButton.clicked.connect(self.show_stats_1)
        self.statsButton.clicked.connect(self.show_stats_2)
        self.printButton.clicked.connect(self.handlePrint)
        self.previewButton.clicked.connect(self.handlePreview)

    def patient_table_cell_was_clicked(self , row_number):
        try:
            patient_id = self.patientTable.item(row_number, 0).text()
            lastname = self.patientTable.item(row_number ,1).text()
            name = self.patientTable.item(row_number ,2).text()
            amka = self.patientTable.item(row_number ,3).text()
            sex = self.patientTable.item(row_number, 4).text()
            if sex=='male':
                self.maleRadioButton.setChecked(True)
            if sex == 'female':
                self.femaleRadioButton.setChecked(True)

            datebirth = self.patientTable.item(row_number, 5).text()
            weight = self.patientTable.item(row_number, 6).text()
            height = self.patientTable.item(row_number, 7).text()
            bmi = self.patientTable.item(row_number, 8).text()
            address =   self.patientTable.item(row_number, 9).text()
            phone =   self.patientTable.item(row_number, 10).text()
            email  = self.patientTable.item(row_number, 11).text()
        except AttributeError:
            pass

        try:
            self.patientIdEdit.setText(str(patient_id))
            self.surnameEdit.setText(str(lastname))
            self.nameEdit.setText(str(name))
            self.ssnEdit_2.setText(str(amka))
            format_str = '%d/%m/%Y'
            datetime_obj = datetime.datetime.strptime(datebirth, format_str)
            self.bdateEdit.setDate(datetime_obj)
            self.weightSpinBox.setValue(double(weight))
            self.heightSpinBox.setValue(double(height))
            self.adressEdit.setText(str(address))
            self.phoneEdit.setText(str(phone))
            self.emailEdit.setText(str(email))
            self.ssnEdit_3.setText(str(amka))
        except UnboundLocalError:
            pass

    def search_patient(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        famka = str(self.ssnEdit.text())
        amka = "'" + famka + "'"
        mycursorActive = mydb.cursor()
        amka_search_active = "SELECT active  FROM patient where  amka=" + amka
        mycursorActive.execute(amka_search_active)
        resultActive = mycursorActive.fetchall()
        resultActive.append((-1,))
        if (resultActive[0][0] == 1):
            mycursor = mydb.cursor()
            amka_search = "SELECT pat_id, lastname, firstname, amka, sex, DATE_FORMAT(birthdate,'%d/%m/%Y'),weight , height, bmi, address,phone_number, email  FROM patient where  active=1 and  amka=" + amka
            mycursor.execute(amka_search)
            result = mycursor.fetchall()
            self.patientTable.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.patientTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.patientTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if (resultActive[0][0] == 0):
            qm = QMessageBox()
            qm.setWindowTitle("Inactive Patient")
            ret = qm.question(self, '', "The patient registry is inactive. Do you want to to recover it?", qm.Yes | qm.No)
            if ret == qm.Yes:
                mycursorActivate = mydb.cursor()
                sql_active = "UPDATE patient SET active = 1 WHERE amka = " + amka
                # val = (famka)
                mycursorActivate.execute(sql_active)
                mydb.commit()
                mycursor = mydb.cursor()
                amka_search = "SELECT pat_id, lastname, firstname, amka, sex, DATE_FORMAT(birthdate,'%d/%m/%Y'),weight , height, bmi, address,phone_number, email  FROM patient where  active=1 and  amka=" + amka
                mycursor.execute(amka_search)
                result = mycursor.fetchall()
                self.patientTable.setRowCount(0)
                for row_number, row_data in enumerate(result):
                    self.patientTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.patientTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if (resultActive[0][0] == -1):
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("No patient with this SSN")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def get_data(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        mycursor = mydb.cursor()
        amka_search = "SELECT  pat_id , lastname,firstname, amka, sex,  DATE_FORMAT(birthdate,'%d/%m/%Y'), weight , height, bmi ,address , phone_number, email FROM patient where  active=1 "

        mycursor.execute(amka_search)
        result = mycursor.fetchall()
        self.patientTable.setRowCount(0)

        for row_number , row_data in enumerate(result):
            self.patientTable.insertRow(row_number)
            for column_number , data in enumerate(row_data):
                self.patientTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def clear_fields(self):
        self.surnameEdit.setText(str(""))
        self.nameEdit.setText(str(""))
        self.ssnEdit_2.setText(str(""))
        self.ssnEdit.setText(str(""))

        self.maleRadioButton.setChecked(False)
        self.femaleRadioButton.setChecked(False)

        bdate = '01/01/2000'
        format_str = '%d/%m/%Y'
        datetime_obj = datetime.datetime.strptime(bdate, format_str)

        weightd = '0.0'
        heightd = '0.0'

        self.bdateEdit.setDate(datetime_obj)
        self.weightSpinBox.setValue(double(weightd))
        self.heightSpinBox.setValue(double(heightd))
        self.adressEdit.setText(str(""))
        self.phoneEdit.setText(str(""))
        self.emailEdit.setText(str(""))
        self.patientIdEdit.setText(str(""))

    def insert_search(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        mycursor = mydb.cursor()
        famka = str(self.ssnEdit_2.text())
        famka = famka.replace('"', '')
        famka = famka.replace("'", '')
        amka = "'" + famka + "'"
        if (famka != ''):
            amka_search = "SELECT pat_id, lastname, firstname, amka, sex, DATE_FORMAT(birthdate,'%d/%m/%Y'), weight, height,bmi, address, phone_number, email FROM patient where active=1 and amka=" + amka
            mycursor.execute(amka_search)
            result = mycursor.fetchall()
            self.patientTable.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.patientTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.patientTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            try:
                if (famka != ''):
                    patient_id = self.patientTable.item(row_number, 0).text()
                    self.patientIdEdit.setText(str(patient_id))
                else:
                    self.patientIdEdit.setText('')
            except IndexError:
                pass

    def add_patient(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        mycursor = mydb.cursor()
        firstname = self.nameEdit.text()
        lastname = self.surnameEdit.text()
        amka = self.ssnEdit_2.text()
        weight = self.weightSpinBox.text()
        height = self.heightSpinBox.text()
        bmi = round(float(weight) / (float(height) * float(height)), 2)
        bdate = self.bdateEdit.text()
        days = bdate.split('/')[0]
        months = bdate.split('/')[1]
        years = bdate.split('/')[2]
        format_str = '%Y-%m-%d'
        stringdate = years + '-' + months + '-' + days

        if self.maleRadioButton.isChecked() == True:
            gender = 'male'
        if self.femaleRadioButton.isChecked() == True:
            gender = 'female'
        address = self.adressEdit.text()
        phone = self.phoneEdit.text()
        email = self.emailEdit.text()
        active = 1
        if (amka != ''):
            try:
                if (self.patientIdEdit.text() == ''):
                    sql = "insert into patient (firstname, lastname, amka, weight, height, birthdate, sex, bmi, address, phone_number, " \
                          "email, active) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    val = (
                    firstname, lastname, amka, weight, height, stringdate, gender, bmi, address, phone, email, active)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    ##############################################################################new
                    sql2 = "INSERT INTO stats (pat_id,deleted_app,rejected_app,app_count,last_app) SELECT pat_id , 0 , 0 , 0 , '0000-01-01' FROM patient WHERE amka ='" + amka + "'"
                    mycursor.execute(sql2)
                    mydb.commit()
                    ###############################################################################new
                    msg = QMessageBox()
                    msg.setWindowTitle("Add patient")
                    msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                    msg.setText("Patient successfully inserted to database!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
            except mysql.connector.errors.IntegrityError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                msg.setText("Wrong ssn")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
            except UnboundLocalError:
                msg = QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                msg.setText("You have to pick a sex")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()

    def update_patient(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        mycursor = mydb.cursor()

        firstname = self.nameEdit.text()
        lastname = self.surnameEdit.text()
        amka = self.ssnEdit_2.text()
        amka = amka.replace('"', '')
        amka = amka.replace("'", '')
        weight = self.weightSpinBox.text()
        height = self.heightSpinBox.text()
        bmi = round(float(weight) / (float(height) * float(height)), 2)

        bdate = self.bdateEdit.text()
        days = bdate.split('/')[0]
        months = bdate.split('/')[1]
        years = bdate.split('/')[2]
        format_str = '%Y-%m-%d'
        stringdate = years + '-' + months + '-' + days

        if self.maleRadioButton.isChecked() == True:
            gender='male'
        if self.femaleRadioButton.isChecked() == True:
            gender = 'female'

        address = self.adressEdit.text()
        phone = self.phoneEdit.text()
        email = self.emailEdit.text()
        pat_id = self.patientIdEdit.text()

        try:
            if (self.patientIdEdit.text() != ''):
                sql = "update patient set firstname = %s , lastname = %s , amka = %s , weight = %s, height = %s, " \
                    "birthdate = %s, sex = %s , bmi = %s , address = %s , phone_number = %s, email = %s where pat_id =" + pat_id
                val = (firstname,lastname,amka,weight,height,stringdate,gender,bmi,address,phone,email)
                mycursor.execute(sql, val)
                mydb.commit()
                msg = QMessageBox()
                msg.setWindowTitle("Update patient")
                msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                msg.setText("Patient successfully updated!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
        except mysql.connector.errors.IntegrityError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("Cannot update patient without ssn")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        except UnboundLocalError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("Cannot update patient without sex")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def delete_patient(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        mycursor = mydb.cursor()
        pat_id = self.patientIdEdit.text()

        qm = QMessageBox()
        qm.setWindowTitle("Delete patient")
        ret = qm.question(self, '', "Are you sure you want to delete this patient?", qm.Yes | qm.No)
        if ret == qm.Yes:
            if (self.patientIdEdit.text() != ''):
                sql = "update patient set active=0 where pat_id =" + pat_id
                mycursor.execute(sql)
                mydb.commit()
                msg = QMessageBox()
                msg.setWindowTitle("Successful delete")
                msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                msg.setText("Patient successfully deleted!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()

        self.surnameEdit.setText(str(""))
        self.nameEdit.setText(str(""))
        self.ssnEdit_2.setText(str(""))
        self.ssnEdit.setText(str(""))
        self.maleRadioButton.setChecked(False)
        self.femaleRadioButton.setChecked(False)

        bdate = '01/01/2000'
        format_str = '%d/%m/%Y'
        datetime_obj = datetime.datetime.strptime(bdate, format_str)

        weightd = '0.0'
        heightd = '0.0'

        self.bdateEdit.setDate(datetime_obj)
        self.weightSpinBox.setValue(double(weightd))
        self.heightSpinBox.setValue(double(heightd))
        self.adressEdit.setText(str(""))
        self.phoneEdit.setText(str(""))
        self.emailEdit.setText(str(""))
        self.patientIdEdit.setText(str(""))

    def search_fill_patient_details(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        cursor = mydb.cursor()
        famka = str(self.ssnEdit_3.text())
        amka = "'" + famka + "'"
        sql = "SELECT lastname, firstname, amka, bmi, height, pat_id, weight from patient where active=1 and amka=" + amka
        cursor.execute(sql)
        for row in cursor.fetchall():
            self.surnameEdit_2.setText(row[0])
            self.nameEdit_2.setText(row[1])
            self.ssnEdit_4.setText(row[2])
            self.bmiSpinBox.setValue(row[3])
            self.heightSpinBox_2.setValue(row[4])
            self.patientIdEdit_2.setText(str(row[5]))
            self.weightSpinBox_2.setValue(row[6])

        self.availabilityTable.setRowCount(0)

    def update_bmi(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        cursor = mydb.cursor()
        famka = str(self.ssnEdit_3.text())
        # amka = "'" + famka + "'"
        weight = self.weightSpinBox_2.text()
        height = self.heightSpinBox_2.text()
        bmi = round(float(weight) / (float(height) * float(height)), 2)

        try:
            sql = "update patient set weight= %s , bmi = %s where amka= %s"
            val = (weight, bmi, famka)
            cursor.execute(sql, val)
            mydb.commit()
            msg = QMessageBox()
            msg.setWindowTitle("Update BMI")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("BMI successfully updated!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
        except mysql.connector.errors.IntegrityError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("Cannot update patient without ssn")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
        except UnboundLocalError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("Cannot update patient without sex")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def check_availability(self):
        tday=datetime.datetime.today()
        end_date = tday + datetime.timedelta(days=14)
        start_date = tday + datetime.timedelta(days=1)
        cnt = 0

        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
        if mydb.is_connected():
            cursorUSER = mydb.cursor()
            sql_select_query = """SELECT a.app_date, a.app_time, p.bmi from appointment as a, patient as p 
            where app_date between %s and %s and a.pat_id=p.pat_id order by a.app_date, a.app_time"""
            data = (start_date.date(), end_date.date(),)
            cursorUSER.execute(sql_select_query, data)
            record = cursorUSER.fetchall()
            mydb.commit()
        cursorUSER.close()
        mydb.close()
        bmi, dttime = [], []
        for row in record:
            bmi.append(row[2])
            dttime.append(datetime.datetime.combine(row[0], (datetime.datetime.min + row[1]).time()))
        appointments = pd.DataFrame()
        appointments['Datetime'] = dttime
        appointments['BMI'] = bmi
        possible_hours = list(range(9, 17))
        possible_appointments_hours, possible_appointments_dates, possible_appointments, tomorrow = [], [], [], []
        for i in range(0, 14):
            if (start_date.date() + datetime.timedelta(days=i)).weekday() == 6 or (
                    start_date.date() + datetime.timedelta(days=i)).weekday() == 5:
                continue
            if datetime.date(tday.year, 1, 1) <= (start_date.date() + datetime.timedelta(days=i)) <= datetime.date(
                    tday.year, 1, 7):
                continue
            if datetime.date(tday.year + 1, 1, 1) <= (start_date.date() + datetime.timedelta(days=i)) <= datetime.date(
                    tday.year + 1, 1, 7):
                continue
            if datetime.date(tday.year, 4, 15) <= (start_date.date() + datetime.timedelta(days=i)) <= datetime.date(
                    tday.year, 4, 21):
                continue
            if datetime.date(tday.year, 8, 8) <= (start_date.date() + datetime.timedelta(days=i)) <= datetime.date(
                    tday.year, 8, 15):
                continue
            if datetime.date(tday.year, 12, 18) <= (start_date.date() + datetime.timedelta(days=i)) <= datetime.date(
                    tday.year, 12, 24):
                continue
            else:
                possible_appointments_dates.append(start_date.date() + datetime.timedelta(days=i))
        for i in possible_hours:
            possible_appointments_hours.append(datetime.time(i, 00, 00))

        for j in possible_appointments_dates:
            for i in possible_appointments_hours:
                pos_app = datetime.datetime.combine(j, i)
                possible_appointments.append(pos_app)
        for i in appointments['Datetime']:
            if i == (tday.date() + datetime.timedelta(days=1)):
                tomorrow.append(i)
        for i in dttime:
            possible_appointments.remove(i)
        bmis_categories = get_bmis_cat()
        bmis_categories['Appointed'] = list(0 for i in range(0, len(bmis_categories['Count'])))
        for i in appointments['BMI']:
            for j in range(0, len(bmis_categories)):
                if i >= bmis_categories['Min'][j] and i <= bmis_categories['Max'][j]:
                    app_category = j
                    break
            bmis_categories['Appointed'][app_category] += 1
        for i in range(0, len(bmis_categories)):
            if float(self.bmiSpinBox.text()) >= bmis_categories['Min'][i] and float(self.bmiSpinBox.text()) <= bmis_categories['Max'][i]:
                catgory_now = i
                break
        try:
            if len(tomorrow) < 8 and tday.hour >= 13:
                mylist = possible_appointments
        except UnboundLocalError:
            pass

        try:
            if bmis_categories['Appointed'][catgory_now] >= bmis_categories['Count'][catgory_now]:
                msg = QMessageBox()
                msg.setWindowTitle("No availability")
                msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                msg.setText("No available appointments for the selected days!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
                mylist = list()
                cnt = 1

                mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
                if mydb.is_connected():
                    pat_id = self.patientIdEdit_2.text()
                    cursorUSER = mydb.cursor()
                    stmt = """UPDATE `stats` SET `rejected_app`=`rejected_app`+1 WHERE pat_id =""" + pat_id
                    cursorUSER.execute(stmt)
                    mydb.commit()
                    cursorUSER.close()
                mydb.close()
            else:
                mylist = possible_appointments
        except UnboundLocalError:
            pass

        list2 = []
        try:
            for i in mylist:
                list2.append(str(i))
        except UnboundLocalError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("You must choose a patient first!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

        try:
            mydb2 = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
            mycursor2 = mydb2.cursor()
            app_pat_id = self.patientIdEdit_2.text()
                # val = (app_pat_id)
            max_pat_date = "SELECT DATE_FORMAT(max(app_date),'%Y-%m-%d') FROM appointment WHERE pat_id=" + app_pat_id
            mycursor2.execute(max_pat_date)

            myresult = mycursor2.fetchall()
            maxdate = []
            for x in myresult:
                maxdate.append(x[0])

                # print(maxdate[0])
            if (maxdate[0] != None):
                maxdapp = datetime.datetime.strptime(str(maxdate[0]), '%Y-%m-%d')
            else:
                maxdapp = datetime.datetime.strptime('1000-01-01', '%Y-%m-%d')

            print(maxdapp)
        except mysql.connector.errors.ProgrammingError:
            pass

        list3 = []
        for k in list2:
            if(datetime.datetime.strptime(k.split(' ')[0], '%Y-%m-%d')>maxdapp):
                list3.append(list((k.split(' ')[0], k.split(' ')[1])))
                print(datetime.datetime.strptime(k.split(' ')[0], '%Y-%m-%d'))

        self.availabilityTable.setRowCount(0)

        for row_number, row_data in enumerate(list3):
            self.availabilityTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.availabilityTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        if not  list3:
            if cnt == 0:
                msg = QMessageBox()
                msg.setWindowTitle("No availability")
                msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                msg.setText("No available appointments for the selected days!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()

                try:
                    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
                    if mydb.is_connected():
                        pat_id = self.patientIdEdit_2.text()
                        cursorUSER = mydb.cursor()
                        stmt = """UPDATE `stats` SET `rejected_app`=`rejected_app`+1 WHERE pat_id ="""+pat_id
                        cursorUSER.execute(stmt)
                        mydb.commit()
                        cursorUSER.close()
                    mydb.close()
                except mysql.connector.errors.ProgrammingError:
                    pass

    def availability_table_cell_was_clicked(self, row_number):
        try:
            app_date = self.availabilityTable.item(row_number, 0).text()
            app_time = self.availabilityTable.item(row_number ,1).text()
        except AttributeError:
            pass

        try:
            self.dateEdit.setText(str(app_date))
            self.timeEdit.setText(str(app_time))
        except UnboundLocalError:
            pass

    def book_appointment(self):

        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")

        pat_id = self.patientIdEdit_2.text()
        app_bmi = self.bmiSpinBox.text()
        app_date = self.dateEdit.text()
        app_time = self.timeEdit.text()
        dose = (0.0091 * float((app_bmi)) ** 3) - (0.7925 * float((app_bmi)) ** 2) + 25.89 * float((app_bmi)) - 79.442

        try:
            if mydb.is_connected():
                cursorUSER = mydb.cursor()
                stmt = ("INSERT INTO appointment (pat_id, dose, app_date, app_time)"
                        " VALUES (%s, %s, %s, %s)")
                data = (pat_id, dose, app_date, app_time)
                cursorUSER.execute(stmt, data)
                mydb.commit()
                msg = QMessageBox()
                msg.setWindowTitle("New appointment")
                msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                msg.setText("New appointment successfully booked!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.availabilityTable.setRowCount(0)
                self.dateEdit.setText(str(""))
                self.timeEdit.setText(str(""))
                stmt = (
                    "UPDATE `stats` SET `last_app`=%s, `rejected_app`=0,`app_count`= `app_count`+1 WHERE `pat_id`=%s")
                data = (app_date, pat_id)
                cursorUSER.execute(stmt, data)
                mydb.commit()
            cursorUSER.close()
            mydb.close()
        except mysql.connector.errors.IntegrityError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("You must choose a patient first!")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def get_appointments(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        mycursor = mydb.cursor()
        date_from = str(self.dateEdit_2.text())
        date_to = str(self.dateEdit_3.text())
        ssn = str(self.ssnEdit_5.text())
        date_from2 = date_from.split('/')[2] + '-' + date_from.split('/')[1] + '-' + date_from.split('/')[0]
        date_to2 = date_to.split('/')[2] + '-' + date_to.split('/')[1] + '-' + date_to.split('/')[0]
        if (ssn == ''):
            val = (date_from2, date_to2)
            amka_search = "select a.app_id ,p.firstname , p.lastname , p.amka, a.dose , DATE_FORMAT(a.app_date ,'%d/%m/%Y'), " \
                          "a.app_time from appointment a , patient p where a.pat_id = p.pat_id and (app_date between %s and %s) " \
                          "order by a.app_date, a.app_time"  #
        if (ssn != ''):
            val = (date_from2, date_to2, ssn)
            amka_search = "select a.app_id ,p.firstname , p.lastname , p.amka, a.dose , DATE_FORMAT(a.app_date ,'%d/%m/%Y'), " \
                          "a.app_time from appointment a , patient p where a.pat_id = p.pat_id and (app_date between %s and %s) and p.amka=%s " \
                          "order by a.app_date, a.app_time"  #
        mycursor.execute(amka_search, val)
        result = mycursor.fetchall()
        self.appointmentsTable.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.appointmentsTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.appointmentsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def appointment_table_cell_was_clicked(self , row_number):
        try:
            app_id = self.appointmentsTable.item(row_number, 0).text()
        except AttributeError:
            pass

        try:
            self.appIdEdit.setText(str(app_id))
        except UnboundLocalError:
            pass

    def cancel_appointment(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="petctdb"
        )
        mycursor = mydb.cursor()

        app_id = self.appIdEdit.text()

        try:
            qm = QMessageBox()
            qm.setWindowTitle("Cancel appointment")
            ret = qm.question(self, '', "Are you sure you want to cancel this appointment?", qm.Yes | qm.No)
            if ret == qm.Yes:
                if mydb.is_connected():
                    sql2 = "update stats set deleted_app = deleted_app + 1 where pat_id = (select pat_id from appointment where app_id= " + app_id + ")"
                    mycursor.execute(sql2)
                    sql3 = "INSERT INTO cancelled_appointment select app_id , pat_id, dose , app_date , app_time , sysdate() from appointment where app_id = " + app_id + " "
                    mycursor.execute(sql3)
                    sql = "delete from appointment where app_id =" + app_id
                    mycursor.execute(sql)
                    mydb.commit()
                    msg = QMessageBox()
                    msg.setWindowTitle("Successful cancelation")
                    msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
                    msg.setText("Appointment canceled!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
        except mysql.connector.errors.ProgrammingError:
            msg = QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setWindowIcon(QIcon("icons8-system-task-40.png"))
            msg.setText("You must pick an appointment first")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def show_graph_1(self):
        report_year = datetime.datetime.today().year
        pd.options.mode.chained_assignment = None
        bmi_list, no = [], []
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
        if mydb.is_connected():
            cursorUSER = mydb.cursor()
            sql_select_query = """SELECT distinct a.pat_id, p.bmi from patient as p, appointment as a 
                where a.pat_id=p.pat_id and a.app_date BETWEEN %s and %s   """
            data = (str(report_year - 1) + '-01-01 00:00:00', str(report_year) + '-01-01 00:00:00',)
            cursorUSER.execute(sql_select_query, data)
            record = cursorUSER.fetchall()
            mydb.commit()
        cursorUSER.close()
        mydb.close()
        for row in record:
            bmi_list.append(row[1])
        bmis = pd.DataFrame()
        bmis['Number'] = no
        bmis['Bmi'] = bmi_list
        cats = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        bmis['bmi_categorical'] = pd.cut(bmis['Bmi'], 10, labels=cats)
        categories = pd.DataFrame()
        mins, maxs, counts = [], [], []
        for i in cats:
            counts.append(len(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
            if counts[int(i) - 1] == 0:
                for j in range(0, int(i) - 1):
                    b = max(bmis['Bmi'].loc[bmis['bmi_categorical'] == str(j + 1)])
                    bmis.loc[bmis.Bmi == b, 'bmi_categorical'] = str(j + 2)
        counts.clear()
        for i in cats:
            mins.append(min(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
            maxs.append(max(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
            counts.append(len(bmis['Bmi'].loc[bmis['bmi_categorical'] == i]))
        categories['Min'] = mins
        categories['Max'] = maxs
        categories['Count'] = counts
        ylist = []
        for i in range(0, len(categories)):
            b = str(categories['Min'][i]) + '-' + str(categories['Max'][i])
            ylist.append(b)

        fig=plt.figure(figsize=(6, 3))
        plt.bar(ylist, categories['Count'], color='r')
        plt.title("BMI Distribution for year " + str(report_year - 1), fontsize=12)
        plt.ylabel('Client Number', fontsize=10)
        plt.xticks(rotation=20, fontsize=6)
        x = (sum(bmi_list) / len(bmi_list))
        x = (x - min(bmi_list)) / (max(bmi_list) - min(bmi_list)) * (10 - 1) + 1
        plt.axvline(x=x, color='k', linestyle='--')
        self.plotWidget = FigureCanvas(fig)
        lay = QtWidgets.QVBoxLayout(self.content_plot_1)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.plotWidget)

    def show_graph_2(self):
        current_time = datetime.datetime.today()
        doses_before, doses_after, dates_before, dates_after = [], [], [], []
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
        if mydb.is_connected():
            cursorUSER = mydb.cursor()
            sql_select_query = """SELECT dose, app_date from  appointment where app_date between %s and %s"""
            data = ('2019-01-01 00:00:00', '2019-12-31 23:59:59',)
            cursorUSER.execute(sql_select_query, data)
            record = cursorUSER.fetchall()
            mydb.commit()
        cursorUSER.close()
        mydb.close()
        for row in record:
            doses_before.append(row[0])
            dates_before.append(row[1])
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
        if mydb.is_connected():
            cursorUSER = mydb.cursor()
            sql_select_query = """SELECT dose, app_date from  appointment where app_date between %s and %s"""
            data = (str(current_time.year) + '-01-01 00:00:00', str(current_time.year) + '-12-31 23:59:59',)
            cursorUSER.execute(sql_select_query, data)
            record = cursorUSER.fetchall()
            mydb.commit()
        cursorUSER.close()
        mydb.close()
        for row in record:
            doses_after.append(row[0])
            dates_after.append(row[1])

        old_data = pd.DataFrame()
        old_data['Dates'] = dates_before
        old_data['Doses'] = doses_before
        new_data = pd.DataFrame()
        new_data['Dates'] = dates_after
        new_data['Doses'] = doses_after

        old_data_by_day = old_data.groupby(['Dates'], as_index=False)['Doses'].sum()
        new_data_by_day = new_data.groupby(['Dates'], as_index=False)['Doses'].sum()

        old_data_by_week = old_data.copy()
        for i in range(0, len(old_data)):
            old_data_by_week['Dates'].iloc[i] = old_data_by_week['Dates'].iloc[i].isocalendar()[1]
        old_data_by_week = old_data_by_week.groupby(['Dates'], as_index=False)['Doses'].sum()
        old_data_by_week.columns = ['Weeks', 'Doses']

        old_data_by_month = old_data.copy()
        for i in range(0, len(old_data)):
            old_data_by_month['Dates'].iloc[i] = old_data_by_month['Dates'].iloc[i].month
        old_data_by_month = old_data_by_month.groupby(['Dates'], as_index=False)['Doses'].sum()
        old_data_by_month.columns = ['Month', 'Doses']

        new_data_by_week = new_data.copy()
        for i in range(0, len(new_data)):
            new_data_by_week['Dates'].iloc[i] = new_data_by_week['Dates'].iloc[i].isocalendar()[1]
        new_data_by_week = new_data_by_week.groupby(['Dates'], as_index=False)['Doses'].sum()
        new_data_by_week.columns = ['Weeks', 'Doses']

        new_data_by_month = new_data.copy()
        for i in range(0, len(new_data)):
            new_data_by_month['Dates'].iloc[i] = new_data_by_month['Dates'].iloc[i].month
        new_data_by_month = new_data_by_month.groupby(['Dates'], as_index=False)['Doses'].sum()
        new_data_by_month.columns = ['Month', 'Doses']

        old_data_by_day_total = old_data_by_day.copy()
        for i in range(1, len(old_data_by_day_total)):
            old_data_by_day_total['Doses'][i] += old_data_by_day_total['Doses'][i - 1]

        new_data_by_day_total = new_data_by_day.copy()
        for i in range(1, len(new_data_by_day_total)):
            new_data_by_day_total['Doses'][i] += new_data_by_day_total['Doses'][i - 1]

        old_data_by_week_total = old_data_by_week.copy()
        for i in range(1, len(old_data_by_week_total)):
            old_data_by_week_total['Doses'][i] += old_data_by_week_total['Doses'][i - 1]

        new_data_by_week_total = new_data_by_week.copy()
        for i in range(1, len(new_data_by_week_total)):
            new_data_by_week_total['Doses'][i] += new_data_by_week_total['Doses'][i - 1]

        old_data_by_month_total = old_data_by_month.copy()
        for i in range(1, len(old_data_by_month_total)):
            old_data_by_month_total['Doses'][i] += old_data_by_month_total['Doses'][i - 1]

        new_data_by_month_total = new_data_by_month.copy()
        for i in range(1, len(new_data_by_month_total)):
            new_data_by_month_total['Doses'][i] += new_data_by_month_total['Doses'][i - 1]

        surplus_dose_by_day = old_data_by_day.copy()
        for i in range(0, len(surplus_dose_by_day)):
            surplus_dose_by_day['Doses'][i] = 2400 - surplus_dose_by_day['Doses'][i]
        surplus_dose_by_day.columns = ['Dates', 'Surplus Doses']

        surplus_dose_by_week = surplus_dose_by_day.copy()
        for i in range(0, len(surplus_dose_by_day)):
            surplus_dose_by_week['Dates'].iloc[i] = surplus_dose_by_week['Dates'].iloc[i].isocalendar()[1]
        surplus_dose_by_week = surplus_dose_by_week.groupby(['Dates'], as_index=False)['Surplus Doses'].sum()
        surplus_dose_by_week.columns = ['Weeks', 'Surplus Doses']

        surplus_dose_by_month = surplus_dose_by_day.copy()
        for i in range(0, len(surplus_dose_by_day)):
            surplus_dose_by_month['Dates'].iloc[i] = surplus_dose_by_month['Dates'].iloc[i].month
        surplus_dose_by_month = surplus_dose_by_month.groupby(['Dates'], as_index=False)['Surplus Doses'].sum()
        surplus_dose_by_month.columns = ['Month', 'Surplus Doses']

        surplus_dose_by_day_total = surplus_dose_by_day.copy()
        for i in range(1, len(surplus_dose_by_day_total)):
            surplus_dose_by_day_total['Surplus Doses'][i] += surplus_dose_by_day_total['Surplus Doses'][i - 1]

        surplus_dose_by_week_total = surplus_dose_by_week.copy()
        for i in range(1, len(surplus_dose_by_week_total)):
            surplus_dose_by_week_total['Surplus Doses'][i] += surplus_dose_by_week_total['Surplus Doses'][i - 1]

        surplus_dose_by_month_total = surplus_dose_by_month.copy()
        for i in range(1, len(surplus_dose_by_month_total)):
            surplus_dose_by_month_total['Surplus Doses'][i] += surplus_dose_by_month_total['Surplus Doses'][i - 1]

        old_system_daily_sum = []
        for i in range(1, len(new_data_by_day_total) + 1):
            old_system_daily_sum.append(i * 2400)

        fig = plt.figure(figsize=(6, 3))
        plt.plot(new_data_by_day_total['Dates'], old_system_daily_sum, new_data_by_day_total['Dates'],
                 new_data_by_day_total['Doses'])
        plt.title("Comparison of new order system vs (Q,r) model ", fontsize=12)
        plt.ylabel('Total doses', fontsize=10)
        plt.xticks(rotation=20, fontsize=6)
        plt.yticks(fontsize=6)
        plt.legend('upper left')
        self.plotWidget = FigureCanvas(fig)
        lay = QtWidgets.QVBoxLayout(self.content_plot_2)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.plotWidget)

    def calculate_tomorrow_dose(self):
        ftomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        tomorrow = "'" + ftomorrow + "'"
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
        if mydb.is_connected():
            cursor = mydb.cursor()
            sql = """SELECT sum(dose) from appointment where app_date="""+tomorrow
            cursor.execute(sql)
            for row in cursor.fetchall():
                self.lcdNumber.display(row[0])

    def show_stats_1(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
        if mydb.is_connected():
            cursorUSER = mydb.cursor()
            sql = """select round(sum(dose),2) as 'Total yearly dose', round(avg(dose),2) as 'Average dose per patient', round(avg(dose),2)*8 as 'Average daily dose', 
                (round(avg(dose),2)*8)*5 as 'Average weekly dose', 
                count(app_id) as 'Total Appointments', round(AVG(bmi),2) as 'Average BMI', year(app_date) as 'Year' 
                from appointment a, patient p 
                where a.pat_id = p.pat_id
                group by year(app_date)
                order by year(app_date) desc"""
            cursorUSER.execute(sql)
            record = cursorUSER.fetchall()

        self.statsTable_1.setRowCount(0)

        for row_number, row_data in enumerate(record):
            self.statsTable_1.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.statsTable_1.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def show_stats_2(self):
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="petctdb")
        if mydb.is_connected():
            cursorUSER = mydb.cursor()
            sql = """select (2400-round(avg(dose),2)*8) as 'Aboslute daily difference', (12000-(round(avg(dose),2)*8)*5) as 'Aboslute weekly difference', 
                    (576000-round(sum(dose),2)) as 'Aboslute yearly difference', round((((2400-round(avg(dose),2)*8)/2400)*100),2) as 'Percentage difference', 
                    year(app_date) as 'Year'  from appointment a, patient p
                    where a.pat_id = p.pat_id
                    group by year(app_date)
                    order by year(app_date) desc"""
            cursorUSER.execute(sql)
            record = cursorUSER.fetchall()

        self.statsTable_2.setRowCount(0)

        for row_number, row_data in enumerate(record):
            self.statsTable_2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.statsTable_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def handlePrint(self):
        dialog = QtPrintSupport.QPrintDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.handlePaintRequest(dialog.printer())

    def handlePreview(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    def handlePaintRequest(self, printer):
        document = QtGui.QTextDocument()
        cursor = QtGui.QTextCursor(document)
        table = cursor.insertTable(
            self.appointmentsTable.rowCount(), self.appointmentsTable.columnCount())
        for row in range(table.rows()):
            for col in range(table.columns()):
                cursor.insertText(self.appointmentsTable.item(row, col).text())
                cursor.movePosition(QtGui.QTextCursor.NextCell)
        document.print_(printer)

# ======================================================================================================================
def main():

    app = QApplication(sys.argv)
    window = PetApp()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()


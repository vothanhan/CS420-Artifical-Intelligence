import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pdb
import algorithm
city_list=[]
heuristic={}
cities_distance={}
path=None
elapsed=None
elapsed1=None
#For fast testing, disable map drawing in algorithm.py
class warning(QMessageBox):		#Show up if there is no path from start to goal
    def __init__(self,parent=None):
        super(warning,self).__init__(parent)

        self.setIcon(QMessageBox.Warning)
        self.setText("No path!")
        self.setWindowTitle("Warning")

class warning1(QMessageBox):	#Show up if one city do not have connection with any other city
    def __init__(self,parent=None):
        super(warning1,self).__init__(parent)

        self.setIcon(QMessageBox.Warning)
        self.setText("Every city must have at least one connection!")
        self.setWindowTitle("Warning")

class warning2(QMessageBox):	#Show up if not choose algorithm yet
    def __init__(self,parent=None):
        super(warning2,self).__init__(parent)

        self.setIcon(QMessageBox.Warning)
        self.setText("Please choose your algorithm first!")
        self.setWindowTitle("Warning")

class warning3(QMessageBox):	#Show up if goal or start city have not been selected yet
    def __init__(self,parent=None):
        super(warning3,self).__init__(parent)

        self.setIcon(QMessageBox.Warning)
        self.setText("Please choose start/goal city !")
        self.setWindowTitle("Warning")

class warning4(QMessageBox):	#Show up if at least one city have not had its heuristic declared, only appear in A* or Greedy BFS
    def __init__(self,parent=None):
        super(warning4,self).__init__(parent)

        self.setIcon(QMessageBox.Warning)
        self.setText("Heuristic is not fully declared")
        self.setWindowTitle("Warning")

class MyDialog(QDialog):	#New Windows to show connection and cost of cities
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(self.reject)
        self.textBrowser = QTextBrowser(self)
        for c in cities_distance:
            c1,c2=c
            key=""
            key+=c1
            key+=" - "
            key+=c2
            key+=": "
            key+=str(cities_distance[c])
            self.textBrowser.append(key)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)

class ShowH(QDialog):	#New window to show heuristic
    def __init__(self, parent=None):
        super(ShowH, self).__init__(parent)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(self.reject)
        self.textBrowser = QTextBrowser(self)
        for c in heuristic.keys():
            key=""
            key+=str(c)
            key+=": "
            key+=str(heuristic[c])
            self.textBrowser.append(key)

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)

class Result(QDialog):	#New window to show result: include the path from start to goal, total cost and the execute time for finding the path and drawing the graph
    def __init__(self, parent=None):
        super(Result, self).__init__(parent)

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.rejected.connect(self.reject)
        self.textBrowser = QTextBrowser(self)
        global path,elapsed,elapsed1
        key="Path: "
        for c in path:
            key+=c
            key+="->"
        key=key[:-2]
        cost=0
        for i in range(1,len(path)):
        	cost+=cities_distance[frozenset([path[i-1],path[i]])]


        self.textBrowser.append(key)
        key="Searching time: "+str(elapsed)
        self.textBrowser.append(key)
        key="Drawing time: "+str(elapsed1)
        self.textBrowser.append(key)
        self.textBrowser.append("Total length: "+str(cost))
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)

class MyWindow(QWidget):	#Main windows of the program
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        layout=QFormLayout()
        self.btn10=QPushButton("Read Distance from File")	#Read distance when provide the path to a txt file. Format is City1 \t City2 \t Distance
        self.btn10.clicked.connect(self.filedis)
        layout.addRow(self.btn10)
        self.btn11=QPushButton("Read Heuristic from File")	#Read heuristic when provide the path to a txt file. Format is City \t Heuristic value
        self.btn11.clicked.connect(self.fileheu)
        layout.addRow(self.btn11)
        self.btn=QPushButton("Add City")	#Add new city. If the input city already exist, ignore
        self.btn.clicked.connect(self.addcity)
        self.le=QLineEdit()
        layout.addRow(self.btn,self.le)

        self.btn4=QPushButton("Remove City")	#Remove city from existing city
        self.btn4.clicked.connect(self.removecity)
        layout.addRow(self.btn4)

        self.btn8=QPushButton("Choose start city")	#Choose start city
        self.btn8.clicked.connect(self.startcity)
        self.le8=QLineEdit()
        layout.addRow(self.btn8,self.le8)

        self.btn9=QPushButton("Choose goal city")	#Choose goal city
        self.btn9.clicked.connect(self.goalcity)
        self.le9=QLineEdit()
        layout.addRow(self.btn9,self.le9)

        self.btn5=QPushButton("Set Distance")		#Show a new window to set distance between 2 cities. Can be used to see the distance between two cities too
        self.btn5.clicked.connect(self.setdistance)
        layout.addRow(self.btn5)

        self.btn6=QPushButton("Print Distance")		#Print all existing connection between cities
        self.btn6.clicked.connect(self.printdistance)
        layout.addRow(self.btn6)

        self.btn7=QPushButton("Print Heuristic")	#Print all existing heuristic of cities
        self.btn7.clicked.connect(self.printheuristic)
        self.btn7.hide()
        layout.addRow(self.btn7)

        self.btn1=QPushButton("Choose algorithm")	#Show new window to select algorithm
        self.btn1.clicked.connect(self.getalgo)
        self.le1=QLineEdit()
        layout.addRow(self.btn1,self.le1)

        self.btn2=QPushButton("Set Heuristic")		#Show new windows to set heuristic, one city at a time. Can be used to see the current heuristic of cities too
        self.btn2.clicked.connect(self.addheuristic)
        self.btn2.hide()
        self.le2=QLineEdit()
        self.le2.hide()
        layout.addRow(self.btn2,self.le2)

        self.le.setReadOnly(True)
        self.le1.setReadOnly(True)
        self.le2.setReadOnly(True)

        self.btn3=QPushButton("Calculate Shortest Path")	#Start the calculation and show the Result window
        self.btn3.clicked.connect(self.calculate)
        layout.addRow(self.btn3)

        self.btn12=QPushButton("RESET DATA")
        self.btn12.clicked.connect(self.resetdata)			#Reset all data
        layout.addRow(self.btn12)

        self.setLayout(layout)
        self.setWindowTitle("AI DEMO")

    def fileheu(self):
        global heuristic
        filepath,ok=QInputDialog.getText(self,'Read heuristic from file','Enter heuristic path:')	#New window to read heuristic from a file
        if ok:
            fh = open(str(filepath), "rb")	#Open file from the given path
            #lines = fh.readlines()
            lines = fh.read().splitlines()
            for each_line in lines:

                words = each_line.split("\t")
                if (len(each_line)<1):		#Ignore empty line
                	continue
                temp=(str(words[0]).lower()).title()	#Get city name in lowercase
                if  temp not in city_list:				#If city is not in city list, add it in city list
                    city_list.append(temp)
                self.le.setText(str(len(city_list)))	#Update the count in the main window
                if (words[0].lower()).title() in heuristic:	#If the city already has a heuristic value, only change if the new value is smaller
                	if(heuristic[(words[0].lower()).title()]>int(words[1].strip("\r\n"))):
                		heuristic[(words[0].lower()).title()]=int(words[1].strip("\r\n"))
                else:
                	heuristic[(words[0].lower()).title()]=int(words[1].strip("\r\n"))
            fh.close()
            self.update_heuristic_status()	#Update heuristic count in the main window

    def resetdata(self):	#Reset all data
        global cities_distance,city_list,heuristic,path,elapsed,elapsed1
        city_list=[]
        heuristic={}
        cities_distance={}
        path=None
        elapsed=None
        elapsed1=None
        self.update_heuristic_status()
        self.le.setText(str(len(city_list)))
        self.le8.setText('')
        self.le9.setText('')
        self.le1.setText('')


    def filedis(self):
        global cities_distance
        filepath,ok=QInputDialog.getText(self,'Read distance from file','Enter distance path:')	#New windows to get path to distance file
        if ok:
            fh = open(str(filepath), "rb")
            lines = fh.read().splitlines()
            for each_line in lines:
                words = each_line.split("\t")
                if (len(each_line)<1):	#Ignore empty line
                	continue
                temp=(str(words[0]).lower()).title()	
                if  temp not in city_list:	#Add city if it not in city list
                    city_list.append(temp)
                self.le.setText(str(len(city_list)))
                temp=(str(words[1]).lower()).title()
                if  temp not in city_list:	#Add city if it not in city list
                    city_list.append(temp)
                self.le.setText(str(len(city_list)))
                if (str(words[0]).lower()).title()==(str(words[1]).lower()).title():	#If the two city is the same, ignore it
                	continue
                key=frozenset([(str(words[0]).lower()).title(),(str(words[1]).lower()).title()])	#Create new key from two city
                cities_distance[key]=int(words[2].strip("\r\n"))	#Add connection to database
            fh.close()

    def printdistance(self):	#Show the distance window
        showdistance=MyDialog(self)
        showdistance.show()

    def printheuristic(self):	#Show the heuristic window
        showheuristic=ShowH(self)
        showheuristic.show()

    def addcity(self):	#Add new city
        city,ok=QInputDialog.getText(self,'Add new city','Enter name of city:')	#Enter city name
        if ok:
            temp=(str(city).lower()).title()
            if  temp not in city_list:	#If city is not already existed in city list, add it in
                city_list.append(temp)
            self.le.setText(str(len(city_list)))

    def getalgo(self):
        algo,ok=QInputDialog.getText(self,'Choose algorithm','Input ID of algorithm(1: A*,2:UCS,3:Greedy BFS):')	#Pick algorithm by input an Integer
        if ok:
            if(int(algo)==1):
                self.le1.setText('A*')	#If 1, algorithm is A#
                self.btn2.show()
                self.le2.show()
                self.btn7.show()
            elif(int(algo)==2):
                self.le1.setText('Uniform Cost Search')	#If 2, algorithm is UCS
                self.btn2.hide()
                self.le2.hide()
                self.btn7.hide()
            elif(int(algo)==3):
                self.le1.setText('Greedy Best First Search')	#If 3, algorithm is GBFS
                self.btn2.show()
                self.le2.show()
                self.btn7.show()
            else:
                self.le1.setText('Invalid algorithm ID')	#	If value is something else, invalid algorithm

    def calculate(self):	#Start the process of finding path using selected algorithm and start/goal city
        global path,elapsed,elapsed1
        h_id=0
        total=True
        b=None
        for c in city_list:
            b=0
            for key in cities_distance:	#If there exist any city with no connnection to any other city, set total as false
                if c in key:
                    b+=1
                    break
            if(b>0):
                total=total*True	
            else:
                total=total*False
        if self.le1.text()=='A*':
            h_id=1
        elif self.le1.text()=='Uniform Cost Search':
            h_id=2
        elif self.le1.text()=='Greedy Best First Search':
            h_id=3
        if total==False:	#If total is false, show error that there exist any city with no connnection to any other city
            w=warning1(self)
               
            w.show()
        elif (h_id==0):#If algorithm is not valid, show error that algorithm is invalid
            w=warning2(self)
               
            w.show()
        elif (self.le8.text()=='' or self.le9.text()==''):	#Show error if start/goal city is empty
            w=warning3(self)	
            w.show()
        elif(len(heuristic.keys())!=len(city_list) and h_id!=2):	#Show error if heuristic is not declared for all cities
            w=warning4(self)
            w.show()

        if (h_id==1 or h_id==3) and total==True:
            if (self.le8.text()!='' and self.le9.text()!='' and len(heuristic.keys())==len(city_list)):	#If there is no error, start calculation. Since UCS do not need heuristic, it is executed separately
                path,elapsed,elapsed1=algorithm.execute(cities_distance,heuristic,str(self.le8.text()),str(self.le9.text()),h_id)	
                if path==None:	#If path is none,show error that no path is found
                    w=warning(self)
                    w.show()
                else:
	                showresult=Result(self)
	                showresult.show()
        elif h_id==2 and total==True:
            if (self.le8.text()!='' and self.le9.text()!='' ):
                path,elapsed,elapsed1=algorithm.execute(cities_distance,None,str(self.le8.text()),str(self.le9.text()),h_id)
                if path==None:	#If path is none,show error that no path is found
                    w=warning(self)
                    w.show()
                else:
                    showresult=Result(self)

                    showresult.show()

    def startcity(self):	#Choose start city from list of existing cities
        cities=[]
        for c in city_list:
            cities.append(c)	#Create list of existing cities
        if self.le9.text()!='':
            cities.remove(str(self.le9.text()))	#If end city is selected, remove end city from available city

        city_,ok=QInputDialog.getItem(self,"Select start city","List of cities",cities,0,False)	#Select city

        if ok and city_:
            self.le8.setText(str(city_))	

    def goalcity(self):	#Choose goal city from list of existing cities
        cities=[]
        for c in city_list:
            cities.append(c)	#Create list of existing cities
        if self.le8.text()!='':
            cities.remove(str(self.le8.text()))	#If start city is selected,remove start city from available city

        city_,ok=QInputDialog.getItem(self,"Select goal city","List of cities",cities,0,False)	#Select city

        if ok and city_:
            self.le9.setText(str(city_))

    def addheuristic(self):	#New window to set heuristic
        addh=AddHeuristic(self)
        addh.show()
        self.update_heuristic_status()

    def update_heuristic_status(self):	#Update the heuristic count in main menu
        temp=""
        temp+=str(len(heuristic.keys()))
        temp+='/'
        temp+=str(len(city_list))
        self.le2.setText(str(temp))

    def removecity(self):	#New window to remove city from list of existing cities
        cities=city_list

        city_,ok=QInputDialog.getItem(self,"Select city to remove","List of cities",cities,0,False)

        if ok and city_:
            city_list.remove(str(city_))
            for key in cities_distance.keys():	#Remove all connection involving this city
                if str(city_) in key:
                    cities_distance.pop(key)
            heuristic.pop(str(city_),None)	#Remove heuristic value
            self.update_heuristic_status()	#Update heuristic count
            self.le.setText(str(len(city_list)))	#Update city count

    def setdistance(self):	#New window to set cost of moving between two city
        addc= AddDistance(self)

        addc.show()
class AddHeuristic(QDialog):
    temp_city_list=[]
    def __init__(self, parent=None):
        super(AddHeuristic, self).__init__(parent)
        layout=QFormLayout()
        self.btn=QPushButton("Choose City")	#Choose city to set heuristic
        self.btn.clicked.connect(self.city1)	#Show new window to select city from list of existing cities
        self.le=QLineEdit()
        self.le.setReadOnly(True)
        layout.addRow(self.btn,self.le)
        self.temp_city_list=[]
        for c in city_list:
            self.temp_city_list.append(c)
        self.btn2=QPushButton("Set Heuristic")	#Show new window to set heuristic
        self.btn2.clicked.connect(self.seth)
        self.le2=QLineEdit()
        layout.addRow(self.btn2,self.le2)
        self.btn3=QPushButton("Save")	#Save the new heuristic
        self.btn3.clicked.connect(self.save)
        self.btn4=QPushButton("Back")	#Close window
        self.btn4.clicked.connect(self.back)
        self.le2.setReadOnly(True)
        layout.addRow(self.btn3,self.btn4)
        
        self.setLayout(layout)
    def city1(self):	#Select city from list of existing cities
        city_,ok=QInputDialog.getItem(self,"Select city 1","List of cities",self.temp_city_list,0,False)

        if ok and city_:
            if city_ in heuristic.keys():
                self.le2.setText(str(heuristic[str(city_)]))
            else:
                self.le2.setText('')
            self.le.setText(str(city_))
    def seth(self):	#Get heuristic value
        num,ok = QInputDialog.getInt(self,"Set Heuristic","Input heuristic:")

        if ok:
            self.le2.setText(str(num))
    def save(self):	#Update heuristic value
        if(self.le2.text()!=''):
            heuristic[str(self.le.text())]=int(self.le2.text())
    def back(self):	#Update heuristic count then close window
        parent=self.parent()
        parent.update_heuristic_status()
        self.close()
class AddDistance(QDialog):
    temp_city_list=[]
    def __init__(self, parent=None):
        super(AddDistance, self).__init__(parent)
        layout=QFormLayout()
        self.btn=QPushButton("Choose City 1")	#Choose city 1
        self.btn.clicked.connect(self.city1)	#Show new window to select city from existing cities
        self.le=QLineEdit()
        self.le.setReadOnly(True)
        layout.addRow(self.btn,self.le)
        self.temp_city_list=[]
        for c in city_list:
            self.temp_city_list.append(c)
        self.btn1=QPushButton("Choose City 2")	#Chose city 2
        self.btn1.clicked.connect(self.city2)	#Show new window to select city from existing cities
        self.le1=QLineEdit()
        layout.addRow(self.btn1,self.le1)

        self.btn2=QPushButton("Set Distance")	#Set distance between two city
        self.btn2.clicked.connect(self.distance)	#Show new window to set distance
        self.le2=QLineEdit()
        layout.addRow(self.btn2,self.le2)
        self.btn3=QPushButton("Save")	#Save the value
        self.btn3.clicked.connect(self.save)
        self.btn4=QPushButton("Back")	#Close the window
        self.btn4.clicked.connect(self.back)
        self.le1.setReadOnly(True)
        self.le2.setReadOnly(True)
        layout.addRow(self.btn3,self.btn4)
        
        self.setLayout(layout)
    def city1(self):	#Select city from existing cities
        cl=[]
        for c in self.temp_city_list:
            cl.append(c)   #Create cities list
        if self.le1.text()!='':
            cl.remove(str(self.le1.text()))	#If the other is already selected, remove that cities from available cities
        city_,ok=QInputDialog.getItem(self,"Select city 1","List of cities",cl,0,False)

        if ok and city_:
            if self.le1.text():
                if frozenset([str(city_),str(self.le1.text())]) in cities_distance.keys():	#If the other cities is already selected, show the distance between the two, leave it blank if there is no connection yet
                    self.le2.setText(str(cities_distance[frozenset([str(city_),str(self.le1.text())])]))
                else :
                    self.le2.setText('')
            self.le.setText(str(city_))
    def city2(self): 	#Similar to above
        cl=[]
        for c in self.temp_city_list:
            cl.append(c)   
        if self.le.text()!='':
            cl.remove(str(self.le.text()))
        city_,ok=QInputDialog.getItem(self,"Select city 2","List of cities",cl,0,False)

        if ok and city_:
            if self.le.text():
                if frozenset([str(self.le.text()),str(city_)]) in cities_distance.keys():
                    self.le2.setText(str(cities_distance[frozenset([str(self.le.text()),str(city_)])]))
                else:
                    self.le2.setText('')
            self.le1.setText(str(city_))
    def distance(self):	#Get an integer for distance
        num,ok = QInputDialog.getInt(self,"Set Distance","Input distance:")

        if ok:
            self.le2.setText(str(num))
    def save(self):	#Set the distance
        if(self.le2.text()!=''):
            key=frozenset([str(self.le.text()),str(self.le1.text())])	#Create a key of selected cities
            cities_distance[key]=int(self.le2.text())	#Set distance of the key as the input distance
    def back(self):	#Close the window
        self.close()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    main = MyWindow()
    main.show()
    sys.exit(app.exec_())
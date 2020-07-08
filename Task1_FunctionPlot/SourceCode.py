from sympy import *
from array import array
import numpy as np
from PySide2.QtWidgets import *
import pyqtgraph as pg
import sys
from PySide2.QtGui import QIcon, QPixmap, QFont
from PyQt5 import QtGui


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plot")
        self.setGeometry(500, 500, 500, 500)
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.setMaximumHeight(500)
        self.setMaximumWidth(500)
        self.center()
        self.UI()


    def UI(self):
        self.functionTextbox = QLineEdit(self)
        self.functionTextbox.move(360, 72)
        self.functionTextbox.cursor()
        self.functionTextbox.setFixedWidth(120)
        self.label1 = QLabel("Please enter the function of x you want to plot :", self)
        self.label1.setFont(QFont("Sanserif", 10))
        self.label1.move(15, 75)


        self.minimumTextbox = QLineEdit(self)
        self.minimumTextbox.move(370, 235)
        self.minimumTextbox.cursor()
        self.minimumTextbox.setFixedWidth(100)
        self.label2 = QLabel("Please enter the minimum value of x :", self)
        self.label2.setFont(QFont("Sanserif", 10))
        self.label2.move(15, 237)


        self.maximumTextbox = QLineEdit(self)
        self.maximumTextbox.move(370, 392)
        self.maximumTextbox.cursor()
        self.maximumTextbox.setFixedWidth(100)
        self.label3 = QLabel("Please enter the maximum value of x :", self)
        self.label3.setFont(QFont("Sanserif", 10))
        self.label3.move(15, 395)


        self.plot_button = QPushButton("Plot", self)
        self.plot_button.move(150, 450)
        self.plot_button.clicked.connect(self.plot_func)


        self.quit_button = QPushButton("Quit", self)
        self.quit_button.move(250, 450)
        self.quit_button.clicked.connect(self.quiteApp)

        self.setWindowIcon(QIcon("python.png"))
        self.show()


    def make_variable_lower_case(self,expr):
        expr = expr.replace("X", "x")
        return expr


    def plot_func(self):
        expr = self.functionTextbox.text()
        x_minimum = self.minimumTextbox.text()
        x_maximum = self.maximumTextbox.text()
        flag = self.check_validity(expr, x_minimum, x_maximum)
        if flag:
            expr = self.make_variable_lower_case(expr)
            x_values = np.linspace(float(x_minimum), float(x_maximum), num=100)
            function = sympify(expr)
            x = symbols("x")
            y_values = array('d')
            for index in range(len(x_values)):
                y_values.append(function.subs(x, x_values[index]))
            plotWidget = pg.plot(title="Function Plot")
            plotWidget.setWindowIcon(QIcon("python.png"))
            plotWidget.plot(x_values, y_values)


    def remove_spaces(self,expr):
        expr = expr.replace(" ", "")
        return expr


    def check_min_max(self, x_min, x_max):
        counter1 = 0
        counter2 = 0
        counter3 = 0
        counter4 = 0
        flag = True
        for index1 in range(len(x_min)):
            if not x_min[index1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '-'):
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText('Wrong value for minimum of x')
                msg.exec_()
            if x_min[index1] == '-' :
                counter1 = counter1 + 1
            if x_min[index1] == '.' :
                counter2 = counter2 + 1
        if counter1 > 1 :
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText('More than 1 negative sign in x_minimum')
            msg.exec_()
        if counter2 > 1 :
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText('More than 1 decimal point in x_minimum')
            msg.exec_()
        for index2 in range(len(x_max)):
            if not x_max[index2] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '-'):
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText('Wrong value for maximum of x')
                msg.exec_()
            if x_max[index2] == '-':
                    counter3 = counter3 + 1
            if x_max[index2] == '.':
                    counter4 = counter4 + 1
        if counter3 > 1:
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText('More than 1 negative sign in x_maximum')
            msg.exec_()
        if counter4 > 1:
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText('More than 1 decimal point in x_maximum')
            msg.exec_()
        if float(x_min) > float(x_max):
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText('Wrong values for minimum and maximum (minimum is greater than maximum)')
            msg.exec_()
        return flag


    def check_validity(self, expr, x_min, x_max):
        flag_1 = self.check_min_max(x_min, x_max)
        counter1 = 0
        counter2 = 0
        expr = self.remove_spaces(expr)
        expr = self.make_variable_lower_case(expr)
        flag = True
        for index in range(len(expr)):
            if not expr[index] in (
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', '-', '*', '/', '^', '(', ')', 'x'):
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText('Unknown symbol entered in your expression (' + expr[index] + ')')
                msg.exec_()
            if expr[index] == '(':
                counter1 = counter1 + 1
            if expr[index] == ')':
                counter2 = counter2 + 1
        for index1 in range(len(expr) - 1):
            if expr[index1] == '+' and expr[index1 + 1] == '+':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive '+' operator  ")
                msg.exec_()
            if expr[index1] == '-' and expr[index1 + 1] == '-':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive '-' operator ")
                msg.exec_()
            if expr[index1] == '*' and expr[index1 + 1] == '*':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive '*' operator ")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == '/':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive '/' operator ")
                msg.exec_()
            if expr[index1] == '^' and expr[index1 + 1] == '^':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive '^' operator ")
                msg.exec_()
            if expr[index1] == '+' and expr[index1 + 1] == '-':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '+-'")
                msg.exec_()
            if expr[index1] == '+' and expr[index1 + 1] == '*':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '+*'")
                msg.exec_()
            if expr[index1] == '+' and expr[index1 + 1] == '/':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '+/'")
                msg.exec_()
            if expr[index1] == '+' and expr[index1 + 1] == '^':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '+^'")
                msg.exec_()
            if expr[index1] == '-' and expr[index1 + 1] == '+':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '-+'")
                msg.exec_()
            if expr[index1] == '-' and expr[index1 + 1] == '*':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '-*'")
                msg.exec_()
            if expr[index1] == '-' and expr[index1 + 1] == '/':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '-/'")
                msg.exec_()
            if expr[index1] == '-' and expr[index1 + 1] == '^':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '-^'")
                msg.exec_()
            if expr[index1] == '*' and expr[index1 + 1] == '+':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '*+'")
                msg.exec_()
            if expr[index1] == '*' and expr[index1 + 1] == '-':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '*-'")
                msg.exec_()
            if expr[index1] == '*' and expr[index1 + 1] == '/':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '*/'")
                msg.exec_()
            if expr[index1] == '*' and expr[index1 + 1] == '^':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '*^'")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == '+':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '/+'")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == '-':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '/-'")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == '*':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '/*'")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == '^':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '/^'")
                msg.exec_()
            if expr[index1] == '^' and expr[index1 + 1] == '+':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '^+'")
                msg.exec_()
            if expr[index1] == '^' and expr[index1 + 1] == '-':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '^-'")
                msg.exec_()
            if expr[index1] == '^' and expr[index1 + 1] == '*':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '^*'")
                msg.exec_()
            if expr[index1] == '^' and expr[index1 + 1] == '/':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive operators '^/'")
                msg.exec_()
            if expr[index1 + 1] == 'x' and expr[index1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText(
                    "ERROR !! Missing operator between variable 'x' and the number before it '" + expr[index1] + "x'")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == '0':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Division by zero undefined")
                msg.exec_()
            if expr[index1] == 'x' and expr[index1 - 1] == 'x':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing operator between two consecutive variable x ")
                msg.exec_()
            if expr[index1] == 'x' and expr[index1 + 1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText(
                    "ERROR !! Missing operator between variable 'x' and the number after it '" + expr[index1 + 1] + "'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == 'x':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before variable x")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Multiple consecutive decimal points '..'")
                msg.exec_()
            if expr[index1] == '+' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right after operator '+.'")
                msg.exec_()
            if expr[index1] == '-' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right after operator '-.'")
                msg.exec_()
            if expr[index1] == '*' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right after operator '*.'")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right after operator '/.'")
                msg.exec_()
            if expr[index1] == '^' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right after operator '^.'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == '+':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before operator '.+'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == '-':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before operator '.-'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == '*':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before operator '.*'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == '/':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before operator './'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == '^':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before operator '.^'")
                msg.exec_()
            if expr[index1] == '(' and expr[index1 + 1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! empty brackets")
                msg.exec_()
            if expr[index1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9') and expr[index1 + 1] == '(':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing operator between number and bracket '" + expr[index1] + "('")
                msg.exec_()
            if expr[index1] == ')' and expr[index1 + 1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing operator between number and bracket ')" + expr[index1 + 1] + "'")
                msg.exec_()
            if expr[index1] == '+' and expr[index1 + 1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between operator + and bracket '+)'")
                msg.exec_()
            if expr[index1] == '-' and expr[index1 + 1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between operator - and bracket '-)'")
                msg.exec_()
            if expr[index1] == '*' and expr[index1 + 1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between operator * and bracket '*)'")
                msg.exec_()
            if expr[index1] == '/' and expr[index1 + 1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between operator / and bracket '/)'")
                msg.exec_()
            if expr[index1] == '^' and expr[index1 + 1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between operator ^ and bracket '^)'")
                msg.exec_()
            if expr[index1] == '(' and expr[index1 + 1] == '+':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between bracket and operator '(+'")
                msg.exec_()
            if expr[index1] == '(' and expr[index1 + 1] == '-':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between bracket and operator '(-'")
                msg.exec_()
            if expr[index1] == '(' and expr[index1 + 1] == '*':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between bracket and operator '(*'")
                msg.exec_()
            if expr[index1] == '(' and expr[index1 + 1] == '/':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between bracket and operator '(/")
                msg.exec_()
            if expr[index1] == '(' and expr[index1 + 1] == '^':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing number or variable x between bracket and operator '(^'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before bracket '.)'")
                msg.exec_()
            if expr[index1] == '.' and expr[index1 + 1] == '(':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right before bracket '.('")
                msg.exec_()
            if expr[index1] == ')' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right after bracket ').'")
                msg.exec_()
            if expr[index1] == '(' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! decimal point right after bracket '(.'")
                msg.exec_()
            if expr[index1] == 'x' and expr[index1 + 1] == '(':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing operator between variable x and bracket 'x('")
                msg.exec_()
            if expr[index1 + 1] == 'x' and expr[index1] == ')':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing operator between variable x and bracket ')x'")
                msg.exec_()
            if expr[index1] == '.' and not expr[index1 + 1] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Invalid decimal point '." + expr[index1 + 1] + "'")
                msg.exec_()
            if expr[index1] == ')' and expr[index1 + 1] == '(':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Missing operator between the brackets ')('")
                msg.exec_()
            if expr[index1] == 'x' and expr[index1 + 1] == '.':
                flag = False
                msg = QMessageBox()
                msg.setWindowTitle("Error Detected")
                msg.setText("ERROR !! Invalid decimal point 'x.'")
                msg.exec_()
        if counter1 != counter2:
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Number of opened brackets does not equal the number of closed brackets")
            msg.exec_()
        if expr[0] == '+':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("Error !! operator at the beginning of the function '+'")
            msg.exec_()
        if expr[0] == '-':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("Error !! operator at the beginning of the function '-'")
            msg.exec_()
        if expr[0] == '*':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("Error !! operator at the beginning of the function '*'")
            msg.exec_()
        if expr[0] == '/':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("Error !! operator at the beginning of the function '/'")
            msg.exec_()
        if expr[0] == '^':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("Error !! operator at the beginning of the function '^'")
            msg.exec_()
        if expr[0] == '.':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("Error !! decimal point at the beginning of the function '.'")
            msg.exec_()
        if expr[0] == ')':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("Error !! a Closing bracket at the beginning of the function ')'")
            msg.exec_()
        if expr[len(expr) - 1] == '+':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Operator at the end of the function '+'")
            msg.exec_()
        if expr[len(expr) - 1] == '-':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Operator at the end of the function '-'")
            msg.exec_()
        if expr[len(expr) - 1] == '*':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Operator at the end of the function '*'")
            msg.exec_()
        if expr[len(expr) - 1] == '/':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Operator at the end of the function '/'")
            msg.exec_()
        if expr[len(expr) - 1] == '^':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Operator at the end of the function '^'")
            msg.exec_()
        if expr[len(expr) - 1] == '.':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Missing number after last decimal point in the function '.'")
            msg.exec_()
        if expr[len(expr) - 1] == '(':
            flag = False
            msg = QMessageBox()
            msg.setWindowTitle("Error Detected")
            msg.setText("ERROR !! Opened bracket at the end of the function")
            msg.exec_()
        return flag and flag_1

    def center(self):
        qrect = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qrect.moveCenter(center_point)
        self.move(qrect.topLeft())

    def quiteApp(self):
        userInfo = QMessageBox.question(self, "Confirmation", "Do You Want To Quit The Application ? ",
                                        QMessageBox.Yes | QMessageBox.No)

        if userInfo == QMessageBox.Yes:
            myApp.quit()

        elif userInfo == QMessageBox.No:
            pass


myApp = QApplication(sys.argv)
window = Window()
window.show()
myApp.exec_()
sys.exit(0)

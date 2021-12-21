import os
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit

def eqCreateTemp(self):
	sambaDir = "/Users/paulo/Desktop/Python_Script/Eq_auto/Samba"
	eqEventName_input = str(self.InfoEv.text()).strip()
	year = eqEventName_input[:4]
	month = eqEventName_input[5:7]
	sambaMonth = datetime.strptime(month, '%m')
	sambaMonth= sambaMonth.strftime('%B')
	print(sambaMonth)

	#self.smsBox.setPlainText("paulo")
	#self.fbBox.setText("gwapo")
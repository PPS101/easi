import os, shutil, codecs
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit

def eqUpload(self):
	mainDir  = "D:\\Eq_auto"
	sambaDir = "D:\\Eq_auto\\Samba"
	eqEventName_input = str(self.InfoEv.text()).strip()
	year = eqEventName_input[:4]
	month = eqEventName_input[5:7]
	sambaMonth = datetime.strptime(month, '%m')
	sambaMonth= sambaMonth.strftime('%B')
	day = eqEventName_input[7:9]
	eqInfoFile_folder = mainDir + "\\" + "Earthquake_Information\\" + year + "_Earthquake_Information\\" + month + "\\" + day
	eqInfoFile = year + "_" + month + day + eqEventName_input[9:] + ".html"
	sambaFolder = sambaDir + "\\" + year + "_Earthquake_Information\\" + sambaMonth
	linkEqEventFile = sambaFolder + "\\" + eqInfoFile
	if not os.path.exists(sambaFolder):
		os.makedirs(sambaFolder)
	shutil.copy(mainDir + "\\" + "red_circle.svg", sambaFolder)
	shutil.copy(eqInfoFile_folder + "\\" + eqInfoFile, sambaFolder)
	utf8_event = eqInfoFile[:-5] + '_utf8.html'
	BLOCKSIZE = 1048576
	with codecs.open(sambaFolder + "\\" + eqInfoFile, "r", "windows-1252") as sourceFile:
		with codecs.open(sambaFolder + "\\" + utf8_event , "w", "utf-8") as targetFile:
			while True:
				contents = sourceFile.read(BLOCKSIZE)
				if not contents:
					break
				targetFile.write(contents)
				targetFile.close()
	sourceFile.close()
	with open(sambaFolder + "\\" + utf8_event, 'r') as eqInfo_open:
		EqInfoEventLine = eqInfo_open.read().splitlines()

	findDt = "<!-- 2 DateTime-Data  -->"
	findLoc = "<!-- 3 Location-Data  -->"
	findDep = "<!-- 4 Depth-Data  -->"
	findMag = "<!-- 5 Magnitude-Data  -->"
	evCount = []
	for i, line in enumerate(EqInfoEventLine):
		if findDt in line:
			lineDT = i + 1
			eqInfo_dt = EqInfoEventLine[lineDT].strip()
			eqInfo_dt = datetime.strptime(eqInfo_dt, '%d %b %Y - %I:%M:%S %p') 
			eqInfo_dt = eqInfo_dt.strftime('%d %B %Y - %I:%M %p')
		if findLoc in line:
			lineLoc = i + 1
			eqInfo_loc = EqInfoEventLine[lineLoc].strip()
			eqInfo_Mainloc = eqInfo_loc.split(' - ')[1].strip()
			eqInfo_Mainloc_0 = eqInfo_Mainloc.split(' km ')[0].strip()
			eqInfo_Mainloc_1 = "km " + eqInfo_Mainloc.split(' km ')[1].strip()
			eqInfoLatLon = eqInfo_loc.split(' - ')[0].strip()
			eqInfoLat = eqInfoLatLon.split(',')[0].strip()[:-3]
			eqInfoLon= eqInfoLatLon.split(',')[1].strip()[:-3]
		if findDep in line:
			lineDep = i + 1
			eqInfo_dep = EqInfoEventLine[lineDep].strip()
		if findMag in line:
			lineMag = i + 1
			eqInfo_mag = EqInfoEventLine[lineMag].strip()
			eqInfo_mag = eqInfo_mag.split()[-1]
	with open (mainDir + '\\EQweb_format.txt', 'r') as format:
		formatHtml_lines = format.read().splitlines()
		if 4.0 <= float(eqInfo_mag) < 5.0:
			formatHtml_lines[15] = formatHtml_lines[15].replace('(MAGNITUDE)','<strong>(MAGNITUDE)</strong>')
		elif 5.0 <= float(eqInfo_mag) < 6.0:
			formatHtml_lines[15] = formatHtml_lines[15].replace('(MAGNITUDE)','<strong> <font color = "blue">(MAGNITUDE)</strong>')
		elif float(eqInfo_mag) >= 6.0:
			formatHtml_lines[15] = formatHtml_lines[15].replace('(MAGNITUDE)','<strong> <font color = "red">(MAGNITUDE)</strong>')
		else:
			formatHtml_lines[15] = formatHtml_lines[15]
		newLine_0 = formatHtml_lines[0]
		newLine_1 = formatHtml_lines[1]
		newLine_2 = formatHtml_lines[2]
		newLine_3 = formatHtml_lines[3].replace('(EQ INFO Link)', linkEqEventFile)
		if self.comboFOrNf.currentText() == "Felt":
			formatHtml_lines[4] = formatHtml_lines[4].split('</span>',1)[0].replace('<span class="auto-style99">', "") + formatHtml_lines[4].split('</span>',1)[1]
		elif self.comboFOrNf.currentText() == "Not Felt":
			formatHtml_lines[4] = formatHtml_lines[4]
		else:
			QMessageBox.information(self, "Message", "Please choose if Felt or Not")
			return
		newLine_4 = formatHtml_lines[4].replace('(DATE - TIME)', eqInfo_dt)
		newLine_5 = formatHtml_lines[5]
		newLine_6 = formatHtml_lines[6].replace('(LATITUDE)', eqInfoLat)
		newLine_7 = formatHtml_lines[7]
		newLine_8 = formatHtml_lines[8]
		newLine_9 = formatHtml_lines[9].replace('(LONGITUDE)', eqInfoLon)
		newLine_10 = formatHtml_lines[10]
		newLine_11 = formatHtml_lines[11]
		newLine_12 = formatHtml_lines[12].replace('(DEPTH)', eqInfo_dep)
		newLine_13 = formatHtml_lines[13]
		newLine_14 = formatHtml_lines[14]
		newLine_15 = formatHtml_lines[15].replace('(MAGNITUDE)', eqInfo_mag)
		newLine_16 = formatHtml_lines[16]
		newLine_17 = formatHtml_lines[17].replace('(LOCATION 1)', eqInfo_Mainloc_0)
		newLine_18 = formatHtml_lines[18].replace('(LOCATION 2)', eqInfo_Mainloc_1)
		newLine_19 = formatHtml_lines[19]
		newHtmlLines = newLine_0 + '\n' + newLine_1 + '\n' + newLine_2 +'\n' + newLine_3 + '\n' + newLine_4 + '\n' + newLine_5 + '\n' + newLine_6 + '\n' + newLine_7 + '\n' + newLine_8 + '\n' + newLine_9 + '\n' + newLine_10 + '\n' + newLine_11 + '\n' + newLine_12 + '\n' + newLine_13 + '\n' + newLine_14 + '\n' + newLine_15 + '\n' + newLine_16 + '\n' + newLine_17 + '\n' + newLine_18 + '\n' + newLine_19
		result = QMessageBox.question(self, 'Message', 'Are you sure you want to upload? \n' + eqInfoFile + '\n' + self.comboFOrNf.currentText() + '\n' + eqInfo_dt + '\n' + 'M' + eqInfo_mag + '\n' + eqInfoLat + 'N, ' + eqInfoLon + 'E - ' + eqInfo_Mainloc_0 + ' ' + eqInfo_Mainloc_1, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if result == QMessageBox.Yes:
			with codecs.open (sambaDir + '\\EQLatest.html', 'r') as eqHtml_read:
				htmlLine = eqHtml_read.readlines()
				clue = 'enter new event below'
				for i,line in enumerate(htmlLine):
					if clue in line:
						insertToLine = i+1
				htmlLine.insert(insertToLine,'\n' + newHtmlLines + '\n')
				eqHtml_read.close()
				with open (sambaDir + '\\EQLatest.html', 'w') as eqHtml_write:
					htmlLine = "".join(htmlLine)
					eqHtml_write.writelines(htmlLine)
					eqInfo_open.close()
					format.close()
					eqHtml_read.close()
					eqHtml_write.close()
					QMessageBox.about(self, 'Upload Status', "Upload finished!")
		else:
			return

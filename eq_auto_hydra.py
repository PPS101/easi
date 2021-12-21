import os, codecs, shutil, time, webbrowser, pygmt, glob
import pandas as pd
from datetime import datetime
from pytz import timezone
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit

def create_EQinfoHydra(self):
	start_time = time.time()
	mainDir = 'D:\\Eq_auto'
	#os.chdir('D:\\Eq_auto\\temp')
	os.chdir('Y:\\output\\raypellets\\auto\\saved')
	try:
		file_list = sorted(glob.glob("*.GSE"))
		latestEqEvent = file_list[-1]
		print(latestEqEvent)
		#file_x = glob.glob("*.GSE")
		#max_file = max(file_x, key=os.path.getctime)
		#print(max_file)
		latestEqEvent_open = codecs.open(latestEqEvent, 'r', "utf-8")
		latestEqEvent_lines = latestEqEvent_open.readlines()
		latestEqEvent_dataline1= latestEqEvent_lines[8].split(' ')
		latestEqEvent_dataline1 = list(filter(None,latestEqEvent_dataline1))
		latestEqEvent_dt =  ' - '.join(latestEqEvent_dataline1[0:2])
		latestEqEvent_dt = datetime.strptime(latestEqEvent_dt, '%Y/%m/%d - %H:%M:%S.%f') #convert to datetime format
		ev_filename = latestEqEvent_dt.strftime('%Y_%m%d_%H%M')
		ev_month = str(latestEqEvent_dt.strftime('%m')).strip()
		ev_day = str(latestEqEvent_dt.strftime('%d')).strip()
		ev_year = str(latestEqEvent_dt.strftime('%Y')).strip()
		ev_filename_forEqinfo = ev_filename + '_B1'
		ev_filename_final = ev_filename + '_B1' + '.html' # create a filename
		latestEqEvent_dt = timezone('Asia/Manila').fromutc(latestEqEvent_dt) #convert to local time
		ev_dt = latestEqEvent_dt.strftime('%d %b %Y - %I:%M:%S %p') #converted date-time in your format
		now = datetime.now()
		dtNow = now.strftime('%d %b %Y - %I:%M:%S %p')
		ev_lat = latestEqEvent_dataline1[4].strip()
		ev_lon = latestEqEvent_dataline1[5].strip()
		ev_lat = format(float(ev_lat[:-1]),"06.3f")
		ev_lon = format(float(ev_lon[:-1]),"07.3f")
		if float(ev_lat) > 22 or float(ev_lat) < 2 or float(ev_lon) < 116  or float(ev_lon) > 130:
			QMessageBox.information(self, "Message", "The epicenter is outside of the PAR")
			return
		out_lat = format(float(ev_lat[:-1]),"05.2f") + '°N'
		out_lon = format(float(ev_lon[:-1]),"06.2f") + '°E'
		ev_latlon = out_lat + ', ' + out_lon
		infoOut_lat = format(float(ev_lat),"06.3f")
		infoOut_lon = format(float(ev_lon),"07.3f")
		infoEv_latlon = str(infoOut_lat).strip('0') + ", " + str(infoOut_lon).strip('0')
		ev_dep = str(round(float(latestEqEvent_dataline1[9]))).zfill(3)
		mag_clue = [match for match in latestEqEvent_lines if "Official Magnitude:" in match]
		mag_line= latestEqEvent_lines.index(''.join(mag_clue)) + 1
		ev_mag = latestEqEvent_lines[mag_line]
		#if 'w' in ev_mag.split(' ')[0] or 'W' in ev_mag.split(' ')[0]:
		type_mag = "M"
		#else:
		#type_mag = ev_mag.split(' ')[0]
		ev_mag = type_mag + " " +  str(round(float(ev_mag.split(' ')[1]), 1))
		intensities = str(self.IntBox.toPlainText()).splitlines()
		intensityList=' '.join(['<br>' + intensity for intensity in intensities])

		def haversine(lon1, lat1, lon2, lat2):
			lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
			dlon = lon2 - lon1 
			dlat = lat2 - lat1 
			a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
			c = 2 * asin(sqrt(a))
			r = 6371 # Radius of earth in kilometers. Use 3956 for miles
			eventDistance = c * r
			return eventDistance
	
		def direction(lon1, lat1, lon2, lat2):
			dX = lat2 - lat1
			dY = lon2 - lon1
			if dX < 0 and dY > 0:
				bearing = int(degrees(atan2(dY,-dX)))
				bearing = "S " + str(bearing) + "° E"
			elif dY < 0 and dX > 0:
				bearing = int(degrees(atan2(-dY,dX)))
				bearing = "N " + str(bearing) + "° W"
			elif dX < 0 and dY < 0:
				bearing = int(degrees(atan2(-dY,-dX)))
				bearing = "S " + str(bearing) + "° W"
			else:
				bearing = int(degrees(atan2(dY,dX)))
				bearing = "N " + str(bearing) + "° E"
			return bearing

		def towns_distance():
			towns = pd.read_csv('D:\\Eq_auto\\Towns.csv')
			towns['EvLat'] = float(ev_lat)
			towns['EvLon'] = float(ev_lon)
			towns['Distance'] = [haversine(towns.EvLon[i],towns.EvLat[i],towns.lon[i],towns.lat[i]) for i in range(len(towns))]
			towns['Distance'] = towns['Distance'].astype(int)
			towns['Bearing to EV'] = [direction(towns.lon[i],towns.lat[i],towns.EvLon[i],towns.EvLat[i]) for i in range(len(towns))]
			towns.sort_values(by=['Distance'], inplace=True)
			towns.drop(['lat','lon','EvLat','EvLon'], axis = 1, inplace=True)
			towns = towns[['Distance','Bearing to EV', 'loc']]
			towns = towns.head(1)
			return towns.values.tolist()

		dist_town_ev = str(towns_distance()[0][0]).zfill(3) + ' km'
		bear_town_ev = str(towns_distance()[0][1]).zfill(2)
		town_ev = towns_distance()[0][2].title()
		ev_loc = ev_latlon + ' - ' + dist_town_ev + ' ' + bear_town_ev + ' of ' + town_ev

		issuedBy = str(self.tboxInitials.text())
		EqInfo_folder = mainDir +'\\Earthquake_Information\\' + ev_year + '_Earthquake_Information\\' + ev_month + '\\' + ev_day
		print(EqInfo_folder)
		if not os.path.exists(EqInfo_folder):
			os.makedirs(EqInfo_folder)
		os.chdir(mainDir)
		EqInfo = open(EqInfo_folder + '\\' + ev_filename_final, 'w',encoding="utf8", errors='ignore')
		EqInfo_template = open('EQ_Info_template.html','r',encoding="utf8", errors='ignore')
		for line in EqInfo_template:
			if self.radioDamageY.isChecked():
				replacelineAftYes = line.replace('EQ INFO TITLE', ev_filename).replace('(DATE - TIME)', ev_dt).replace('(LOCATION OF EVENT)', ev_loc).replace('(DEPTH OF EVENT)', ev_dep).replace('(MAGNITUDE OF EVENT)', ev_mag).replace("const mymap = L.map('mapid').setView(new L.LatLng(0,0), 7);", "const mymap = L.map('mapid').setView(new L.LatLng(" + infoEv_latlon + "), 7);").replace("let Event = L.marker([0,0], {icon: myIcon}).addTo(mymap);","let Event = L.marker([" + infoEv_latlon + "], {icon: myIcon}).addTo(mymap);").replace('(ISSUED DATE - TIME)', dtNow).replace('AFTERSHOCKS?', 'YES').replace('INITIALS', issuedBy).replace('DAMAGE?', 'YES').replace('EQ INFO Filename', ev_filename_forEqinfo).replace('Insert Intensity here', intensityList)
				replacelineAftNo = line.replace('EQ INFO TITLE', ev_filename).replace('(DATE - TIME)', ev_dt).replace('(LOCATION OF EVENT)', ev_loc).replace('(DEPTH OF EVENT)', ev_dep).replace('(MAGNITUDE OF EVENT)', ev_mag).replace("const mymap = L.map('mapid').setView(new L.LatLng(0,0), 7);", "const mymap = L.map('mapid').setView(new L.LatLng(" + infoEv_latlon + "), 7);").replace("let Event = L.marker([0,0], {icon: myIcon}).addTo(mymap);","let Event = L.marker([" + infoEv_latlon + "], {icon: myIcon}).addTo(mymap);").replace('(ISSUED DATE - TIME)', dtNow).replace('AFTERSHOCKS?', 'NO').replace('INITIALS', issuedBy).replace('DAMAGE?', 'YES').replace('EQ INFO Filename', ev_filename_forEqinfo).replace('Insert Intensity here', intensityList)
			elif self.radioDamageN.isChecked():
				replacelineAftYes = line.replace('EQ INFO TITLE', ev_filename).replace('(DATE - TIME)', ev_dt).replace('(LOCATION OF EVENT)', ev_loc).replace('(DEPTH OF EVENT)', ev_dep).replace('(MAGNITUDE OF EVENT)', ev_mag).replace("const mymap = L.map('mapid').setView(new L.LatLng(0,0), 7);", "const mymap = L.map('mapid').setView(new L.LatLng(" + infoEv_latlon + "), 7);").replace("let Event = L.marker([0,0], {icon: myIcon}).addTo(mymap);","let Event = L.marker([" + infoEv_latlon + "], {icon: myIcon}).addTo(mymap);").replace('(ISSUED DATE - TIME)', dtNow).replace('AFTERSHOCKS?', 'YES').replace('INITIALS', issuedBy).replace('DAMAGE?', 'NO').replace('EQ INFO Filename', ev_filename_forEqinfo).replace('Insert Intensity here', intensityList)
				replacelineAftNo = line.replace('EQ INFO TITLE', ev_filename).replace('(DATE - TIME)', ev_dt).replace('(LOCATION OF EVENT)', ev_loc).replace('(DEPTH OF EVENT)', ev_dep).replace('(MAGNITUDE OF EVENT)', ev_mag).replace("const mymap = L.map('mapid').setView(new L.LatLng(0,0), 7);", "const mymap = L.map('mapid').setView(new L.LatLng(" + infoEv_latlon + "), 7);").replace("let Event = L.marker([0,0], {icon: myIcon}).addTo(mymap);","let Event = L.marker([" + infoEv_latlon + "], {icon: myIcon}).addTo(mymap);").replace('(ISSUED DATE - TIME)', dtNow).replace('AFTERSHOCKS?', 'NO').replace('INITIALS', issuedBy).replace('DAMAGE?', 'NO').replace('EQ INFO Filename', ev_filename_forEqinfo).replace('Insert Intensity here', intensityList)
			else:
				QMessageBox.information(self, "Message", "Please choose whether expecting damage or not!")
				return
			if ev_mag >= '5.0' and ev_dep <= '150':
				EqInfo.write(replacelineAftYes)
			else:
				EqInfo.write(replacelineAftNo)
		shutil.copy('red_circle.svg', EqInfo_folder)
		EqInfo.close()
		EqInfo_template.close()
		webbrowser.open('file:\\\\' + EqInfo_folder + '\\' + ev_filename_final, new=2)

		if float(ev_lat) <= 22 and float(ev_lat) >= 16 and float(ev_lon) >= 116 and float(ev_lon) <= 126:
			minLat = 14
			maxLat = 22
			minLon = 116
			maxLon = 126
		elif float(ev_lat) < 16 and float(ev_lat) >= 12.5 and float(ev_lon) >= 117 and float(ev_lon) <= 128:
			minLat = 10
			maxLat = 18
			minLon = 117
			maxLon = 128
		elif float(ev_lat) < 12.5 and float(ev_lat) >= 9 and float(ev_lon) >= 117 and float(ev_lon) <= 129:
			minLat = 6
			maxLat = 14
			minLon = 117
			maxLon = 129
		elif float(ev_lat) < 9 and float(ev_lat) >=2 and float(ev_lon) >= 117 and float(ev_lon) <= 130:
			minLat = 2
			maxLat = 10
			minLon = 117
			maxLon = 130
		else:
			QMessageBox.information(self, "Message", "The epicenter is outside of the PAR")
			return

		region = [minLon, maxLon, minLat, maxLat]
		grid = pygmt.datasets.load_earth_relief(resolution="30s",region=region)
		fig = pygmt.Figure()
		fig.grdimage(grid=grid, projection= 'M25',frame=['a2f2', 'WSne'],cmap = 'geo')

		fig.plot(
			data="AF.gmt",
			pen=".1p,red",
		)

		fig.plot(
			data="trench.gmt",
			Sf = '+.3i/.1i+l+t',
			color="blue",
			pen=".4p,blue",
		)

		fig.plot(
			x = float(ev_lon),
			y = float(ev_lat),
			style = 'c0.2i',
			color = 'red',
			pen= ".1p,black",
		)

		fig.savefig(EqInfo_folder + '\\' + ev_filename_forEqinfo + ".jpg")
		print("--- %s seconds ---" % (time.time() - start_time))
		QMessageBox.information(self, "Message", "Successfully created an earthquake information")

	
	except ValueError:
		QMessageBox.information(self, "Message", "Sorry can't use the file " + latestEqEvent.split('/')[-1] + " yet, Try again after a few seconds")
		return



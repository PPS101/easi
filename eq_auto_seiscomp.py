import os, codecs, shutil, time, webbrowser, pygmt
import pandas as pd
from paramiko import SSHClient, AutoAddPolicy
from datetime import datetime
from pytz import timezone
from math import radians, cos, sin, asin, sqrt, atan2, degrees
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit

def create_EQinfoSeiscomp(self):
    start_time = time.time()
    mainDir = 'D:\\Eq_auto'
    os.chdir(mainDir)

    router_ip = "192.168.100.66"
    router_username = "sysop"
    router_password = "bolinao2003"
    
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    ssh.connect(router_ip, username=router_username, password=router_password)
    
    ftp = ssh.open_sftp()
    file = ftp.open('/home/sysop/.seiscomp3/bulletin.txt')
    initial_ev = file.readlines()
    id_clue = [match for match in initial_ev if "Public ID" in match]
    id_line = initial_ev.index(''.join(id_clue))
    id_ev = initial_ev[id_line]
    id_ev = id_ev.split()[-1]
    file.close()
    
    shell_file = ftp.open('/home/sysop/.seiscomp3/bang.sh', 'r')
    shell_line = shell_file.readlines()
    shell_idClue = [match for match in shell_line if "(ID)" in match]
    shell_idLine = shell_line.index(''.join(shell_idClue))
    ev_shell = '#!/bin/sh' + '\n' + '\n' + 'scbulletin -d mysql://sysop:sysop@localhost/seiscomp3 -E ' + id_ev + ' -3 '
    evshell_file = ftp.open('/home/sysop/ev.sh', 'w')
    evshell_file.write(ev_shell)
    evshell_file.close()
    evshell_file.close()
    shell_file.close()
    
    bash_script = ftp.open("ev.sh").read()
    stdin, stdout, stderr = ssh.exec_command(bash_script)
    ev = stdout.read().decode()
    file_ev = open('seiscomp3_event.txt', 'w')
    file_ev.write(''.join(ev))
    file_ev.close()
    ftp.close()
    ssh.close()
    
    file = open('seiscomp3_event.txt', 'r')
    seis_ev = file.readlines()
    date_clue = [match for match in seis_ev if "Date" in match]
    date_line= seis_ev.index(''.join(date_clue))
    ev_date = seis_ev[date_line].split()[1]
    time_clue = [match for match in seis_ev if "Time" in match]
    time_line= seis_ev.index(''.join(time_clue))
    ev_time = seis_ev[time_line].split()[1]
    ev_dt = ev_date + ' - ' + ev_time
    ev_dt = datetime.strptime(ev_dt, '%Y-%m-%d - %H:%M:%S.%f') #convert to datetime format
    ev_filename = ev_dt.strftime('%Y_%m%d_%H%M')
    ev_month = str(ev_dt.strftime('%m')).strip()
    ev_day = str(ev_dt.strftime('%d')).strip()
    ev_year = str(ev_dt.strftime('%Y')).strip()
    ev_filename_forEqinfo = ev_filename + '_B1'
    ev_filename_final = ev_filename + '_B1' + '.html' # create a filename
    ev_dt = timezone('Asia/Manila').fromutc(ev_dt) #convert to local time
    ev_dt = ev_dt.strftime('%d %b %Y - %I:%M:%S %p')
    now = datetime.now()
    dtNow = now.strftime('%d %b %Y - %I:%M:%S %p')
    lat_clue = [match for match in seis_ev if "Latitude" in match]
    lat_line= seis_ev.index(''.join(lat_clue))
    ev_lat = seis_ev[lat_line].split()[1]
    lon_clue = [match for match in seis_ev if "Longitude" in match]
    lon_line= seis_ev.index(''.join(lon_clue))
    ev_lon = seis_ev[lon_line].split()[1]
    if float(ev_lat) > 22 or float(ev_lat) < 2 or float(ev_lon) < 116  or float(ev_lon) > 130:
        QMessageBox.information(self, "Message", "The epicenter is outside of the PAR")
        return
    out_lat = format(float(ev_lat),"05.2f") + '°N'
    out_lon = format(float(ev_lon),"06.2f") + '°E'
    ev_latlon = out_lat + ", " + out_lon
    infoOut_lat = format(float(ev_lat),"06.3f")
    infoOut_lon = format(float(ev_lon),"07.3f")
    infoEv_latlon = str(infoOut_lat).strip('0') + ", " + str(infoOut_lon).strip('0')
    dep_clue = [match for match in seis_ev if "Depth" in match]
    dep_line= seis_ev.index(''.join(dep_clue))
    ev_dep = seis_ev[dep_line].split()[1].zfill(3)
    mag_clue = [match for match in seis_ev if "Network magnitudes:" in match]
    phase_clue = [match for match in seis_ev if "Phase arrivals:" in match]
    mag_lines = seis_ev.index(''.join(mag_clue)) + 1
    phase_line = seis_ev.index(''.join(phase_clue)) - 1
    mags_list = seis_ev[mag_lines:phase_line]
    mag_pref = [match for match in mags_list if "preferred" in match]
    pref_mag_line = seis_ev.index(''.join(mag_pref))
    ev_mag = ' '.join(seis_ev[pref_mag_line].split()[0:2])
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
    
    dist_town_ev = str(towns_distance()[0][0]) + ' km'
    bear_town_ev = str(towns_distance()[0][1])
    town_ev = towns_distance()[0][2].title()
    ev_loc = ev_latlon + ' - ' + dist_town_ev + ' ' + bear_town_ev + ' of ' + town_ev
    
    issuedBy = str(self.tboxInitials.text())
    EqInfo_folder = 'Earthquake_Information\\' + ev_year + '_Earthquake_Information\\' + ev_month + '\\' + ev_day
    if not os.path.exists(EqInfo_folder):
        os.makedirs(EqInfo_folder)
    EqInfo = open(EqInfo_folder + '/' + ev_filename_final, 'w',encoding="utf8", errors='ignore')
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
    webbrowser.open('file:\\\\' + mainDir + '\\' + EqInfo_folder + '\\' + ev_filename_final, new=2)

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


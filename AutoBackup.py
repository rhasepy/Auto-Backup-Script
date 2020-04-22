"""
* AutoBackup v1.0
*
* [[ PYTHON3 REQUIRED ]]
*
* This program backups the given directory and 
* sends the zipped backup file to given mail account.
* This program runs with 2 modes, Auto Mode and Manual Mode
* 
* In Auto Mode, Program backups the per given minute, 
* if files in the directory are modified.
* In Manual Mode, Program waits user inputs to backup the file.
* 
* example run ;
* python3 AutoBackup.py -- from from@gmail.com --to target@gmail.com -- path /home/user/Desktop/folder/ -- check 60
*
*
* Goktug AKIN
*
*
"""

import shutil
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
from getpass import getpass
import optparse
import os
from os import listdir
from os.path import isfile, join
from os import system,name
import time
from threading import Thread
import sys

# CONSTANST

DEFAULT_ARCHIVE_FORMAT = "zip"

# command line arguments
fromaddr = ""
toaddr = ""
inputpath = ""
checktime = 30

# default zipname
zipname = "backup"

# logged in flag
logged_in = False

# last backup time
last_backup_time = 0

# local functions

def clear(): 
  
	# for windows 
	if name == 'nt': 
		_ = system('cls') 
  
	else: 
		_ = system('clear') 

def print_status():
	print("")
	print(">> Account : " + fromaddr)
	print(">> Target addres : " + toaddr)
	if logged_in is True:
		print(">> Status : Online")
	else:
		print(">> Status : Offline")
	print(">> Input directory : " + inputpath)
	print(">> Scanner time : " + str(checktime) + " minutes.")

def progress(message):
	i = 0
	while True:
		if logged_in is True:
			return
		dots = ""
		i = (i % 3) + 1
		dots += "." * i + " " * (3 - i)
		sys.stdout.write("\r{}".format(message + dots))
		sys.stdout.flush()
		i += 1
		time.sleep(0.3)

def parse_args():

	global fromaddr,toaddr,inputpath,checktime

	parser = optparse.OptionParser()
	parser.add_option('-f', '--from',
		action="store", dest="fromaddr",
		help="from string")
	parser.add_option('-t', '--to',
		action="store", dest="toaddr",
		help="to string")
	parser.add_option('-p', '--path',
		action="store", dest="path",
		help="path string")
	parser.add_option('-c', '--check',
		action="store", dest="check",
		help="check string")

	options, args = parser.parse_args()

	fromaddr = options.fromaddr
	toaddr = options.toaddr
	inputpath = options.path
	
	if options.check is not None:
		checktime = int(options.check)

	if checktime < 1:
		print("Invalid input for checktime argument.\nexit.")
		exit()
	
	if fromaddr is None:
		print("Ivalid input for fromaddr argument.\nexit.")
		exit()
	if toaddr is None:
		print("Ivalid input for toaddr argument.\nexit.")
		exit()
	if inputpath is None:
		print("Ivalid input for inputpath argument.\nexit.")
		exit()


def check_files(all_files):
	global checktime
	for file in all_files:
		# get modification time of file
		stat = os.path.getmtime(inputpath + allfiles[0])
		# 30 minutes past 
		if stat > last_backup_time:
			if time.time() > last_backup_time + checktime :
				return True
	return False

def create_archive(dir_name,output_filename,arch_format):
	shutil.make_archive(output_filename, arch_format, dir_name)


def login_test(fromaddr,password):
	global logged_in
	try:
		# creates SMTP session 
		s = smtplib.SMTP('smtp.gmail.com', 587) 
		  
		# start TLS for security 
		s.starttls() 

		time.sleep(2)
		  
		# Authentication 
		s.login(fromaddr, password) 
	except smtplib.SMTPAuthenticationError:
		print("Authentication failure! Invalid username or password.")
		os._exit(0)
	logged_in = True;
	# terminating the session 
	s.quit() 
	return
	
def send_file(fromaddr,toaddr,usr_password,file_name):
  
	# instance of MIMEMultipart 
	msg = MIMEMultipart() 
	  
	# storing the senders email address   
	msg['From'] = fromaddr 
	  
	# storing the receivers email address  
	msg['To'] = toaddr 
	  
	# storing the subject  
	msg['Subject'] = "File backuped"
	  
	# string to store the body of the mail 
	body = "File backuped"
	  
	# attach the body with the msg instance 
	msg.attach(MIMEText(body, 'plain')) 
	  
	# open the file to be sent  
	filename = file_name
	attachment = open(filename, "rb") 
	  
	# instance of MIMEBase and named as p 
	p = MIMEBase('application', 'octet-stream') 
	  
	# To change the payload into encoded form 
	p.set_payload((attachment).read()) 
	  
	# encode into base64 
	encoders.encode_base64(p) 
	   
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
	  
	# attach the instance 'p' to instance 'msg' 
	msg.attach(p) 
	  
	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	  
	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login(fromaddr, usr_password) 
	  
	# Converts the Multipart msg into a string 
	text = msg.as_string() 
	  
	# sending the mail 
	s.sendmail(fromaddr, toaddr, text) 
	  
	# terminating the session 
	s.quit() 

def manual():
	print(">> Mode : Manual")
	print(">> Enter \"send\" to send backup")
	print(">> Enter \"clear\" to clear the prompt\n")
	while(True):
		inputdummy = input()
		if inputdummy ==  'send':
			create_archive(inputpath,zipname,DEFAULT_ARCHIVE_FORMAT)
			time.sleep(2)
			send_file(fromaddr,toaddr,usrpassword,zipname+"."+DEFAULT_ARCHIVE_FORMAT)
			last_backup_time = time.time()
		elif inputdummy == 'clear':
			clear()
			print("#########################################################################")
			print("# AutoBackup v1                                                         #")
			print("# This program backups the given directory in auto mode or manual mode. #")
			print("#########################################################################")
			print(">> Enter \"send\" to send backup")
			print(">> Enter \"clear\" to clear the prompt\n")
		
def auto():
	# archive the folder initially and send it
	last_backup_time = time.time()
	create_archive(inputpath,zipname,DEFAULT_ARCHIVE_FORMAT)
	time.sleep(2)
	send_file(fromaddr,toaddr,usrpassword,zipname+"."+DEFAULT_ARCHIVE_FORMAT)
	last_backup_time = time.time()

	while(True):
		test = check_files(allfiles)
		if test is True:
			create_archive(inputpath,zipname,DEFAULT_ARCHIVE_FORMAT)
			time.sleep(2)
			send_file(fromaddr,toaddr,usrpassword,zipname+"."+DEFAULT_ARCHIVE_FORMAT)
			last_backup_time = time.time()
		time.sleep(checktime*60)


#################################################
################# START_MAIN ####################

print("")
print("#########################################################################")
print("# AutoBackup v1                                                         #")
print("# This program backups the given directory in auto mode or manual mode. #")
print("#########################################################################")
print(">> Use Ctrl-D or Ctrl-C to exit\n")

# parse command line arguments
parse_args()

# get all filenames from directory
allfiles = [f for f in listdir(inputpath) if isfile(join(inputpath, f))]

# get user password
usrpassword = getpass(">> Enter password for [" + fromaddr + "] : ")

# do login test
log_test = Thread(target=login_test,args = (fromaddr,usrpassword))
log_test.start()
progress(">> Logging in")
print("")
print(">> OK.")
log_test.join()

time.sleep(1)

print_status()
print("")
print("Select the backup mode : ")
print("1) Auto backup")
print("2) Manual backup")

select = input()
time.sleep(1)
clear()

print("")
print("#########################################################################")
print("# AutoBackup v1                                                         #")
print("# This program backups the given directory in auto mode or manual mode. #")
print("#########################################################################")

if select is '1':
	auto()
elif select is '2':
	manual()
else:
	print("Invalid choice")
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import *
from bs4 import BeautifulSoup
import os, json, random
import rom_list

def ua_open(urll):
	# Use browser proxy to parse web pages
	# Borrow random number generation function, randomly select the browser UA
	# (Win10+Chrome、MacOS+Safari、Win7+Opera、MacOS+Firefox)
	random_number = random.randint(1,4)
	if random_number == 1:
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
	elif random_number == 2:
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
	elif random_number == 3:
		headers = {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}
	elif random_number == 4:
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'}
	req = Request(url=urll, headers=headers)
	try:
		html = urlopen(req).read()
	except:
		return False
	return html

def de_open(urll):
	# The general method of parsing the page
	try:
		html = urlopen(urll)
	except:
		return False
	return html

def get_bs(urll):
	# Check if webpage parsing is successful or False if the parsing fails
	if urll == False:
		return False
	# Get beautifulSoup for the source of the page, set the return parameters to avoid unnecessary anomalies
	try:
		# The best use of the default:lxml
		bsObj = BeautifulSoup(urll,"lxml")
		# Parsing methods other than using the lxml library:
		# Use Python standard library 
		# (not recommended, will lead to some webpage parsing exception)
		#~ bsObj = BeautifulSoup(urll,"html.parser")
		# Use html5lib	
		#~ bsObj = BeautifulSoup(urll,"html5lib")
	except:
		return False
	return bsObj

def open_failed(name):
	# Output web page access failed message
	print("\n%s:"%(get_rom_name(name)))
	print("\n*** Access failed or request timeout!")

def analyze_failed(name):
	# Output page parsing error message
	print("\n%s:"%(get_rom_name(name)))
	print("\n*** Parsing failed! Please tell the author to fix this error!")

def os_clear_screen(ostype):
	if ostype == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def get_md5_from_file(urll):
	# Download MD5 verification file, 
	# read & return MD5 value and delete verification file.
	try:
		urlretrieve(urll,"tempfile")
	except:
		fmd5 = "Failed to get!"
	else:
		try:
			with open("tempfile") as md5file:
				fmd5 = md5file.read()
			os.remove("tempfile")
			fmd5 = fmd5.split(" ")[0]
		except:
			fmd5 = "Failed to get!"
	return fmd5

def get_rom_name(name):
	# According to the dictionary, get the project name by the function name identifier
	roms = rom_list.Rom_List()
	for lists in [roms.rom8_list, roms.rom7_list, roms.rom6_list, roms.other_list]:
		for key,value in lists.items():
			if key == name:
				return value
	return "Unknown item"

def out_put(fast_flag, name, fversion, build_info):
	# Output check results
	print_info = []
	while True:
		print_info.append(None)
		if len(print_info) >= 11:
			break
	print_info[0] = "\n%s:"%get_rom_name(name)
	print_info[1] = "\n=== The latest version:\n\n    " + fversion
	for key, value in build_info.items():
		if key == "build_type":
			print_info[2] = "\n=== Build type:\n\n    " + value
		elif key == "build_version":
			print_info[3] = "\n=== Build version:\n\n    " + value
		elif key == "fdate":
			print_info[4] = "\n=== Updated:\n\n    " + value
		elif key == "update_log":
			print_info[5] = "\n=== Changelog:\n\n    " + value
		elif key == "fmd5":
			print_info[6] = "\n=== MD5:\n\n    " + value
		elif key == "fsha256":
			print_info[7] = "\n=== sha256:\n\n    " + value
		elif key == "fsha1":
			print_info[8] = "\n=== sha1:\n\n    " + value
		elif key == "flink":
			print_info[9] = "\n=== Download link:\n\n    " + value
		elif key == "fsize":
			print_info[10] = "\n=== Size:\n\n    " + value
	for info in print_info:
		if info == None:
			continue
		print(info)
	# After output, update the dictionary
	saved = None
	if fast_flag == False:
		saved = read_from_json("save.json")
	saved = saved_update(get_rom_name(name), fversion, saved)
	return saved

def check_for_update(checked, temp2):
	# Check whether the project has been updated, 
	# If there is an update, the output prompt.
	saved = read_from_json("save.json")
	names = None
	# Special
	if checked == "miui_c":
		names = ("MIUI China Stable ROM","MIUI China Developer ROM")
	elif checked == "miui_g":
		names = ("MIUI Global Stable ROM","MIUI Global Developer ROM")
	elif checked == "miui_mr":
		names = ("MIUI MultiRom China Developer ROM","MIUI MultiRom Global Developer ROM")
	elif checked == "miui_pl":
		name = "MIUI Poland Developer ROM"
	# Normal
	else:
		name = get_rom_name(checked)
	if saved:
		if names:
			more_update_flag = False
			for name in names:
				if name in saved:
					if saved[name] != temp2[name]:
						print_update_info(name, saved[name], temp2[name])
						more_update_flag = True
			return more_update_flag
		else:
			if name in saved:
				if saved[name] != temp2[name]:
					print_update_info(name, saved[name], temp2[name])
					return True
	return False

def print_update_info(name, old_name, new_name):
	# Output update information
	print("")
	print("*" * 100)
	print("")
	print("=== %s updated! Hurry to tell your friends :P"%(name))
	print("")
	print("=== Old version: " + old_name)
	print("")
	print("=== New version: " + new_name)

def saved_update(name, version, saved):
	# Update dictionary
	# If the dictionary does not exist, create a new one
	if not saved:
		saved = {}
	saved[name]=version
	return saved

def save_to_json(ready_save_data, filename):
	# Save the dictionary to json
	with open(filename,'w') as savefile:
		json.dump(ready_save_data, savefile, sort_keys=True, indent=4, ensure_ascii=False)

def read_from_json(filename):
	# Read dictionary from json
	try:
		with open(filename,'r') as savefile:
			json_saved = json.load(savefile)
	except:
		try:
			# If the json file is broken or can not read properly, 
			# try removing it and return None.
			os.remove(filename)
		except FileNotFoundError:
			return None
		return None
	return json_saved

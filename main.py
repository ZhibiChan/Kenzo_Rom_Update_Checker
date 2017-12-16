#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, socket, platform
import check_update, rom_list, tools

# TEST FUNCTION
# ~ check_update.twrp(fast_flag = False)
# ~ sys.exit()
# TEST END

''' Check OS, this program support Windows & Linux now '''
sysstr = platform.system()
if sysstr not in ("Windows", "Linux"):
	print("\nFailed to run this program!")
	print("\nNot support your OS!")
	sys.exit()

''' Check Python version '''
if (sys.version.split(".")[0] != "3") \
		or (int(sys.version.split(".")[1]) < 5):
	print("\nFailed to run this program!")
	print("\nRunning this program requires a Python 3.5+ version")

''' Initialization parameters '''
# Tools version
tool_version = "v1.0.3 Alpha"
# Connection timeout(Default 20s)
socket.setdefaulttimeout(20)
# Import Rom List Dictionary
roms = rom_list.Rom_List()
# Define a range of numbers
r8_s = 1		;r8_e = len(roms.rom8_list)
r7_s = r8_e + 1	;r7_e = len(roms.rom7_list) + r8_e
r6_s = r7_e + 1	;r6_e = len(roms.rom6_list) + r7_e
r5_s = r6_e + 1	;r5_e = len(roms.check_list)
if sysstr == "Windows":
	''' Set the terminal for Win OS '''
	# Set the title
	title = "title KENZO ROM UPDATE CHECKER " + tool_version
	os.system(title)
	# Set the size
	term_lines = 38
	term_cols = 138
	hex_lines = hex(term_lines).replace("0x","").zfill(4)
	hex_cols = hex(term_cols).replace("0x","").zfill(4)
	set_terminal_size = \
	"reg add \"HKEY_CURRENT_USER\Console\" /t REG_DWORD /v WindowSize /d 0x"
	set_terminal_buffer = \
	"reg add \"HKEY_CURRENT_USER\Console\" /t REG_DWORD /v ScreenBufferSize /d 0x"
	os.system("%s%s%s /f >nul"%(set_terminal_size, hex_lines, hex_cols))
	os.system("%s%s%s /f >nul"%(set_terminal_buffer, "07d0", hex_cols))
else:
	''' Set the terminal for Linux OS '''
	term_cols = os.get_terminal_size().columns

def main():
	''' The main interface loop begins '''
	# Close all subdirectories
	r8 = r7 = r6 = r5 = False
	while True:
		# Main interface
		tools.os_clear_screen(sysstr)
		print("")
		print("======================================")
		print("     = KENZO ROM UPDATE CHECKER =")
		print("======================================")
		print("                             By: Pzqqt\n")
		print("*** Tool version: " + tool_version)
		print("")
		print("=== Rom List:")
		print("|")
		print("====①: Android 8.0")
		if r8:
			i = r8_s
			print("| |")
			for key in roms.rom8_list.keys():
				print("| ====%s.%s"%(i, roms.rom8_list[key]))
				i+=1
		print("|")
		print("====②: Android 7.x")
		if r7:
			i = r7_s
			print("| |")
			for key in roms.rom7_list.keys():
				print("| ====%s.%s"%(i, roms.rom7_list[key]))
				i+=1
		print("|")
		print("====③: Android 6.0")
		if r6:
			i = r6_s
			print("| |")
			for key in roms.rom6_list.keys():
				print("| ====%s.%s"%(i, roms.rom6_list[key]))
				i+=1
		print("|")
		print("====④: Other")
		if r5:
			i = r5_s
			print("  |")
			for key in roms.other_list.keys():
				print("  ====%s.%s"%(i, roms.other_list[key]))
				i+=1
		print("")
		# Start checking user input
		# Expand subdirectories
		selected = None
		if not(r8 or r7 or r6 or r5):
			print("*** Please enter the Rom type label you want to check and press Enter")
			print("")
			selected = input('*** (Enter \'e\' to exit, enter \'9999\' to automatically check all): ')
			# Check quit
			if selected == "e" or selected == "E":
				break
			# Check input
			if selected == "1":
				r8 = True
			if selected == "2":
				r7 = True
			if selected == "3":
				r6 = True
			if selected == "4":
				r5 = True
			if selected == "9999":
				check_all_auto()
			continue
		# After the subdirectory expands
		print("*** Please enter the Rom number you need to check and press Enter")
		print("")
		selected = input('*** (Enter \'0\' to close the sub-directory, enter \'e\' to exit): ')
		# Check quit
		if selected == "e" or selected == "E":
			break
		# Check close the subdirectory
		if selected == "0":
			r8 = r7 = r6 = r5 = False
			continue
		# Check the input
		try:
			selected_number = int(selected)
		except ValueError:
			continue
		if r8:
			if selected_number < r8_s or selected_number > r8_e:
				continue
		if r7:
			if selected_number < r7_s or selected_number > r7_e:
				continue
		if r6:
			if selected_number < r6_s or selected_number > r6_e:
				continue
		if r5:
			if selected_number < r5_s or selected_number > r5_e:
				continue
		# User input check completed
		# Start check for updates
		tools.os_clear_screen(sysstr)
		check_one(selected)
		# Return or exit
		temp = input('*** Enter \'e\' to exit, enter other to return to the main interface: ')
		if temp == "e" or temp == "E":
			break
		continue

def check_one(selected):
	# Check a single item
	print("")
	print("=== Checking now, results will be shown below...")
	print("")
	print("*" * term_cols)
	checking = "check_update." + roms.check_list[selected]
	temp2 = eval(checking)(fast_flag = False)
	if temp2:
		# Get the function name identifier
		checked = roms.check_list[selected]
		# Judge whether Rom is updated
		tools.check_for_update(checked, temp2)
		# Save the new dictionary to json
		tools.save_to_json(temp2, "save.json")
	print("")
	print("*" * term_cols)
	print("")
	if temp2:
		print("=== Check completed!")
	else:
		print("=== Check Failed!")
	print("")

def check_all_auto():
	# Automatically check the mode
	'''
	This mode does not perform the operation of downloading the MD5 file 
	to obtain the hash check value (fast_flag is True) to improve the checking speed.
	(Will not block the checksum that can be taken directly from the page)
	'''
	# Read saved Rom update status dictionary from json file
	saved = tools.read_from_json("save.json")
	# If failed to read the dictionary, create a new one
	if not saved:
		saved = {}
	# ~ Some URLs are not accessible right now (At least in my area is like this).
	# ~ such as: aex, aosip
	# ~ But I will not ignore them anymore.
	# ~ If you don't want to output these check failure messages after each auto check,
	# ~ Please write the corresponding function name in this tuple.
	skip_tuple = ("mokee")
	# Temporary dictionary, do not write json after each check. 
	# After all the checks, then update the json dictionary and write.
	temp3 = {}
	# Create a new dictionary, used to save the check failed items
	failed_list = {}
	j = 1
	check_2nd = ""
	while True:
		tools.os_clear_screen(sysstr)
		print("")
		print("=== Automatically check all Rom updates, please wait...")
		print("")
		print("=== Checking %s of %s %s..." %(j, len(roms.check_list), check_2nd))
		print("")
		print("*" * term_cols)
		checking = "check_update." + roms.check_list[str(j)]
		temp2 = eval(checking)(fast_flag = True)
		if temp2:
			# Get the function name identifier
			checked = roms.check_list[str(j)]
			# Judge whether Rom is updated
			new_flag = tools.check_for_update(checked, temp2)
			# Update the temporary dictionary 
			# (this method of merging dictionaries is limited to Python version 3.5 and above)
			temp3 = {**temp3, **temp2}
			#~ # Other ways of merging dictionaries:
			#~ # 1.Dictionary analysis (the most stupid, the slowest, most reliable method):
			#~ for key,value in temp2.items():
				#~ temp3[key] = value
			#~ # 2.element stitching (Python3 version can not be omitted "dictionary to list" step):
			#~ temp3 = dict(list(temp3.items()) + list(temp2.items()))
		elif roms.check_list[str(j)] not in skip_tuple:
			if check_2nd == "(Second check)":
				failed_list[j] = roms.check_list[str(j)]
			else:
				check_2nd = "(Second check)"
				continue
		check_2nd = ""
		j+=1
		if new_flag:
			print("")
			print("*" * term_cols)
			print("")
			input('*** Press the Enter key to continue: ')
		new_flag = False
		if j > len(roms.check_list):
			# Update temporary dictionary to json dictionary
			saved = {**saved, **temp3}
			# Write json dictionary to json
			tools.save_to_json(saved, "save.json")
			tools.os_clear_screen(sysstr)
			print("")
			print("*" * term_cols)
			print("")
			print("=== Check completed!")
			print("")
			if len(failed_list) != 0:
				print("*** Check failed items:")
				for key,value in failed_list.items():
					print("\n*** === %s. %s"%(key, tools.get_rom_name(value)))
				print("")
			else:
				print("=== No error occurred during the check.\n")
			input('*** Press the Enter key to return to the main interface: ')
			break

# Start the main interface loop
main()
# After jumping out of circulation, clear the screen and exit the program
tools.os_clear_screen(sysstr)
sys.exit()

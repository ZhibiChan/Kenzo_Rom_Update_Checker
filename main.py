#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, socket, platform
import check_update, rom_list, tools

# TEST FUNCTION
# ~ check_update.twrp(fast_flag = False)
# ~ sys.exit()
# TEST END

''' Check OS '''
sysstr = platform.system()
if sysstr not in ("Windows", "Linux"):
	print("\nFailed to run this program!")
	print("\nNot support your OS!")
	sys.exit()
''' Check BS4 parser'''
bs4_parser = tools.select_bs4_parser()
if bs4_parser == None:
	print("\nFailed to run this program!")
	print("\nPlease install at least one parser " +
			"in \"lxml\" and \"html5lib\"!")
	sys.exit()
''' Initialization parameters '''
# Tools version
tool_version = "v1.0.7 Test"
# Connection timeout(Default 20s)
socket.setdefaulttimeout(20)
# Import Rom List dict
roms = rom_list.Rom_List()
# Define a range of numbers
r8_s = 1
r8_e = len(roms.rom8_list)
r7_s = r8_e + 1
r7_e = len(roms.rom7_list) + r8_e
r6_s = r7_e + 1
r6_e = len(roms.rom6_list) + r7_e
r5_s = r6_e + 1
r5_e = len(roms.check_list)
# Set terminal
if sysstr == "Windows":
	os.system("title KENZO ROM UPDATE CHECKER " + tool_version)
	term_lines = 38
	term_cols = 138
	hex_lines = hex(term_lines).replace("0x","").zfill(4)
	hex_cols = hex(term_cols).replace("0x","").zfill(4)
	set_terminal_size = \
		("reg add \"HKEY_CURRENT_USER\Console\" /t REG_DWORD /v "
		"WindowSize /d 0x")
	set_terminal_buffer = \
		("reg add \"HKEY_CURRENT_USER\Console\" /t REG_DWORD /v "
		"ScreenBufferSize /d 0x")
	os.system("%s%s%s /f >nul"%(set_terminal_size, hex_lines, hex_cols))
	os.system("%s%s%s /f >nul"%(set_terminal_buffer, "07d0", hex_cols))
else:
	term_cols = os.get_terminal_size().columns

def main():
	''' The main interface loop begins '''
	# Close all subdirectories
	r8 = r7 = r6 = r5 = False
	while True:
		# Main interface
		tools.os_clear_screen(sysstr)
		print()
		print("======================================")
		print("     = KENZO ROM UPDATE CHECKER =")
		print("======================================")
		print("                             By: Pzqqt")
		print("# Tool version : " + tool_version)
		print("#  BS4 parser  : " + bs4_parser)
		print()
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
		print()
		selected = None
		if not(r8 or r7 or r6 or r5):
			print(
				"*** Please enter the Rom type label you "
				"want to check and press Enter\n")
			selected = input(
				"*** (Enter \"e\" to exit, "
				"enter \"9999\" to automatically check all): ")
			if selected == "e" or selected == "E":
				break
			elif selected == "1":
				r8 = True
			elif selected == "2":
				r7 = True
			elif selected == "3":
				r6 = True
			elif selected == "4":
				r5 = True
			elif selected == "9999":
				check_all_auto()
			continue
		print(
			"*** Please enter the Rom number you need "
			"to check and press Enter\n")
		selected = input(
			"*** (Enter \"0\" to close the sub-directory, "
			"enter \"e\" to exit): ")
		if selected == "e" or selected == "E":
			break
		if selected == "0":
			r8 = r7 = r6 = r5 = False
			continue
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
		while True:
			temp, failed_flag = check_one(selected, False)
			if temp != "0" or not failed_flag:
				break
		if temp == "e" or temp == "E":
			break
		continue

def check_one(selected, auto_flag):
	# Check a single item
	tools.os_clear_screen(sysstr)
	print(
		"\n=== Checking now, results will be shown below...\n\n"
		+ "*" * term_cols)
	checking = "check_update." + roms.check_list[selected]
	temp2 = eval(checking)(False, bs4_parser)
	if temp2:
		checked = roms.check_list[selected]
		tools.check_for_update(checked, temp2, term_cols)
		tools.save_to_json(temp2, "save.json")
	print("\n%s\n"%("*" * term_cols))
	if temp2:
		print("=== Check completed!")
		check_2nd = ""
	else:
		print("=== Check Failed!")
		check_2nd = "\"0\" to try again, enter "
	print()
	if auto_flag:
		input("*** Press the Enter key to continue: ")
		return None
	else:
		return input(
			"*** Enter %s\"e\" to exit, "
			"enter other to return to the main interface: "
			%check_2nd), check_2nd

def check_all_auto():
	# Automatically check all
	'''
	This mode does not perform the operation of downloading the MD5 file 
	to obtain the hash check value (fast_flag is True) 
	to improve the checking speed.
	(Will not block the hash that can be taken directly from the page)
	'''
	# Read saved Rom update status dictionary from json file
	saved = tools.read_from_json("save.json")
	if not saved:
		saved = {}
	# ~ Some URLs are not accessible right now 
	# ~ (At least in my area is like this).
	# ~ such as: aex
	# ~ But I will not ignore them anymore.
	# ~ If you don't want to output these check failure messages,
	# ~ Please write the corresponding function name in this tuple.
	skip_tuple = ("mokee")
	temp3 = failed_list = {}
	j = 1
	check_2nd = ""
	while True:
		tools.os_clear_screen(sysstr)
		print("\n=== Automatically check all Rom updates, "
				"please wait...")
		print("\n=== Checking %s of %s %s..." 
				%(j, len(roms.check_list), check_2nd))
		print("\n" + "*" * term_cols)
		new_flag = False
		checking = "check_update." + roms.check_list[str(j)]
		temp2 = eval(checking)(True, bs4_parser)
		if temp2:
			checked = roms.check_list[str(j)]
			new_flag = tools.check_for_update(checked, temp2, term_cols)
			# Merging dictionaries
			# (this method is limited to Python version 3.5 and above)
			temp3 = {**temp3, **temp2}
			# Other ways of :
			# 1.Dictionary analysis 
			# (the most stupid, the slowest, most reliable method):
			# ~ for key,value in temp2.items():
				# ~ temp3[key] = value
			# 2.element stitching 
			# (Python3 can not be omitted "dictionary to list" step):
			# ~ temp3 = dict(list(temp3.items()) + list(temp2.items()))
		elif roms.check_list[str(j)] not in skip_tuple:
			if check_2nd == "(Second check)":
				failed_list[j] = roms.check_list[str(j)]
			else:
				check_2nd = "(Second check)"
				continue
		check_2nd = ""
		if new_flag:
			print("\n%s\n"%("*" * term_cols))
			temp = input(
				"*** Enter \"0\" to view details, "
				"enter other to continue: ")
			if temp == "0":
				check_one(str(j), True)
		j+=1
		if j > len(roms.check_list):
			saved = {**saved, **temp3}
			tools.save_to_json(saved, "save.json")
			tools.os_clear_screen(sysstr)
			print("\n%s\n"%("*" * term_cols))
			print("=== Check completed!\n")
			if len(failed_list) != 0:
				print("*** Check failed items:")
				for key,value in failed_list.items():
					print("\n*** === %s. %s"
						%(key, tools.get_rom_name(value)))
				print()
			else:
				print("=== No error occurred during the check.\n")
			input("*** Press the Enter key to "
				"return to the main interface: ")
			break

main()
tools.os_clear_screen(sysstr)
sys.exit()

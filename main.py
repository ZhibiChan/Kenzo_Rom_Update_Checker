#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import socket
import platform

import check_update
import rom_list
import tools

# TEST FUNCTION
# ~ check_update.atomic(False, "lxml")
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
    print("\nPlease install at least one parser "
          "in \"lxml\" and \"html5lib\"!")
    sys.exit()

''' Initialization parameters '''
# Tools version
tool_version = "v1.0.7 Test"
# Connection timeout(Default 20s)
socket.setdefaulttimeout(20)
# Import Rom List dict
roms = rom_list.Rom_List()
# Set terminal
if sysstr == "Windows":
    os.system("title KENZO ROM UPDATE CHECKER " + tool_version)
    term_lines = 41
    term_cols = 138
    hex_lines = hex(term_lines).replace("0x","").zfill(4)
    hex_cols = hex(term_cols).replace("0x","").zfill(4)
    set_terminal_size = ("reg add \"HKEY_CURRENT_USER\Console\" /t "
                         "REG_DWORD /v WindowSize /d 0x")
    set_terminal_buffer = ("reg add \"HKEY_CURRENT_USER\Console\" /t "
                           "REG_DWORD /v ScreenBufferSize /d 0x")
    os.system("%s%s%s /f >nul"%(set_terminal_size, hex_lines, hex_cols))
    os.system("%s%s%s /f >nul"%(set_terminal_buffer, "07d0", hex_cols))
else:
    term_cols = os.get_terminal_size().columns

def main():
    ''' The main interface loop begins '''
    # Close all subdirectories
    r8 = r7 = r6 = r5 = False
    # Define a range of numbers
    r8_s = 1
    r8_e = len(roms.rom8_list)
    r7_s = r8_e + 1
    r7_e = len(roms.rom7_list) + r8_e
    r6_s = r7_e + 1
    r6_e = len(roms.rom6_list) + r7_e
    r5_s = r6_e + 1
    r5_e = len(roms.check_list)
    # Pre-generate Rom list for display
    no = 1
    print_r8 = print_r7 = print_r6 = "  | |\n"
    print_r5 = "    |\n"
    for key in roms.rom8_list.keys():
        print_r8+="  | ====%s.%s\n"%(no, roms.list_all[key])
        no+=1
    for key in roms.rom7_list.keys():
        print_r7+="  | ====%s.%s\n"%(no, roms.list_all[key])
        no+=1
    for key in roms.rom6_list.keys():
        print_r6+="  | ====%s.%s\n"%(no, roms.list_all[key])
        no+=1
    for key in roms.other_list.keys():
        print_r5+="    ====%s.%s\n"%(no, roms.list_all[key])
        no+=1
    # Main interface
    while True:
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
        print("  |")
        print("  ==== ①: Android 8.0")
        if r8:
            print(print_r8.rstrip())
        print("  |")
        print("  ==== ②: Android 7.x")
        if r7:
            print(print_r7.rstrip())
        print("  |")
        print("  ==== ③: Android 6.0")
        if r6:
            print(print_r6.rstrip())
        print("  |")
        print("  ==== ④: Other")
        if r5:
            print(print_r5.rstrip())
        if not(r8 or r7 or r6 or r5):
            print()
            print("=== Other options")
            print("  |")
            print("  ==== A : Automatically check all")
            print("  |")
            print("  ==== L : Show saved info")
            print("  |")
            print("  ==== X : Preview Kenzo's XDA development page")
            print("  |")
            print("  ==== E : Exit")
        print()
        selected = None
        if not(r8 or r7 or r6 or r5):
            selected = input("*** Please enter the "
                             "option and press Enter: ")
            if selected == "1":
                r8 = True
            elif selected == "2":
                r7 = True
            elif selected == "3":
                r6 = True
            elif selected == "4":
                r5 = True
            elif selected == "a" or selected == "A":
                check_all_auto()
            elif selected == "l" or selected == "L":
                tools.os_clear_screen(sysstr)
                show_info()
                input("*** Press the Enter key to "
                      "return to the main interface: ")
            elif selected == "x" or selected == "X":
                check_update.xda(bs4_parser, sysstr, term_cols)
            elif selected == "e" or selected == "E":
                break
            continue
        print("*** Please enter the Rom number you need "
              "to check and press Enter\n")
        selected = input("*** Enter \"0\" to close the sub-directory,"
                         " enter \"E\" to exit : ")
        if selected == "0":
            r8 = r7 = r6 = r5 = False
            continue
        elif selected == "e" or selected == "E":
            break
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
            temp, failed_flag = check_one(selected)
            if temp != "0" or not failed_flag:
                break

def check_one(selected, auto_flag = False, argv_flag = False):
    # Check a single item
    tools.os_clear_screen(sysstr)
    print("\n=== Checking now, results will be shown below...\n\n"
          + "*" * term_cols)
    if argv_flag:
        checking = "check_update." + selected
    else:
        checking = "check_update." + roms.check_list[selected]
    temp2 = eval(checking)(False, bs4_parser)
    if temp2:
        if argv_flag:
            checked = selected
        else:
            checked = roms.check_list[selected]
        tools.check_for_update(checked, temp2, term_cols)
        tools.save_to_json(temp2, "save.json")
    print("\n%s\n"%("*" * term_cols))
    if temp2:
        print("=== Check completed!")
        check_res = ("\n*** Press the Enter key ")
        exit_st = 0
    else:
        print("=== Check Failed!")
        check_res = ("\n*** Enter \"0\" to try again, enter other ")
        exit_st = 1
    if auto_flag:
        input("\n*** Press the Enter key to continue: ")
        return
    if argv_flag:
        return
    return input(check_res + "to return to the main interface: "), exit_st

def check_all_auto(argv_flag = False):
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
                failed_list[str(j)] = roms.check_list[str(j)]
            else:
                check_2nd = "(Second check)"
                continue
        check_2nd = ""
        if new_flag:
            print("\n%s\n"%("*" * term_cols))
            temp = input("*** Enter \"0\" to view details, "
                         "enter other to continue: ")
            if temp == "0":
                check_one(str(j), auto_flag = True)
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
                          %(key, roms.list_all[value]))
                print()
            else:
                print("=== No error occurred during the check.\n")
            if not argv_flag:
                input("*** Press the Enter key to "
                      "return to the main interface: ")
            break

def show_list():
    print("\nAvailable parameters:\n")
    for key in sorted(roms.list_all.keys()):
        print("    %s : %s"%(key.ljust(10), roms.list_all[key]))

def show_info():
    saved_info = tools.read_from_json("save.json")
    if not saved_info:
        print("\nRead \"save.json\" failed or no such file!\n")
        return
    print("\nSaved info:\n")
    if term_cols >= 120:
        for key, value in saved_info.items():
            print("    %s : %s"%(key.ljust(60), value))
        print()
    else:
        for key, value in saved_info.items():
            print("  %s :\n"%key + \
                  "      %s\n"%value)

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        main()
        tools.os_clear_screen(sysstr)
        sys.exit()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-a" or sys.argv[1] == "-A":
            check_all_auto(True)
            sys.exit()
        if sys.argv[1] == "-s" or sys.argv[1] == "-S":
            print("\nUsage: main.py -s <argv>")
            show_list()
            sys.exit()
        if sys.argv[1] == "-l" or sys.argv[1] == "-L":
            show_info()
            sys.exit()
        if sys.argv[1] == "-x" or sys.argv[1] == "-X":
            check_update.xda(bs4_parser, sysstr, term_cols)
            tools.os_clear_screen(sysstr)
            sys.exit()
    elif len(sys.argv) == 3:
        if sys.argv[1] == "-s" or sys.argv[1] == "-S":
            if sys.argv[2] in roms.check_list.values():
                check_one(sys.argv[2], argv_flag = True)
                sys.exit()
            else:
                print("\nIncorrect parameter!")
                show_list()
                sys.exit()
    print()
    print("Kenzo Rom Update Checker " + tool_version)
    print()
    print("Usage: main.py [<command>] [<argv>]")
    print()
    print("Available commands:")
    print("  None         Goto main interface")
    print("  -a           Automatically check all Rom updates")
    print("  -s <argv>    Check a single item")
    print("  -l           Show saved info")
    print("  -x           Preview Kenzo's XDA development page")
    sys.exit()

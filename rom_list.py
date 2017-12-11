#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rom_List:
	# A class that holds a Rom list dictionary
	def __init__(self):
		# Build a dictionary list of sequence numbers and function names
		self.check_list = {
			"1":"aoscp",
			"2":"cardinal",
			"3":"nos_o",
			"4":"aex",
			"5":"aicp",
			"6":"aosip",
			"7":"bliss",
			"8":"cosmicos",
			"9":"dotos",
			"10":"los",
			"11":"los_mg",
			"12":"los_u1",
			"13":"mokee",
			"14":"nos_s",
			"15":"omni",
			"16":"rr",
			"17":"sudamod",
			"18":"viperos",
			"19":"xenonhd",
			"20":"flyme",
			"21":"miui_c",
			"22":"miui_g",
			"23":"miui_mr",
			"24":"miui_pl",
			"25":"miui_br",
			"26":"twrp"
		}
		# Build a dictionary list of function names and project names
		# Android 8.0:
		self.rom8_list = {
			"aoscp":"AOSCP Unofficial",
			"cardinal":"Cardinal AOSP Official Test",
			"nos_o":"Nitrogen OS 8.1 Test"
		}
		# Android 7.x:
		self.rom7_list = {
			"aex":"AospExtended Official",
			"aicp":"AICP Official",
			"aosip":"AOSiP Official",
			"bliss":"Bliss Official",
			"cosmicos":"Cosmic OS Official",
			"dotos":"DotOS Official",
			"los":"LineageOS Official",
			"los_mg":"LineageOS for MicroG Unofficial",
			"los_u1":"LineageOS 14.1 Unofficial(By Umang96)",
			"mokee":"Mokee Official Nightly",
			"nos_s":"Nitrogen OS Official Stable",
			"omni":"Omni Official",
			"rr":"Resurrection Remix OS Official",
			"sudamod":"SudaMod Official",
			"viperos":"ViperOS Official",
			"xenonhd":"XenonHD Official"
		}
		# Android 6.0:
		self.rom6_list = {
			"flyme":"Flyme Official(haohao3344)",
			"miui_c":"MIUI China",
			"miui_g":"MIUI Global",
			"miui_mr":"MIUI MultiRom Developer ROM",
			"miui_pl":"MIUI Poland Developer ROM",
			"miui_br":"MIUI Brazil Developer ROM"
		}
		# Other:
		self.other_list = {
			"twrp":"TWRP Official"
		}

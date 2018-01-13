#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rom_List:
	def __init__(self):
		roms_list = [
			"aex_sf",
			"aoscp",
			"cardinal",
			"cosmicos",
			"nos_o",
			"pe_u1",
			"pe_u2s",
			"pe_u2b",
			"aex",
			"aicp",
			"aosip",
			"bliss",
			"dotos",
			"los",
			"los_mg",
			"los_u1",
			"mokee",
			"nos_s",
			"omni",
			"rr",
			"sudamod",
			"viperos",
			"xenonhd",
			"flyme",
			"miui_br",
			"miui_c",
			"miui_g",
			"miui_mr",
			"miui_pl",
			"twrp"
		]
		self.check_list = {}
		i = 1
		for item in roms_list:
			self.check_list[str(i)] = item
			i+=1
		
		self.rom8_list = {
			"aex_sf":"AospExtended Oreo Official",
			"aoscp":"AOSCP Official",
			"cardinal":"Cardinal AOSP Official Test",
			"cosmicos":"Cosmic OS Official",
			"nos_o":"Nitrogen OS 8.1 Test",
			"pe_u1":"Pixel Experience (Unofficial By irvin16, miguelndecarval)",
			"pe_u2s":"Pixel Experience Stable (Unofficial By irvin16)",
			"pe_u2b":"Pixel Experience Beta (Unofficial By irvin16)"
		}
		self.rom7_list = {
			"aex":"AospExtended Official",
			"aicp":"AICP Official",
			"aosip":"AOSiP Official",
			"bliss":"Bliss Official",
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
		self.rom6_list = {
			"flyme":"Flyme Official(haohao3344)",
			"miui_br":"MIUI Brazil Developer ROM",
			"miui_c":"MIUI China",
			"miui_g":"MIUI Global",
			"miui_mr":"MIUI MultiRom Developer ROM",
			"miui_pl":"MIUI Poland Developer ROM"
		}
		self.other_list = {
			"twrp":"TWRP Official"
		}

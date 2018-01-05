#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rom_List:
	def __init__(self):
		roms_list = [
			"aex_sf",
			"aoscp",
			"aoscp_u1",
			"cardinal",
			"nos_o",
			"pe",
			"aex",
			"aicp",
			"aosip",
			"bliss",
			"cosmicos",
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
			"aoscp_u1":"AOSCP Unofficial By Aashiq Jacob",
			"cardinal":"Cardinal AOSP Official Test",
			"nos_o":"Nitrogen OS 8.1 Test",
			"pe":"Pixel Experience"
		}
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

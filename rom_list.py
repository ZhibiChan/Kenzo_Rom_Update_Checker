#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rom_List:
	# 一个保存Rom列表字典的类
	def __init__(self):
		# 构建序号和函数名的字典列表
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
		# 构建函数名和项目名的字典列表
		# Android 8.0:
		self.rom8_list = {
			"aoscp":"AOSCP 非官方版",
			"cardinal":"Cardinal AOSP 官方测试版",
			"nos_o":"Nitrogen OS 8.1测试版"
		}
		# Android 7.x:
		self.rom7_list = {
			"aex":"AospExtended 官方版",
			"aicp":"AICP 官方版",
			"aosip":"AOSiP 官方版",
			"bliss":"Bliss 官方版",
			"cosmicos":"Cosmic OS 官方版",
			"dotos":"DotOS 官方版",
			"los":"LineageOS 官方版",
			"los_mg":"LineageOS for MicroG 非官方版",
			"los_u1":"LineageOS 14.1 非官方版(By Umang96)",
			"mokee":"Mokee 官方每夜版",
			"nos_s":"Nitrogen OS 官方稳定版",
			"omni":"Omni 官方版",
			"rr":"Resurrection Remix OS 官方版",
			"sudamod":"SudaMod 官方版",
			"viperos":"ViperOS 官方版",
			"xenonhd":"XenonHD 官方版"
		}
		# Android 6.0:
		self.rom6_list = {
			"flyme":"Flyme 官方版(haohao3344)",
			"miui_c":"MIUI 天朝版",
			"miui_g":"MIUI 国际版",
			"miui_mr":"MIUI MultiRom 开发版",
			"miui_pl":"MIUI 波兰版 开发版",
			"miui_br":"MIUI 巴西版 开发版"
		}
		# Other:
		self.other_list = {
			"twrp":"TWRP 官方版"
		}

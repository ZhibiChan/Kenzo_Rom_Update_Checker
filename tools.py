#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import *
from bs4 import BeautifulSoup
import os, json, random
import rom_list

def ua_open(urll):
	# 使用浏览器代理解析网页
	# 借用随机数生成函数，随机选择浏览器UA标识（Win10+Chrome、MacOS+Safari、Win7+Opera、MacOS+Firefox）
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
	# 一般的方法解析网页
	try:
		html = urlopen(urll)
	except:
		return False
	return html

def get_bs(urll):
	# 检查网页解析是否成功，如果解析失败则直接返回False
	if urll == False:
		return False
	# 对网页源码获取BeautifulSoup，设置返回参数以规避不必要的异常
	try:
		# 默认使用效果最好的lxml
		bsObj = BeautifulSoup(urll,"lxml")
		# 除了使用lxml库之外的解析方法：
		# 使用Python标准库（不建议，会导致某些网页解析出现异常）
		#~ bsObj = BeautifulSoup(urll,"html.parser")
		# 使用html5lib	
		#~ bsObj = BeautifulSoup(urll,"html5lib")
	except:
		return False
	return bsObj

def open_failed():
	# 输出网页访问失败的信息
	print("\n访问失败或请求超时！")

def analyze_failed():
	# 输出网页解析出错的信息
	print("\n网页解析失败！请告知作者修正此错误！")

def get_md5_from_file(urll):
	# 下载MD5校验文件，读取&返回MD5值并删除校验文件
	try:
		urlretrieve(urll,"tempfile")
	except:
		fmd5 = "获取失败！"
	else:
		try:
			with open("tempfile") as md5file:
				fmd5 = md5file.read()
			os.remove("tempfile")
			fmd5 = fmd5.split(" ")
			fmd5 = fmd5[0]
		except:
			fmd5 = "获取失败！"
	return fmd5

def get_rom_name(name):
	# 依据字典，通过函数名标识获取项目名
	roms = rom_list.Rom_List()
	for lists in [roms.rom8_list, roms.rom7_list, roms.rom6_list, roms.other_list]:
		for key,value in lists.items():
			if key == name:
				return value
	return "未知的项目"

def out_put(fast_flag, name, fversion, build_type, build_version, fdate, update_log, fmd5, fsha256, fsha1, flink, fsize):
	# 检查结果输出打印到屏幕
	if name:
		print("\n%s："%(get_rom_name(name)))
	if fversion:
		print("\n当前最新版本：\n\n" + fversion)
	if build_type and build_version:
		print("\n构建类型 & 构建版本：\n\n%s\t%s"%(build_type, build_version))
	elif build_type:
		print("\n构建类型：\n\n" + build_type)
	if fdate:
		print("\n更新日期：\n\n" + fdate)
	if update_log:
		print("\n更新日志：\n\n" + update_log)
	if fmd5:
		print("\nMD5：\n\n" + fmd5)	
	if fsha256:
		print("\nsha256：\n\n" + fsha256)
	if fsha1:
		print("\nsha1：\n\n" + fsha1)
	if flink:
		print("\n下载链接：\n\n" + flink)
	if fsize:
		print("\n大小：\n\n" + fsize)
	# 打印结束后更新字典
	saved = None
	if fast_flag == False:
		saved = read_from_json("save.json")
	saved = saved_update(get_rom_name(name), fversion, saved)
	return saved

def check_for_update(checked, temp2):
	# 检查项目是否有更新，如有更新则输出提示
	saved = read_from_json("save.json")
	names = None
	# 特殊处理
	if checked == "miui_c":
		names = ("MIUI 天朝版 稳定版","MIUI 天朝版 开发版")
	elif checked == "miui_g":
		names = ("MIUI 国际版 稳定版","MIUI 国际版 开发版")
	elif checked == "miui_mr":
		names = ("MIUI MultiRom 开发版 天朝版","MIUI MultiRom 开发版 国际版")
	elif checked == "miui_pl":
		name = "MIUI 波兰版 开发版"
	# 普通处理
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
	# 打印输出更新信息
	print("")
	print("****************************************************************************************************")
	print("")
	print("=== %s 有更新了哟~快点去告诉你的小伙伴们吧！"%(name))
	print("")
	print("===旧版本：" + old_name)
	print("")
	print("===新版本：" + new_name)

def saved_update(name, version, saved):
	# 更新项目更新状态的字典
	# 如果字典不存在，就新建一个空的字典
	if not saved:
		saved = {}
	saved[name]=version
	return saved

def save_to_json(ready_save_data, filename):
	# 将字典保存到json
	with open(filename,'w') as savefile:
		json.dump(ready_save_data, savefile, sort_keys=True, indent=4, ensure_ascii=False)

def read_from_json(filename):
	# 从json中读取字典
	try:
		with open(filename,'r') as savefile:
			json_saved = json.load(savefile)
	except:
		try:
			# 如果json文件损坏了无法正常读取内容，就尝试删除它并返回None
			os.remove(filename)
		except FileNotFoundError:
			return None
		return None
	return json_saved

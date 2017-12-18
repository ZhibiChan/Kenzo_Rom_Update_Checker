#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, time, re
from tools import *

def aex(fast_flag):
	name = "aex"
	build_info = {}
	ual = ua_open("https://downloads.aospextended.com/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"class":"cm"}).find("tbody").find("tr")
		i=0
		for child in nb.findAll("td")[1]:
			i+=1
			if i == 5:
				fsize=child
				continue
			if i == 7:
				fmd5=child
				break
		build_info['fsize'] = fsize.split(" ",3)[3]
		build_info['fmd5'] = fmd5.split(" ",2)[2]
		fversion = nb.findAll("td")[1].find("a").find("strong").get_text()
		build_info['fdate'] = nb.findAll("td")[2].find("strong").get_text().strip()
		build_info['flink'] = "https://downloads.aospextended.com" + nb.findAll("td")[1].find("a")["href"]
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def aicp(fast_flag):
	name = "aicp"
	build_info = {}
	ual = de_open("http://dwnld.aicp-rom.com/?device=kenzo")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"class":"table table-bordered table-striped"}).find("tbody").find("tr")
		build_info['build_type'] = nb.findAll("td")[1].get_text()
		build_info['fsize'] = nb.findAll("td")[3].get_text()
		build_info['update_log'] = nb.findAll("td")[2].findAll("a")[1]["href"]
		fversion = nb.findAll("td")[2].find("a").get_text()
		build_info['fdate'] = nb.findAll("td")[-1].get_text()
		fmd5_temp = nb.findAll("td")[2].find("small").get_text().split(":")[1]
		fmd5 = ""
		for char in fmd5_temp:
			if re.match('[0-9a-fA-F]',char):
				fmd5+=char
		build_info['fmd5'] = fmd5
		build_info['flink'] = nb.findAll("td")[2].find("a")["href"]
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def aoscp(fast_flag):
	name = "aoscp"
	build_info = {}
	ual = de_open("https://carvalho-server.no-ip.biz/?C=M;O=A")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"indexlist"}).findAll("tr")[-1]
		fversion = nb.findAll("td")[1].find("a").get_text()
		build_info['fdate'] = nb.findAll("td")[2].get_text()
		build_info['flink'] = "https://carvalho-server.no-ip.biz/" + nb.findAll("td")[1].find("a").get_text()
		build_info['fsize'] = nb.findAll("td")[3].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def aosip(fast_flag):
	name = "aosip"
	build_info = {}
	ual = de_open("https://get.aosiprom.com/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"id":"fallback"}).find("table").findAll("tr")[-2]
		if fast_flag == False:
			fmd5 = bsObj.find("div",{"id":"fallback"}).find("table") \
					.findAll("tr")[-1].findAll("td")[1].find("a")["href"]
			build_info['fmd5'] = get_md5_from_file("https://get.aosiprom.com" + fmd5)
		fversion = nb.findAll("td")[1].find("a").get_text()
		build_info['fdate'] = nb.findAll("td")[2].get_text()
		build_info['flink'] = "https://get.aosiprom.com" + nb.findAll("td")[1].find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[3].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def bliss(fast_flag):
	name = "bliss"
	build_info = {}
	ual = de_open("https://downloads.blissroms.com/Bliss/Official/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"id":"fallback"}).find("table").findAll("tr")[-3]
		if fast_flag == False:
			fmd5 = bsObj.find("div",{"id":"fallback"}).find("table") \
					.findAll("tr")[-2].findAll("td")[1].find("a")["href"]
			build_info['fmd5'] = get_md5_from_file("https://downloads.blissroms.com" + fmd5)
		build_info['fdate'] = nb.findAll("td")[2].get_text()
		fversion = nb.findAll("td")[1].find("a").get_text()
		build_info['flink'] = "https://downloads.blissroms.com" + nb.findAll("td")[1].find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[3].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def cardinal(fast_flag):
	name = "cardinal"
	build_info = {}
	ual = de_open("https://sourceforge.net/projects/cardinal-aosp/files/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[1]
		fversion = nb["title"]
		build_info['fdate'] = nb.find("td").find("abbr")["title"]
		build_info['flink'] = nb.find("th").find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[1].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def cosmicos(fast_flag):
	name = "cosmicos"
	build_info = {}
	ual = de_open("https://sourceforge.net/projects/cosmic-os/files/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[0]
		fversion = nb["title"]
		build_info['fdate'] = nb.find("td").find("abbr")["title"]
		build_info['flink'] = nb.find("th").find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[1].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def dotos(fast_flag):
	name = "dotos"
	build_info = {}
	ual = de_open("https://sourceforge.net/projects/dotos-ota/files/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[0]
		fversion = nb["title"]
		build_info['fdate'] = nb.find("td").find("abbr")["title"]
		build_info['flink'] = nb.find("th").find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[1].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def flyme(fast_flag):
	name = "flyme"
	build_info = {}
	ual = de_open("http://www.flyme.cn/firmwarelist-51.html")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"class":"wrap"}).find_next("script",{"type":"text/javascript"}) \
			.get_text().split("data=",1)[-1].replace(";","")
		# This magical command can convert strings to dictionaries.
		# By the way, Unicode encoding can be switched back to Chinese. Great!
		nb = json.loads(nb)
		# "0_1" point to haohao3344 version, "1_1" point to Pan's version.
		# The latter has stopped updating, so give up.
		nb = nb["0_1"]
		fversion = nb["name"]
		build_info['flink'] = nb["download"]
		build_info['fsize'] = nb["size"] + "MB"
		build_info['fdate'] = nb["time"]
		build_info['fmd5'] = nb["md5"]
		build_info['update_log'] = nb["log"].replace("\n","\n    ")
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def los(fast_flag):
	name = "los"
	build_info = {}
	ual = de_open("https://download.lineageos.org/kenzo")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"class":"striped bordered"}).find("tbody").find("tr")
		fversion = nb.findAll("td")[2].find("a").get_text()
		build_info['build_type'] = nb.findAll("td")[0].get_text()
		build_info['build_version'] = nb.findAll("td")[1].get_text()
		if fast_flag == False:
			build_info['fsha256'] = get_md5_from_file(nb.findAll("td")[2].find("a")["href"] + "?sha256")
			build_info['fsha1'] = get_md5_from_file(nb.findAll("td")[2].find("a")["href"] + "?sha1")
		build_info['fdate'] = nb.findAll("td")[-1].get_text()
		build_info['flink'] = nb.findAll("td")[2].find("a")["href"]
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def los_u1(fast_flag):
	name = "los_u1"
	build_info = {}
	ual = de_open("https://github.com/los-kenzo/downloads/blob/lk-7.1/README.md")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("article",{"class":"markdown-body entry-content"}).findAll("a")[2]
		build_info['update_log'] = bsObj.find("article",{"class":"markdown-body entry-content"}) \
					.findAll("ul")[0].get_text().replace("\n","\n    ")[5:-5]
		build_info['flink'] = nb["href"]
		fversion = nb.get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def los_mg(fast_flag):
	name = "los_mg"
	build_info = {}
	ual = de_open("https://download.lineage.microg.org/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"id":"fallback"}).find("table").findAll("tr")[-2]
		if fast_flag == False:
			fmd5 = bsObj.find("div",{"id":"fallback"}).find("table"). \
					findAll("tr")[-1].findAll("td")[1].find("a")["href"]
			build_info['fmd5'] = get_md5_from_file("https://download.lineage.microg.org" + fmd5)
		fversion = nb.findAll("td")[1].find("a").get_text()
		build_info['fdate'] = nb.findAll("td")[2].get_text()
		build_info['flink'] = "https://download.lineage.microg.org" + nb.findAll("td")[1].find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[3].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def miui_br(fast_flag):
	name = "miui_br"
	build_info = {}
	ual = ua_open("http://miuibrasil.org/downloads/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"id":"kenzo"}).find("div",{"class":"x-accordion-inner"}).find("a")
		build_info['flink'] = nb["href"]
		fversion = nb.get_text().split(" ")[-1]
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def miui_c(fast_flag):
	name = "miui_c"
	ual = de_open("http://www.miui.com/download-308.html")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb_s = bsObj.find("div",{"id":"content_t_451"}).find("div",{"class":"block"})
		nb_d = bsObj.find("div",{"id":"content_t_451"}).findAll("div",{"class":"block"})[1]
		flink1 = nb_s.find("div",{"class":"to_miroute"}).find("a")["href"]
		flink2 = nb_d.find("div",{"class":"to_miroute"}).find("a")["href"]
		fvalue1 = nb_s.find("div",{"class":"supports"}).find("p")
		fvalue2 = nb_d.find("div",{"class":"supports"}).find("p")
		i=0
		for child in fvalue1:
			i+=1
			if i == 3:
				fversion1=child
				continue
			if i == 5:
				fsize1=child
				break
		i=0
		for child in fvalue2:
			i+=1
			if i == 3:
				fversion2=child
				continue
			if i == 5:
				fsize2=child
				break
		fversion1 = fversion1.split("：")[1].strip()
		fversion2 = fversion2.split("：")[1].strip()
		fsize1 = fsize1.split("：")[1]
		fsize2 = fsize2.split("：")[1]
	except:
		return analyze_failed(name)
	print("")
	print("MIUI China:")
	print("")
	print("Stable ROM:")
	print("\n=== The latest version:\n\n    " + fversion1)
	print("\n=== Download link:\n\n    " + flink1)
	print("\n=== Size:\n\n    " + fsize1)
	print("")
	print("Developer ROM:")
	print("\n=== The latest version:\n\n    " + fversion2)
	print("\n=== Download link:\n\n    " + flink2)
	print("\n=== Size:\n\n    " + fsize2)
	saved = None
	if fast_flag == False:
		saved = read_from_json("save.json")
	saved = saved_update("MIUI China Stable ROM", fversion1, saved)
	saved = saved_update("MIUI China Developer ROM", fversion2, saved)
	return saved

def miui_g(fast_flag):
	name = "miui_g"
	ual = de_open("http://en.miui.com/download-301.html")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb_s = bsObj.find("div",{"id":"content_t_438"}).find("div",{"class":"block"})
		nb_d = bsObj.find("div",{"id":"content_t_438"}).findAll("div",{"class":"block"})[1]
		flink1 = nb_s.find("div",{"class":"stable div_margin"}).find("div").find("a")["href"]
		flink2 = nb_d.find("div",{"class":"stable div_margin"}).find("div").find("a")["href"]
		fvalue1 = nb_s.find("div",{"class":"supports"}).find("p")
		fvalue2 = nb_d.find("div",{"class":"supports"}).find("p")
		i=0
		for child in fvalue1:
			i+=1
			if i == 3:
				fversion1=child
				continue
			if i == 5:
				fsize1=child
				break
		i=0
		for child in fvalue2:
			i+=1
			if i == 3:
				fversion2=child
				continue
			if i == 5:
				fsize2=child
				break
		fversion1 = fversion1.split(" ",1)[1].strip()
		fversion2 = fversion2.split(" ",1)[1].strip()
		fsize1 = fsize1.split(" ",1)[1]
		fsize2 = fsize2.split(" ",1)[1]
	except:
		return analyze_failed(name)
	print("")
	print("MIUI Global:")
	print("")
	print("Stable ROM:")
	print("\n=== The latest version:\n\n    " + fversion1)
	print("\n=== Download link:\n\n    " + flink1)
	print("\n=== Size:\n\n    " + fsize1)
	print("")
	print("Developer ROM:")
	print("\n=== The latest version:\n\n    " + fversion2)
	print("\n=== Download link:\n\n    " + flink2)
	print("\n=== Size:\n\n    " + fsize2)
	saved = None
	if fast_flag == False:
		saved = read_from_json("save.json")
	saved = saved_update("MIUI Global Stable ROM", fversion1, saved)
	saved = saved_update("MIUI Global Developer ROM", fversion2, saved)
	return saved

def miui_mr(fast_flag):
	name = "miui_mr"
	ual = ua_open("https://multirom.me/index.php?m=app&a=view&id=54&app=roms")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb_c = bsObj.find("div",{"id":"last_roms142"})
		nb_g = bsObj.find("div",{"id":"last_roms186"})
		flink1 = nb_c.find("div",{"class":"wbtn-center"}).find("a")["href"]
		flink2 = nb_g.find("div",{"class":"wbtn-center"}).find("a")["href"]
		fname1 = flink1.split("/",4)[-1]
		fname2 = flink2.split("/",4)[-1]
		fvalue1 = nb_c.find("div",{"class":"rom_info"})
		fvalue2 = nb_g.find("div",{"class":"rom_info"})
		fversion1 = fvalue1.find("span").get_text().split(" ")[-1]
		fversion2 = fvalue2.find("span").get_text().split(" ")[-1]
		fsize1 = fvalue1.findAll("span")[2].get_text().split(" ")[-2] + " MB"
		fsize2 = fvalue2.findAll("span")[2].get_text().split(" ")[-2] + " MB"
		flink3 = "https://mirror.byteturtle.eu/multirom/" + fname1
		flink4 = "https://mirror.byteturtle.eu/multirom/" + fname2
		# Download link from the official website can not be downloaded normally, 
		# so give up.
		flink1 = flink3
		flink2 = flink4
		flink3 = None
		flink4 = None
	except:
		return analyze_failed(name)
	print("")
	print("MIUI MultiRom Developer ROM:")
	print("")
	print("China:")
	print("\n=== The latest version:\n\n    " + fversion1)
	print("\n=== Mirror Station Download Link (Quick):\n\n    " + flink1)
	print("\n=== Size\n\n    " + fsize1)
	print("")
	print("Global:")
	print("\n=== The latest version:\n\n    " + fversion2)
	print("\n=== Mirror Station Download Link (Quick):\n\n    " + flink2)
	print("\n=== Size:\n\n    " + fsize2)
	saved = None
	if fast_flag == False:
		saved = read_from_json("save.json")
	saved = saved_update("MIUI MultiRom Developer ROM China", fversion1, saved)
	saved = saved_update("MIUI MultiRom Developer ROM Global", fversion2, saved)
	return saved

def miui_pl(fast_flag):
	name = "miui_pl"
	ual = ua_open("https://miuipolska.pl/download/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"id":"redmi-note-3-pro"}).find_next().find("div",{"class":"col-sm-9"})
		flink1 = nb.find("ul",{"class":"dwnl-b"}).find("li").find("a")["href"]
		flink2 = nb.find("ul",{"class":"dwnl-b"}).findAll("li")[1].find("a")["href"]
		flink3 = nb.findAll("ul",{"class":"dwnl-b"})[1].find("li").find("a")["href"]
		fvalue = nb.find("div",{"class":"dwnl-m"})
		fversion = fvalue.find("ul").find("li").get_text().split(" ")[-1]
		fsize = fvalue.find("ul").findAll("li")[-1].get_text().split(" ")[-1]
		fvalue2 = fvalue.find("i").get_text().split(" ")
		fmd5 = fvalue2[1]
		fdate = fvalue2[-1]
	except:
		return analyze_failed(name)
	print("")
	print("MIUI Poland Developer ROM:")
	print("\n=== The latest version:\n\n    " + fversion)
	print("\n=== Updated:\n\n    " + fdate)
	print("\n=== MD5:\n\n    " + fmd5)
	print("\n=== Download link:    ")
	print("\n======= Main server(sourceforge):\n\n        " + flink1)
	print("\n======= Spare 1(AFH):\n\n        " + flink2)
	print("\n======= Spare 2:\n\n        " + flink3)
	print("\nSize:\n\n" + fsize)
	saved = None
	if fast_flag == False:
		saved = read_from_json("save.json")
	return saved_update("MIUI Poland Developer ROM", fversion, saved)

def mokee(fast_flag):
	name = "mokee"
	# hahahaha
	time.sleep(1)
	print('''
Mokee Official Nightly:

=== The latest version:

    Keep updated daily, inquiries are not necessary

=== Download link:

    You need to see the advertisement before you can get it :P

    https://download.mokeedev.com/?device=kenzo''')
	return None

def nos_o(fast_flag):
	name = "nos_o"
	build_info = {}
	ual = de_open("https://sourceforge.net/projects/nitrogen-project/files/kenzo/kenzo_test/8.1/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[1]
		nb2 = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[0]
		# Sometimes log and Rom locations are reversed due to the order of uploads,
		# So...
		if nb["title"].split(".")[-1] != "zip":
			swap_temp = nb;nb = nb2;nb2 = swap_temp
		build_info['update_log'] = nb2.find("th").find("a")["href"]
		fversion = nb["title"]
		build_info['fdate'] = nb.find("td").find("abbr")["title"]
		build_info['flink'] = nb.find("th").find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[1].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def nos_s(fast_flag):
	name = "nos_s"
	build_info = {}
	ual = de_open("https://sourceforge.net/projects/nitrogen-project/files/kenzo/kenzo_stable/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[1]
		nb2 = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[0]
		if nb["title"].split(".")[-1] != "zip":
			swap_temp = nb;nb = nb2;nb2 = swap_temp
		build_info['update_log'] = nb2.find("th").find("a")["href"]
		fversion = nb["title"]
		build_info['fdate'] = nb.find("td").find("abbr")["title"]
		build_info['flink'] = nb.find("th").find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[1].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def omni(fast_flag):
	name = "omni"
	build_info = {}
	ual = de_open("http://dl.omnirom.org/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"id":"fallback"}).find("table").findAll("tr")[-2]
		if fast_flag == False:
			fmd5 = bsObj.find("div",{"id":"fallback"}).find("table"). \
					findAll("tr")[-1].findAll("td")[1].find("a").get_text()
			build_info['fmd5'] = get_md5_from_file("http://dl.omnirom.org/kenzo/" + fmd5)
		fversion = nb.findAll("td")[1].find("a").get_text()
		build_info['fdate'] = nb.findAll("td")[2].get_text()
		build_info['flink'] = "http://dl.omnirom.org/kenzo/" + fversion
		build_info['fsize'] = nb.findAll("td")[3].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def rr(fast_flag):
	name = "rr"
	build_info = {}
	ual = de_open("https://sourceforge.net/projects/resurrectionremix/files/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"files_list"}).findAll("tbody")[0].findAll("tr")[1]
		fversion = nb["title"]
		build_info['fdate'] = nb.find("td").find("abbr")["title"]
		build_info['flink'] = nb.find("th").find("a")["href"]
		build_info['fsize'] = nb.findAll("td")[1].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def sudamod(fast_flag):
	name = "sudamod"
	build_info = {}
	ual = de_open("https://sudamod.download/kenzo")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"class":"striped bordered"}).find("tbody").find("tr")
		build_info['fmd5'] = nb.findAll("td")[2].find("small").get_text().split(" ")[1]
		build_info['build_type'] = nb.findAll("td")[0].get_text()
		fversion = nb.findAll("td")[2].find("a").get_text()
		build_info['build_version'] = nb.findAll("td")[1].get_text()
		build_info['fdate'] = nb.findAll("td")[-2].get_text()
		build_info['flink'] = nb.findAll("td")[2].find("a")["href"]
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def twrp(fast_flag):
	name = "twrp"
	build_info = {}
	ual = de_open("https://dl.twrp.me/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"class":"post"}).findAll("article",
				{"class":"post-content"})[1].find("table").find("tr")
		nblink = nb.find("td").find("a")["href"]
		fversion = nb.find("td").find("a").get_text()
		build_info['fsize'] = nb.findAll("td")[1].find("small").get_text()
		build_info['fdate'] = nb.findAll("td")[2].find("em").get_text()
		ual2 = de_open("https://dl.twrp.me" + nblink)
		bsObj2 = get_bs(ual2)
		if not bsObj2:
			return open_failed(name)
		nb2 = bsObj2.find("div",{"class":"page-content"}).find("div",{"class":"post"})
		if fast_flag == False:
			fmd5 = nb2.find("header",{"class":"post-header"}).find("p").find("a")["href"]
			build_info['fmd5'] = get_md5_from_file("https://dl.twrp.me" + fmd5)
		build_info['flink'] = "https://dl.twrp.me" + nb2.find("article",{"class":"post-content"}).find("h3").find("a")["href"]
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def viperos(fast_flag):
	name = "viperos"
	build_info = {}
	ual = ua_open("http://viper-os.com/devicedownloads/redminote3pro.html")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("div",{"class":"table-scroll"}).find("tbody").find("tr")
		fmd5 = nb.findAll("td")[1]
		fversion = fmd5.find("a").get_text()
		build_info['flink'] = fmd5.find("a")["href"]
		i = 1
		for child in fmd5:
			if i == 4:
				build_info['fmd5'] = child.strip().split(" ")[1]
				break
			i+=1
		build_info['fsize'] = nb.findAll("td")[2].get_text().strip()
		build_info['fdate'] = nb.findAll("td")[3].get_text().strip()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

def xenonhd(fast_flag):
	name = "xenonhd"
	build_info = {}
	ual = de_open("https://mirrors.c0urier.net/android/teamhorizon/N/Official/kenzo/")
	bsObj = get_bs(ual)
	if not bsObj:
		return open_failed(name)
	try:
		nb = bsObj.find("table",{"id":"indexlist"}).findAll("tr")[-2]
		if fast_flag == False:
			fmd5 = bsObj.find("table",{"id":"indexlist"}).findAll("tr") \
					[-1].findAll("td")[1].find("a").get_text()
			build_info['fmd5'] = get_md5_from_file("https://mirrors.c0urier.net/android/teamhorizon/N/Official/kenzo/" + fmd5)
		fversion = nb.findAll("td")[1].find("a").get_text()
		build_info['fdate'] = nb.findAll("td")[2].get_text()
		build_info['flink'] = "https://mirrors.c0urier.net/android/teamhorizon/N/Official/kenzo/" + fversion
		build_info['fsize'] = nb.findAll("td")[3].get_text()
	except:
		return analyze_failed(name)
	return out_put(fast_flag, name, fversion, build_info)

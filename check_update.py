#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, time, re
from tools import *

def sf_check(bsObj, cl_flag = False, skip = 0):
    try:
        build_info = {}
        nb = bsObj.find("table",{"id":"files_list"})\
             .find_all("tbody")[0].find_all("tr")
        nb1 = nb[skip]
        if cl_flag:
            nb2 = nb[skip + 1]
            if nb1["title"].split(".")[-1] != "zip":
                nb1, nb2 = nb2, nb1
            build_info['update_log'] = nb2.find("th").find("a")["href"]
        nb3 = json.loads(bsObj.find_all("script")[-1]\
              .get_text().split(" = ",1)[-1].split(";",1)[0])
        fversion = nb1["title"]
        build_info['fmd5'] = nb3[fversion]["md5"]
        build_info['fsha1'] = nb3[fversion]["sha1"]
        build_info['fdate'] = nb1.find("td").find("abbr")["title"]
        build_info['flink'] = nb1.find("th").find("a")["href"]
        build_info['fsize'] = nb1.find_all("td")[1].get_text()
        return fversion, build_info
    except:
        return None, {}

def h5ai_check(bsObj, fast_flag, web_link):
    try:
        build_info = {}
        nb = bsObj.find("div",{"id":"fallback"})\
             .find("table").find_all("tr")[-1]
        while True:
            fversion = nb.find_all("td")[1].find("a").get_text()
            if fversion.split(".")[-1] == "zip":
                break
            nb = nb.previous_sibling
        if fast_flag == False:
            for child in nb.parent:
                try:
                    file_hash = child.find_all("td")[1]\
                                .find("a").get_text()
                except IndexError:
                    continue
                if file_hash == (fversion + ".md5sum"):
                    fmd5 = child.find_all("td")[1].find("a")["href"]
                    build_info['fmd5'] = \
                        get_md5_from_file(web_link + fmd5)
                if file_hash == (fversion + ".sha256sum"):
                    fsha256 = child.find_all("td")[1].find("a")["href"]
                    build_info['fsha256'] = \
                        get_md5_from_file(web_link + fsha256)
        build_info['fdate'] = nb.find_all("td")[2].get_text()
        build_info['flink'] = web_link + \
                              nb.find_all("td")[1].find("a")["href"]
        build_info['fsize'] = nb.find_all("td")[3].get_text()
        return fversion, build_info
    except:
        return None, {}

def aex(fast_flag, bs4_parser):
    name = "aex"
    build_info = {}
    url = "https://downloads.aospextended.com"
    ual = ua_open(url + "/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("table",{"class":"cm"})\
             .find("tbody").find("tr").find_all("td")
        nb_info = nb[1].get_text().split(" ")
        fversion = nb_info[0].strip()
        build_info['fsize'] = nb_info[3] + " " + nb_info[4]
        build_info['fmd5'] = nb_info[6]
        build_info['flink'] = url + nb[1].find("a")["href"]
        build_info['fdate'] = nb[2].get_text().strip()
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def aex_sf(fast_flag, bs4_parser):
    name = "aex_sf"
    build_info = {}
    ual = ua_open("https://sourceforge.net/projects/"
                  "aospextended-rom/files/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("table",{"id":"files_list"})\
            .find_all("tbody")[0].find_all("tr")[0]
        if nb["class"] == ["empty"]:
            fversion = "Looks like there is no Rom file right now"
        else:
            nb2 = json.loads(bsObj.find_all("script")[-1]\
                  .get_text().split(" = ",1)[-1].split(";",1)[0])
            fversion = nb["title"]
            build_info['fmd5'] = nb2[fversion]["md5"]
            build_info['fsha1'] = nb2[fversion]["sha1"]
            build_info['fdate'] = nb.find("td").find("abbr")["title"]
            build_info['flink'] = nb.find("th").find("a")["href"]
            build_info['fsize'] = nb.find_all("td")[1].get_text()
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def aicp(fast_flag, bs4_parser):
    name = "aicp"
    build_info = {}
    ual = de_open("http://dwnld.aicp-rom.com/?device=kenzo")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("table",
		                {"class":"table table-bordered table-striped"}
		               ).find("tbody").find("tr")
        build_info['build_type'] = nb.find_all("td")[1].get_text()
        build_info['fsize'] = nb.find_all("td")[3].get_text()
        build_info['update_log'] = nb.find_all("td")[2]\
                                   .find_all("a")[1]["href"]
        fversion = nb.find_all("td")[2].find("a").get_text()
        build_info['fdate'] = nb.find_all("td")[-1].get_text()
        fmd5_temp = nb.find_all("td")[2].find("small")\
                    .get_text().split(":")[1]
        fmd5 = ""
        for char in fmd5_temp:
            if re.match('[0-9a-fA-F]',char):
                fmd5+=char
        build_info['fmd5'] = fmd5
        build_info['flink'] = nb.find_all("td")[2].find("a")["href"]
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def aim_u1(fast_flag, bs4_parser):
    name = "aim_u1"
    ual = ua_open("https://sourceforge.net/projects/"
                  "redmi-note-3/files/AIM/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def aoscp(fast_flag, bs4_parser):
    name = "aoscp"
    ual = ua_open("https://sourceforge.net/projects/"
                  "unofficial-cypheros-for-kenzo/files/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, skip = 1)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def aosip(fast_flag, bs4_parser):
    name = "aosip"
    url = "https://get.aosiprom.com"
    ual = de_open(url + "/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = \
        h5ai_check(bsObj, fast_flag, url)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def bliss(fast_flag, bs4_parser):
    name = "bliss"
    url = "https://downloads.blissroms.com"
    ual = de_open(url + "/Bliss/Official/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = \
        h5ai_check(bsObj, fast_flag, url)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def cardinal(fast_flag, bs4_parser):
    name = "cardinal"
    ual = ua_open("https://sourceforge.net/projects/"
                  "cardinal-aosp/files/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, skip = 1)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def cosmicos(fast_flag, bs4_parser):
    name = "cosmicos"
    ual = ua_open("https://sourceforge.net/projects/"
                  "cosmic-os/files/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
        bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def dotos(fast_flag, bs4_parser):
    name = "dotos"
    ual = ua_open("https://sourceforge.net/projects/"
                  "dotos-ota/files/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def flyme(fast_flag, bs4_parser):
    name = "flyme"
    build_info = {}
    ual = de_open("http://www.flyme.cn/firmwarelist-51.html")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("div",{"class":"wrap"})\
             .find_next("script",{"type":"text/javascript"})\
             .get_text().split("data=",1)[-1].replace(";","")
        # This magical command can convert strings to dictionaries.
        # By the way, 
        # Unicode encoding can be switched back to Chinese. Great!
        nb = json.loads(nb)
        # "0_1" point to haohao3344's version,
        # "1_1" point to Pan's version.
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

def los(fast_flag, bs4_parser):
    name = "los"
    build_info = {}
    ual = de_open("https://download.lineageos.org/kenzo")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("table",{"class":"striped bordered"})\
             .find("tbody").find("tr")
        fversion = nb.find_all("td")[2].find("a").get_text()
        build_info['build_type'] = nb.find_all("td")[0].get_text()
        build_info['build_version'] = nb.find_all("td")[1].get_text()
        build_info['flink'] = nb.find_all("td")[2].find("a")["href"]
        if fast_flag == False:
            build_info['fsha256'] = \
                get_md5_from_file(build_info['flink'] + "?sha256")
            build_info['fsha1'] = \
                get_md5_from_file(build_info['flink'] + "?sha1")
        build_info['fdate'] = nb.find_all("td")[-1].get_text()
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def los_u1(fast_flag, bs4_parser):
    name = "los_u1"
    build_info = {}
    ual = de_open("https://github.com/los-kenzo/"
                  "downloads/blob/lk-7.1/README.md")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("article",
                        {"class":"markdown-body entry-content"})
        build_info['update_log'] = nb.find_all("ul")[0].get_text()\
                                   .replace("\n","\n    ")[5:-5]
        build_info['flink'] = nb.find_all("a")[2]["href"]
        fversion = nb.find_all("a")[2].get_text()
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def los_mg(fast_flag, bs4_parser):
    name = "los_mg"
    url = "https://download.lineage.microg.org"
    ual = de_open(url + "/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = h5ai_check(bsObj, fast_flag, url)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def miui_br(fast_flag, bs4_parser):
    name = "miui_br"
    build_info = {}
    ual = ua_open("http://miuibrasil.org/downloads/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("div",{"id":"kenzo"})\
             .find("div",{"class":"x-accordion-inner"}).find("a")
        build_info['flink'] = nb["href"]
        fversion = nb.get_text().split(" ")[-1]
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def miui_c(fast_flag, bs4_parser):
    name = "miui_c"
    ual = de_open("http://www.miui.com/download-308.html")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb_s = bsObj.find("div",{"id":"content_t_451"})\
               .find("div",{"class":"block"})
        nb_d = bsObj.find("div",{"id":"content_t_451"})\
               .find_all("div",{"class":"block"})[1]
        flink1 = nb_s.find("div",{"class":"to_miroute"})\
                 .find("a")["href"]
        flink2 = nb_d.find("div",{"class":"to_miroute"})\
                 .find("a")["href"]
        fvalue1 = nb_s.find("div",{"class":"supports"})\
                  .find("p").get_text().replace("\n","").split("：")
        fvalue2 = nb_d.find("div",{"class":"supports"})\
                  .find("p").get_text().replace("\n","").split("：")
        fversion1 = fvalue1[2][:-2]
        fsize1 = fvalue1[-1]
        fversion2 = fvalue2[2][:-2]
        fsize2 = fvalue2[-1]
    except:
        return analyze_failed(name)
    print("\nMIUI China:")
    print("\n# Stable ROM:")
    print("\n=== The latest version:\n\n    " + fversion1)
    print("\n=== Download link:\n\n    " + flink1)
    print("\n=== Size:\n\n    " + fsize1)
    print("\n# Developer ROM:")
    print("\n=== The latest version:\n\n    " + fversion2)
    print("\n=== Download link:\n\n    " + flink2)
    print("\n=== Size:\n\n    " + fsize2)
    saved = {}
    if fast_flag == False:
        saved = read_from_json("save.json")
    saved = saved_update("MIUI China Stable ROM", fversion1, saved)
    saved = saved_update("MIUI China Developer ROM", fversion2, saved)
    return saved

def miui_g(fast_flag, bs4_parser):
    name = "miui_g"
    ual = de_open("http://en.miui.com/download-301.html")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb_s = bsObj.find("div",{"id":"content_t_438"})\
               .find("div",{"class":"block"})
        nb_d = bsObj.find("div",{"id":"content_t_438"})\
               .find_all("div",{"class":"block"})[1]
        flink1 = nb_s.find("div",{"class":"stable div_margin"})\
                 .find("div").find("a")["href"]
        flink2 = nb_d.find("div",{"class":"stable div_margin"})\
                 .find("div").find("a")["href"]
        fvalue1 = nb_s.find("div",{"class":"supports"})\
                  .find("p").get_text().replace("\n","").split(": ")
        fvalue2 = nb_d.find("div",{"class":"supports"})\
                  .find("p").get_text().replace("\n","").split(": ")
        fversion1 = fvalue1[2][:-4]
        fsize1 = fvalue1[-1]
        fversion2 = fvalue2[2][:-4]
        fsize2 = fvalue2[-1]
    except:
        return analyze_failed(name)
    print("\nMIUI Global:")
    print("\n# Stable ROM:")
    print("\n=== The latest version:\n\n    " + fversion1)
    print("\n=== Download link:\n\n    " + flink1)
    print("\n=== Size:\n\n    " + fsize1)
    print("\n# Developer ROM:")
    print("\n=== The latest version:\n\n    " + fversion2)
    print("\n=== Download link:\n\n    " + flink2)
    print("\n=== Size:\n\n    " + fsize2)
    saved = {}
    if fast_flag == False:
        saved = read_from_json("save.json")
    saved = saved_update("MIUI Global Stable ROM", fversion1, saved)
    saved = saved_update("MIUI Global Developer ROM", fversion2, saved)
    return saved

def miui_mr(fast_flag, bs4_parser):
    name = "miui_mr"
    ual = ua_open("https://multirom.me"
                  "/index.php?m=app&a=view&id=54&app=roms")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb_c = bsObj.find("div",{"id":"last_roms142"})
        nb_g = bsObj.find("div",{"id":"last_roms186"})
        flink1 = nb_c.find("div",{"class":"wbtn-center"})\
                 .find("a")["href"]
        flink2 = nb_g.find("div",{"class":"wbtn-center"})\
                 .find("a")["href"]
        fname1 = flink1.split("/",4)[-1]
        fname2 = flink2.split("/",4)[-1]
        fvalue1 = nb_c.find("div",{"class":"rom_info"})
        fvalue2 = nb_g.find("div",{"class":"rom_info"})
        fversion1 = fvalue1.find("span").get_text().split(" ")[-1]
        fversion2 = fvalue2.find("span").get_text().split(" ")[-1]
        fsize1 = fvalue1.find_all("span")[2]\
                 .get_text().split(" ")[-2] + " MB"
        fsize2 = fvalue2.find_all("span")[2]\
                 .get_text().split(" ")[-2] + " MB"
        mirror_url = "https://mirror.byteturtle.eu/multirom/"
        flink3 = mirror_url + fname1
        flink4 = mirror_url + fname2
        # Download link from the official website can not
        # be downloaded normally, so give up.
        flink1 = flink3
        flink2 = flink4
        flink3 = None
        flink4 = None
    except:
        return analyze_failed(name)
    print("\nMIUI MultiRom Developer ROM:")
    print("\n# China:")
    print("\n=== The latest version:\n\n    " + fversion1)
    print("\n=== Mirror Station Download Link (Quick):\n\n    "
          + flink1)
    print("\n=== Size\n\n    " + fsize1)
    print("\n# Global:")
    print("\n=== The latest version:\n\n    " + fversion2)
    print("\n=== Mirror Station Download Link (Quick):\n\n    "
          + flink2)
    print("\n=== Size:\n\n    " + fsize2)
    saved = {}
    if fast_flag == False:
        saved = read_from_json("save.json")
    saved = saved_update("MIUI MultiRom Developer ROM China",
                         fversion1, saved)
    saved = saved_update("MIUI MultiRom Developer ROM Global",
                         fversion2, saved)
    return saved

def miui_pl(fast_flag, bs4_parser):
    name = "miui_pl"
    build_info = {}
    ual = ua_open("https://miuipolska.pl/download/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("div",{"id":"redmi-note-3-pro"})\
             .find_next().find("div",{"class":"col-sm-9"})
        flink1 = nb.find("ul",{"class":"dwnl-b"})\
                 .find("li").find("a")["href"]
        flink2 = nb.find("ul",{"class":"dwnl-b"})\
                 .find_all("li")[1].find("a")["href"]
        flink3 = nb.find_all("ul",{"class":"dwnl-b"})[1]\
                 .find("li").find("a")["href"]
        fvalue = nb.find("div",{"class":"dwnl-m"})
        fversion = fvalue.find("ul").find("li")\
                   .get_text().split(" ")[-1]
        fvalue2 = fvalue.find("i").get_text().split(" ")
        build_info['fsize'] = fvalue.find("ul").find_all("li")[-1]\
                              .get_text().split(" ")[-1]
        build_info['fmd5'] = fvalue2[1]
        build_info['fdate'] = fvalue2[-1]
        build_info['flink'] = \
            "# Main server(sourceforge):\n\n    " + flink1 + \
            "\n\n    # Spare 1(AFH):\n\n    " + flink2 + \
            "\n\n    # Spare 2:\n\n    " + flink3
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def mokee(fast_flag, bs4_parser):
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

def nos_o1(fast_flag, bs4_parser):
    name = "nos_o1"
    ual = ua_open("https://sourceforge.net/projects/"
                  "nitrogen-project/files/kenzo/kenzo_test/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, cl_flag = True, skip = 1)
    if fversion == None:
        return analyze_failed(name)
    flink2 = ("https://sourceforge.mirrorservice.org"
              "/n/ni/nitrogen-project/kenzo/kenzo_test/"
              + fversion)
    build_info['flink'] = \
        "# Sourceforge:\n\n    " + build_info['flink'] + \
        "\n\n    # Mirror for Sourceforge:\n\n    " + flink2
    return out_put(fast_flag, name, fversion, build_info)

def nos_o2(fast_flag, bs4_parser):
    name = "nos_o2"
    ual = ua_open("https://sourceforge.net/projects/"
                  "nitrogen-project/files/kenzo/kenzo_test/8.1/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, cl_flag = True)
    if fversion == None:
        return analyze_failed(name)
    flink2 = ("https://sourceforge.mirrorservice.org"
              "/n/ni/nitrogen-project/kenzo/kenzo_test/8.1/"
              + fversion)
    build_info['flink'] = \
        "# Sourceforge:\n\n    " + build_info['flink'] + \
        "\n\n    # Mirror for Sourceforge:\n\n    " + flink2
    return out_put(fast_flag, name, fversion, build_info)

def nos_s(fast_flag, bs4_parser):
    name = "nos_s"
    ual = ua_open("https://sourceforge.net/projects/"
                  "nitrogen-project/files/kenzo/kenzo_stable/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, cl_flag = True)
    if fversion == None:
        return analyze_failed(name)
    flink2 = "https://sourceforge.mirrorservice.org" + \
             "/n/ni/nitrogen-project/kenzo/kenzo_stable/" + fversion
    build_info['flink'] = \
        "# Sourceforge:\n\n    " + build_info['flink'] + \
        "\n\n    # Mirror for Sourceforge:\n\n    " + flink2
    return out_put(fast_flag, name, fversion, build_info)

def omni(fast_flag, bs4_parser):
    name = "omni"
    build_info = {}
    url = "http://dl.omnirom.org/kenzo/"
    ual = de_open(url)
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("div",{"id":"fallback"})\
             .find("table").find_all("tr")
        if fast_flag == False:
            fmd5 = nb[-1].find_all("td")[1].find("a").get_text()
            build_info['fmd5'] = get_md5_from_file(url + fmd5)
        fversion = nb[-2].find_all("td")[1].find("a").get_text()
        build_info['fdate'] = nb[-2].find_all("td")[2].get_text()
        build_info['fsize'] = nb[-2].find_all("td")[3].get_text()
        build_info['flink'] = url + fversion
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def pe(fast_flag, bs4_parser):
    name = "pe"
    build_info = {}
    url = "https://download.pixelexperience.org"
    ual = ua_open(url + "/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("table",{"class":"cm"})\
             .find("tbody").find("tr").find_all("td")
        nb_info = nb[1].get_text().split(" ")
        fversion = nb_info[0].strip()
        build_info['fsize'] = nb_info[3] + " " + nb_info[4]
        build_info['fmd5'] = nb_info[6]
        build_info['update_log'] = url +  nb[1].find_all("a")[1]["href"]
        build_info['flink'] = url + nb[1].find("a")["href"]
        build_info['fdate'] = nb[2].get_text().strip()
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def pe_u1(fast_flag, bs4_parser):
    name = "pe_u1"
    ual = ua_open("https://sourceforge.net/projects/"
                  "pixel-experience-for-kenzo/files/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, cl_flag = True)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def pe_u2b(fast_flag, bs4_parser):
    name = "pe_u2b"
    ual = ua_open("https://sourceforge.net/projects/"
                  "pixel-experience/files/Beta/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, cl_flag = True)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def pe_u2s(fast_flag, bs4_parser):
    name = "pe_u2s"
    ual = ua_open("https://sourceforge.net/projects/"
                  "pixel-experience/files/Stable/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, cl_flag = True)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def rr(fast_flag, bs4_parser):
    name = "rr"
    url = ("https://sourceforge.net/projects/"
           "resurrectionremix/files/kenzo/")
    ual = ua_open(url)
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj, skip = 1)
    if fversion == None:
        return analyze_failed(name)
    build_info['update_log'] = url + "Changelog.txt/download"
    return out_put(fast_flag, name, fversion, build_info)

def screwd_u1(fast_flag, bs4_parser):
    name = "screwd_u1"
    ual = ua_open("https://sourceforge.net/projects/"
                  "redmi-note-3/files/Screwd/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def sudamod(fast_flag, bs4_parser):
    name = "sudamod"
    build_info = {}
    ual = de_open("https://sudamod.download/kenzo")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("table",{"class":"striped bordered"})\
             .find("tbody").find("tr")
        build_info['fmd5'] = nb.find_all("td")[2].find("small")\
                             .get_text().split(" ")[1]
        fversion = nb.find_all("td")[2].find("a").get_text()
        build_info['build_type'] = nb.find_all("td")[0].get_text()
        build_info['build_version'] = nb.find_all("td")[1].get_text()
        build_info['fdate'] = nb.find_all("td")[-2].get_text()
        build_info['flink'] = nb.find_all("td")[2].find("a")["href"]
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def twrp(fast_flag, bs4_parser):
    name = "twrp"
    build_info = {}
    ual = de_open("https://dl.twrp.me/kenzo/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("div",{"class":"post"})\
             .find_all("article",{"class":"post-content"})[1]\
             .find("table").find("tr").find_all("td")
        nblink = nb[0].find("a")["href"]
        fversion = nb[0].find("a").get_text()
        build_info['fsize'] = nb[1].find("small").get_text()
        build_info['fdate'] = nb[2].find("em").get_text()
        if fast_flag == False:
            # The default is to parse "Primary (Americas)" download page
            ual2 = de_open("https://dl.twrp.me" + nblink)
            bsObj2 = get_bs(ual2, bs4_parser)
            if not bsObj2:
                return open_failed(name)
            nb2 = bsObj2.find("div",{"class":"page-content"})\
                  .find("div",{"class":"post"})
            fmd5 = nb2.find("header",{"class":"post-header"})\
                   .find("p").find("a")["href"]
            build_info['fmd5'] = \
                get_md5_from_file("https://dl.twrp.me" + fmd5)
        flink1 = "https://dl.twrp.me/kenzo/" + fversion
        flink2 = "https://eu.dl.twrp.me/kenzo/" + fversion
        build_info['flink'] = \
            "# Primary (Americas):\n\n    " + flink1 + \
            "\n\n    # Primary (Europe):\n\n    " + flink2
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def validus_u1(fast_flag, bs4_parser):
    name = "validus_u1"
    ual = ua_open("https://sourceforge.net/projects/"
                  "sarveshrulz/files/Validus/")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    fversion, build_info = sf_check(bsObj)
    if fversion == None:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def viperos(fast_flag, bs4_parser):
    name = "viperos"
    build_info = {}
    ual = ua_open("http://viper-os.com"
                  "/devicedownloads/redminote3pro.html")
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("div",{"class":"table-scroll"})\
             .find("tbody").find("tr")
        fmd5 = nb.find_all("td")[1]
        fversion = fmd5.find("a").get_text()
        build_info['flink'] = fmd5.find("a")["href"]
        i = 1
        for child in fmd5:
            if i == 4:
                build_info['fmd5'] = child.strip().split(" ")[1]
                break
            i+=1
        build_info['fsize'] = nb.find_all("td")[2].get_text().strip()
        build_info['fdate'] = nb.find_all("td")[3].get_text().strip()
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

def xenonhd(fast_flag, bs4_parser):
    name = "xenonhd"
    build_info = {}
    url = ("https://mirrors.c0urier.net/android/"
           "teamhorizon/N/Official/kenzo/")
    ual = de_open(url)
    bsObj = get_bs(ual, bs4_parser)
    if not bsObj:
        return open_failed(name)
    try:
        nb = bsObj.find("table",{"id":"indexlist"}).find_all("tr")[-2]
        if fast_flag == False:
            fmd5 = bsObj.find("table",{"id":"indexlist"})\
                   .find_all("tr")[-1].find_all("td")[1]\
                   .find("a").get_text()
            build_info['fmd5'] = get_md5_from_file(url + fmd5)
        fversion = nb.find_all("td")[1].find("a").get_text()
        build_info['fdate'] = nb.find_all("td")[2].get_text()
        build_info['flink'] = url + fversion
        build_info['fsize'] = nb.find_all("td")[3].get_text()
    except:
        return analyze_failed(name)
    return out_put(fast_flag, name, fversion, build_info)

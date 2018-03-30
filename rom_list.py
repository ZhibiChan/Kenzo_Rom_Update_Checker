#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Rom_List:
    def __init__(self):
        __roms_list = [
            "aex_sf",
            "aim",
            "aim_u1",
            "aim_u2",
            "aosip",
            "cardinal",
            "cosmicos",
            "aoscp",
            "aoscp_u1",
            "aoscp_u2",
            "du_u1",
            "firehound",
            "los_o_u1",
            "nos_o1",
            "nos_o2",
            "pe",
            "pe_u1",
            "pe_u2s",
            "pe_u2b",
            "rr_o",
            "screwd_u1",
            "validus_u1",
            "aex",
            "aicp",
            "bliss",
            "dotos",
            "flyme",
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
            "miui_c",
            "miui_g",
            "miui_mr",
            "miui_pl",
            "twrp",
            "twrp_u1"
        ]
        self.check_list = {}
        i = 1
        for item in __roms_list:
            self.check_list[str(i)] = item
            i+=1
        
        self.rom8_list = {
            "aex_sf":"AospExtended Oreo Official",
            "aim":"AIM Official",
            "aim_u1":"AIM (Unofficial By carlosarriaga)",
            "aim_u2":"AIM (Unofficial By sarveshrulz)",
            "aosip":"AOSiP Official",
            "cardinal":"Cardinal AOSP Official",
            "cosmicos":"Cosmic OS Official",
            "aoscp":"CypherOS Official",
            "aoscp_u1":"CypherOS (Unofficial By sarveshrulz)",
            "aoscp_u2":"CypherOS (Unofficial By miguelndecarval)",
            "du_u1":"Dirty Unicorns (Unofficial By sarveshrulz)",
            "firehound":"FireHound Official",
            "los_o_u1":"LineageOS 15.1 (Unofficial By LokManSiu)",
            "nos_o1":"Nitrogen OS Official Test",
            "nos_o2":"Nitrogen OS Official 8.1 Test",
            "pe":"Pixel Experience Official",
            "pe_u1":"Pixel Experience (Unofficial By irvin16, miguelndecarval)",
            "pe_u2s":"Pixel Experience Stable (Unofficial By irvin16)",
            "pe_u2b":"Pixel Experience Beta (Unofficial By irvin16)",
            "rr_o":"Resurrection Remix OS Oreo Official",
            "screwd_u1":"Screwd (Unofficial By carlosarriaga)",
            "validus_u1":"Validus (Unofficial By sarveshrulz)"
        }
        self.rom7_list = {
            "aex":"AospExtended Official",
            "aicp":"AICP Official",
            "bliss":"Bliss Official",
            "dotos":"DotOS Official",
            "flyme":"Flyme Official(haohao3344)",
            "los":"LineageOS Official",
            "los_mg":"LineageOS for MicroG Unofficial",
            "los_u1":"LineageOS 14.1 (Unofficial By Umang96)",
            "mokee":"Mokee Official Nightly",
            "nos_s":"Nitrogen OS Official Stable",
            "omni":"Omni Official",
            "rr":"Resurrection Remix OS Official",
            "sudamod":"SudaMod Official",
            "viperos":"ViperOS Official",
            "xenonhd":"XenonHD Official"
        }
        self.rom6_list = {
            "miui_c":"MIUI China",
            "miui_g":"MIUI Global",
            "miui_mr":"MIUI MultiRom Developer ROM",
            "miui_pl":"MIUI Poland Developer ROM"
        }
        self.other_list = {
            "twrp":"TWRP Official",
			"twrp_u1":"TWRP (Unofficial By LokManSiu)"
        }
        self.list_all = {
            **self.rom8_list,
            **self.rom7_list,
            **self.rom6_list,
            **self.other_list
        }
        

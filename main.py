#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, socket, time
import check_update, rom_list, tools

#~ # 测试函数
#~ check_update.twrp(fast_flag = False)
#~ sys.exit()
#~ # 测试结束

def main():
	''' 初始化参数 '''
	# 工具版本
	tool_version = "v1.0.0 Alpha"
	# 连接超时时间（默认为20秒）
	socket.setdefaulttimeout(20)
	# 关闭子目录
	r8 = r7 = r6 = r5 = False
	# 导入Rom列表字典
	roms = rom_list.Rom_List()
	# 定义标号范围
	r8_s = 1		;r8_e = len(roms.rom8_list)
	r7_s = r8_e + 1	;r7_e = len(roms.rom7_list) + r8_e
	r6_s = r7_e + 1	;r6_e = len(roms.rom6_list) + r7_e
	r5_s = r6_e + 1	;r5_e = len(roms.check_list)
	# 设置窗口标题（Win系统）
	title = "title KENZO ROM 更新检查工具 " + tool_version
	os.system(title)
	
	''' 主界面循环开始 '''
	while True:
		# 主界面
		os.system("cls")
		print("======================================")
		print("      = KENZO ROM 更新检查工具 =")
		print("======================================")
		print("                             By：Pzqqt")
		print("***工具版本：" + tool_version)
		print("")
		print("===Rom 列表：")
		print("|")
		print("====①：Android 8.0")
		if r8:
			i = r8_s
			print("| |")
			for value in roms.rom8_list.values():
				print("| ====%s.%s"%(i, value))
				i+=1
		print("|")
		print("====②：Android 7.x")
		if r7:
			i = r7_s
			print("| |")
			for value in roms.rom7_list.values():
				print("| ====%s.%s"%(i, value))
				i+=1
		print("|")
		print("====③：Android 6.0")
		if r6:
			i = r6_s
			print("| |")
			for value in roms.rom6_list.values():
				print("| ====%s.%s"%(i, value))
				i+=1
		print("|")
		print("====④：其他")
		if r5:
			i = r5_s
			print("  |")
			for value in roms.other_list.values():
				print("  ====%s.%s"%(i, value))
				i+=1
		print("")
		# 开始检测用户输入
		# 子目录展开
		selected = None
		if not(r8 or r7 or r6 or r5):
			print("***请输入您需要检查版本更新的 Rom 类型标号并按回车键")
			print("")
			selected = input('***（输入e退出，输入9999可自动检查所有Rom更新）：')
			# 判断退出
			if selected == "e" or selected == "E":
				break
			# 检查输入
			if selected == "1":
				r8 = True
			if selected == "2":
				r7 = True
			if selected == "3":
				r6 = True
			if selected == "4":
				r5 = True
			if selected == "9999":
				check_all_auto(roms)
			continue
		# 子目录展开之后
		print("***请输入您需要检查版本更新的 Rom 标号并按回车键")
		print("")
		selected = input('***（输入0关闭子目录，输入e则退出）：')
		# 判断退出
		if selected == "e" or selected == "E":
			break
		# 判断关闭子目录
		if selected == "0":
			r8 = r7 = r6 = r5 = False
			continue
		# 检查输入
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
		# 用户输入检测结束
		# 开始检查
		os.system("cls")
		check_one(selected, roms)
		# 返回 or 退出
		temp = input('***输入e退出，输入其他则返回主界面：')
		if temp == "e" or temp == "E":
			break
		continue

def check_one(selected, roms):
	# 检查单个项目的更新
	print("")
	print("===正在检查，结果稍候将在下方显示...")
	print("")
	print("****************************************************************************************************")
	checking = "check_update." + roms.check_list[selected]
	temp2 = eval(checking)(fast_flag = False)
	if temp2:
		# 获取函数名标识
		checked = roms.check_list[selected]
		# 判断Rom是否有更新
		tools.check_for_update(checked, temp2)
		# 将新的字典保存至json
		tools.save_to_json(temp2, "save.json")
	print("")
	print("****************************************************************************************************")
	print("")
	print("===检查完成！")
	print("")

def check_all_auto(roms):
	# 自动检查模式
	# 此模式不执行下载MD5文件获取哈希校验值的操作（fast_flag为True），以提升检查速度
	# （不阻止可直接从页面获取的校验值）
	# 从json文件中读取已保存的Rom更新状态字典
	saved = tools.read_from_json("save.json")
	# 如果读取字典失败就新建一个字典
	if not saved:
		saved = {}
	# 临时字典，每次检查后并不写入json，直到全部检查完毕后再更新json字典并写入
	temp3 = {}
	j = 1
	while True:
		os.system("cls")
		print("")
		print("===自动检查所有Rom更新，请稍候...")
		print("")
		print("===正在检查第%s项，共%s项..." %(j, len(roms.check_list)))
		print("")
		print("****************************************************************************************************")
		checking = "check_update." + roms.check_list[str(j)]
		temp2 = eval(checking)(fast_flag = True)
		if temp2:
			# 获取函数名标识
			checked = roms.check_list[str(j)]
			# 判断Rom是否有更新
			new_flag = tools.check_for_update(checked, temp2)
			# 更新临时字典（此合并字典的方法仅限Python 3.5以上版本）
			temp3 = {**temp3, **temp2}
			#~ # 其他的合并字典的方法：
			#~ # 1.字典解析法（最笨、最慢、最可靠的方法）：
			#~ for key,value in temp2.items():
				#~ temp3[key] = value
			#~ # 2.元素拼接法（Python3版本不可省略将字典转为列表的步骤）：
			#~ temp3 = dict(list(temp3.items()) + list(temp2.items()))
		elif roms.check_list[str(j)] != "mokee":
			# 如果发生异常则延时3秒并提示
			print("")
			print("****************************************************************************************************")
			print("")
			print("===3秒后继续...")
			time.sleep(3)
		j+=1
		if new_flag:
			print("")
			print("****************************************************************************************************")
			print("")
			input('***按回车键继续：')
		new_flag = False
		if j > len(roms.check_list):
			# 将临时字典更新至json字典
			saved = {**saved, **temp3}
			# 将json字典写入json
			tools.save_to_json(saved, "save.json")
			os.system("cls")
			print("")
			print("****************************************************************************************************")
			print("")
			print("===检查完成！")
			print("")
			input('***按回车键返回主界面：')
			break

# 开始主界面循环
main()
# 跳出循环后清屏并退出程序
os.system("cls")
sys.exit()

#!/usr/bin/env python
# -*- coding:cp936 -*-
import pandas
import math
import os
import Tkinter
import tkFileDialog
import tkMessageBox

filename_original = unicode()
filename_display = unicode()
title = ['Target Type', 'Target Name', 'Access Specification Name', '# Managers', '# Workers', '# Disks', 'IOps',
         'Read IOps',
         'Write IOps', 'MBps', 'Read MBps', 'Write MBps', 'Transactions per Second', 'Connections per Second',
         'Average Response Time', 'Average Read Response Time', 'Average Write Response Time',
         'Average Transaction Time', 'Average Connection Time', 'Maximum Response Time', 'Maximum Read Response Time',
         'Maximum Write Response Time', 'Maximum Transaction Time', 'Maximum Connection Time', 'Errors', 'Read Errors',
         'Write Errors', 'Bytes Read', 'Bytes Written', 'Read I/Os', 'Write I/Os', 'Connections',
         'Transactions per Connection', 'Total Raw Read Response Time', 'Total Raw Write Response Time',
         'Total Raw Transaction Time', 'Total Raw Connection Time', 'Maximum Raw Read Response Time',
         'Maximum Raw Write Response Time', 'Maximum Raw Transaction Time', 'Maximum Raw Connection Time',
         'Total Raw Run Time', 'Starting Sector', 'Maximum Size', 'Queue Depth', '% CPU Utilization', '% User Time',
         '% Privileged Time', '% DPC Time', '% Interrupt Time', 'Processor Speed', 'Interrupts per Second',
         'CPU Effectiveness', 'Packets/Second', 'Packet Errors', 'Segments Retransmitted/Second']


def get_filename():
    global filename_original
    filename_iometer = tkFileDialog.askopenfilename()
    var_char_entry_original_filename.set(filename_iometer)
    filename_original = filename_iometer


def set_filename():
    global filename_display
    dir_filter_iometer = tkFileDialog.askdirectory().replace('/', '\\')
    var_char_entry_filter_filename.set(dir_filter_iometer)
    filename_display = os.path.join(dir_filter_iometer, "result-filter-iometer.csv")


def get_data(data, cpu_core_number_sub, worker_disk_sub, partition_undertest_number_sub):
    cpu_core_number = cpu_core_number_sub
    partition_undertest_number = partition_undertest_number_sub
    worker_disk = worker_disk_sub
    policy = data.iloc[2, 0]
    total_read_iops = data.iloc[8, 7]
    total_write_iops = data.iloc[8, 8]
    total_read_mb = data.iloc[8, 10]
    total_write_mb = data.iloc[8, 11]
    #    sum_read_iops, sum_write_iops, sum_read_mb, sum_write_mb = 0, 0, 0, 0
    # 确定需要读取数据的行
    dict_for_row = {}
    list_for_write_mb = []
    list_for_read_mb = []
    list_for_write_iops = []
    list_for_read_iops = []
    base_row_num = 11 + cpu_core_number
    # 创建储存数据的字典和列表
    for disk_count_sub in range(0, partition_undertest_number):
        dict_for_row['total_row_action_list_' + str(disk_count_sub)] = []

    for item in dict_for_row.keys():
        i = item[-1]
        for cpu_count in range(0, worker_disk):
            row_num_action = base_row_num + int(i) + cpu_count * (partition_undertest_number+1)
            dict_for_row[item].append(row_num_action)
    for item in dict_for_row.keys():
        read_iops_list = []
        write_iops_list = []
        read_mb_list = []
        write_mb_list = []
        for row_count in dict_for_row[item]:
            read_iops = data.iloc[row_count, 7]
            write_iops = data.iloc[row_count, 8]
            read_mb = data.iloc[row_count, 10]
            write_mb = data.iloc[row_count, 11]
            read_iops_list.append(float(read_iops))
            write_iops_list.append(float(write_iops))
            read_mb_list.append(float(read_mb))
            write_mb_list.append(float(write_mb))
        sum_read_iops = math.fsum(read_iops_list)
        sum_write_iops = math.fsum(write_iops_list)
        sum_read_mb = math.fsum(read_mb_list)
        sum_write_mb = math.fsum(write_mb_list)

        list_for_read_iops.append(sum_read_iops)
        list_for_write_iops.append(sum_write_iops)
        list_for_read_mb.append(sum_read_mb)
        list_for_write_mb.append(sum_write_mb)
    return policy, total_read_iops, total_write_iops, total_read_mb, total_write_mb, list_for_read_iops, list_for_write_iops, list_for_read_mb, list_for_write_mb


def filter_iometer():
    cpu_core_number = int(var_char_entry_cpucore.get())
    partition_undertest_number = int(var_char_entry_disk.get())
    worker_disk = int(var_char_entry_worker.get())
    filename = filename_original
    count = cpu_core_number + ((partition_undertest_number + 1) * worker_disk) + 12
    row_nrows = 12 + cpu_core_number + 5 + partition_undertest_number
    file_iometer_disk_name = pandas.read_csv(filename, sep=',', skiprows=6, na_filter=True, names=title,
                                             encoding='gbk', nrows=row_nrows)
    disk_name_list = []
    for disk_count in range(0, partition_undertest_number):
        row_number = 11 + cpu_core_number + disk_count
        disk_name = file_iometer_disk_name.iloc[row_number, 1]
        disk_name_list.append(disk_name)

    file_iometer = pandas.read_csv(filename, sep=',', skiprows=6, na_filter=True, names=title, encoding='gbk',
                                   chunksize=count)
    policy_list_display = []
    read_iops_total_display = []
    write_iops_total_display = []
    read_mb_total_display = []
    write_mb_total_display = []
    data = {}
    for disk_num in range(0, partition_undertest_number):
        data['total_data_' + str(disk_num)] = {}
        for disk_count_sub in ('read_iops', 'write_iops', 'read_mb', "write_mb"):
            data['total_data_' + str(disk_num)]['data_for_' + str(disk_count_sub)] = []

    for part_data in file_iometer:
        policy_display, total_read_iops_display, total_write_iops_display, total_read_mb_display, total_write_mb_display, list_for_read_iops_display, list_for_write_iops_display, list_for_read_mb_display, list_for_write_mb_display = get_data(
            part_data, cpu_core_number, worker_disk, partition_undertest_number)

        policy_list_display.append(policy_display)
        read_iops_total_display.append(total_read_iops_display)
        write_iops_total_display.append(total_write_iops_display)
        read_mb_total_display.append(total_read_mb_display)
        write_mb_total_display.append(total_write_mb_display)
        for disk in range(0, partition_undertest_number):
            data['total_data_' + str(disk)]['data_for_read_iops'].append(list_for_read_iops_display[disk])
            data['total_data_' + str(disk)]['data_for_write_iops'].append(list_for_write_iops_display[disk])
            data['total_data_' + str(disk)]['data_for_read_mb'].append(list_for_read_mb_display[disk])
            data['total_data_' + str(disk)]['data_for_write_mb'].append(list_for_write_mb_display[disk])

    data_dataframe_display = pandas.DataFrame(index=policy_list_display)
    for i in range(0, partition_undertest_number):
        data_dataframe_display['Read_Iops_for_' + disk_name_list[i]] = data['total_data_' + str(i)][
            'data_for_read_iops']
        data_dataframe_display['Write_Iops_for_' + disk_name_list[i]] = data['total_data_' + str(i)][
            'data_for_write_iops']
        data_dataframe_display['Read_Mbps_for_' + disk_name_list[i]] = data['total_data_' + str(i)]['data_for_read_mb']
        data_dataframe_display['Write_Mbps_for' + disk_name_list[i]] = data['total_data_' + str(i)]['data_for_write_mb']
    if os.path.exists(filename_display):
        os.remove(filename_display)
    data_dataframe_display.to_csv(filename_display, encoding='gbk', mode='w')
    tkMessageBox.showinfo('Info', '过滤结果创建成功，请去%s查看。然后点击退出手动关闭窗口'.decode('gbk') % filename_display)


root = Tkinter.Tk()
root.title("Iometer测试结果过滤工具".decode('gbk'))
root.geometry('800x600')
root.resizable(width=True, height=True)

frame_top_1 = Tkinter.Frame(root, height=20)
frame_top_1.pack(side=Tkinter.TOP)

frame_top_1_left = Tkinter.Frame(frame_top_1)
frame_top_1_left.pack(side=Tkinter.LEFT)

frame_top_1_middle = Tkinter.Frame(frame_top_1)
frame_top_1_middle.pack(side=Tkinter.LEFT)

frame_top_1_right = Tkinter.Frame(frame_top_1)
frame_top_1_right.pack(side=Tkinter.RIGHT)

Tkinter.Label(frame_top_1_left, text='请在如下如数CPU核心数'.decode('gbk'), bg='Red').pack(side=Tkinter.TOP)
var_char_entry_cpucore = Tkinter.StringVar()
Tkinter.Entry(frame_top_1_left, textvariable=var_char_entry_cpucore, width=30).pack(side=Tkinter.BOTTOM)

Tkinter.Label(frame_top_1_middle, text='请在如下输入Worker数量'.decode('gbk'), bg='Red').pack(side=Tkinter.TOP)
var_char_entry_worker = Tkinter.StringVar()
Tkinter.Entry(frame_top_1_middle, textvariable=var_char_entry_worker, width=30).pack(side=Tkinter.BOTTOM)

Tkinter.Label(frame_top_1_right, text='请在如下输入Iometer测试的盘符数'.decode('gbk'), bg='Red').pack(side=Tkinter.TOP)
var_char_entry_disk = Tkinter.StringVar()
Tkinter.Entry(frame_top_1_right, textvariable=var_char_entry_disk, width=30).pack(side=Tkinter.BOTTOM)

frame_top = Tkinter.Frame(root, height=20)
frame_top.pack(side=Tkinter.TOP)

frame_top_top = Tkinter.Frame(frame_top)
frame_top_top.pack(side=Tkinter.TOP)

frame_top_bottom = Tkinter.Frame(frame_top)
frame_top_bottom.pack(side=Tkinter.BOTTOM)

Tkinter.Label(frame_top_top, text='请点击如下按钮选择Iometer的原始数据文件'.decode('gbk'), bg='Red').pack()
var_char_entry_original_filename = Tkinter.StringVar()
Tkinter.Entry(frame_top_bottom, textvariable=var_char_entry_original_filename, width=40).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_top_bottom, text='选择文件'.decode('gbk'), command=get_filename, width=20).pack(side=Tkinter.RIGHT)

frame_middle = Tkinter.Frame(root, height=20)
frame_middle.pack()

frame_middle_top = Tkinter.Frame(frame_middle)
frame_middle_top.pack()

frame_middle_bottom = Tkinter.Frame(frame_middle)
frame_middle_bottom.pack(side=Tkinter.BOTTOM)

Tkinter.Label(frame_middle_top, text='请点击如下按钮选择Iometer过滤之后生成的文件地址'.decode('gbk'), bg='Red').pack()
var_char_entry_filter_filename = Tkinter.StringVar()
Tkinter.Entry(frame_middle_bottom, textvariable=var_char_entry_filter_filename, width=40).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_middle_bottom, text='选择文件'.decode('gbk'), command=set_filename, width=20).pack(side=Tkinter.RIGHT)

frame_bottom = Tkinter.Frame(root, height=20)
frame_bottom.pack()

Tkinter.Button(frame_bottom, text='GO'.decode('gbk'), width=20, command=filter_iometer).pack(side=Tkinter.LEFT)
Tkinter.Button(frame_bottom, text='退出'.decode('gbk'), width=20, command=root.destroy).pack(side=Tkinter.LEFT)
Tkinter.mainloop()

# batch_sacfile.py
# -*- coding: utf-8 -*-
# author : Sonder
# created : 12th May 2022
# version : 2.0
'''

This python script will do these things:

1. add information of head in sacfile
	stla stlo stel evla evlo evdp 
2. modify kcmpnm to LHZ
3. format sacfile name as 
	event.station.LHZ.sac

'''

# just checking
_author_ = 'Sonder M. W.'

from icecream import ic
import os
import argparse
import subprocess

station_cat = 'station_el.cat'
event_cat = 'event_14_depth.cat'
# beceuse of using event_14,
# the step of rename will be final

# get stla stlo stel from station.cat
def get_dic(catfile):
    lalo = ["lo", "la", "dp"]
    cat_dic = {}
    with open(catfile, 'r', encoding='utf-8') as f:
        for lines in f.readlines():
            line = lines.replace('\n', '').split()
            cat_dic[line[0]] = {lalo[i-1]: line[i] for i in range(1, 4)}

    return cat_dic


# batch dir
# ch ev?? st??
def batch_sac_ch_evst(work_dir, station_dic, event_dic):
    os.chdir(work_dir)
    # ch evla evlo evdp
    os.putenv("SAV_DISPLAY_COPYRIGHT", "0")
    s = "wild echo off \n"
    s += "r *.sac \n"
    s += "ch evla {} \n".format(event_dic['la'])
    s += "ch evlo {} \n".format(event_dic['lo'])
    s += "ch evdp {} \n".format(event_dic['dp'])
    s += "wh \n"

    # ch stla stlo stel
    for sta in station_dic:
        ic(sta)
        s += "r *{}* \n".format(sta)
        s += f"ch stla {station_dic[sta]['la']} \n"
        s += f"ch stlo {station_dic[sta]['lo']} \n"
        s += f"ch stel {station_dic[sta]['dp']} \n"
        s += "wh \n"

    s += "q \n"
    subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
    ic("finish ch event and station")
    os.chdir('..')
    ic()
        
# ch kcmpnm LHZ
def batch_sac_ch_kcmpnm(work_dir):
    os.chdir(work_dir)
    # ch evla evlo evdp
    ic(work_dir)
    os.putenv("SAV_DISPLAY_COPYRIGHT", "0")
    s = "wild echo off \n"
    s += "r *.sac \n"
    s += "ch kcmpnm LHZ \n"
    s += "wh \n"
    s += "q \n"
    subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
    ic("finish ch kcmpnm LHZ")
    os.chdir('..')
    ic()

def batch_sac_rename(work_dir):
    ic(work_dir)
    for filename in os.listdir(work_dir):
        namesplits = filename.split(".")
        new_namelist = [namesplits[i] for i in [1, 3, 6]]
        new_namelist.insert(0, work_dir[:12])
        new_name = ".".join(new_namelist)
        os.rename(work_dir+"/"+filename, work_dir+"/"+new_name)
    ic("finish rename file")
    os.rename(work_dir, work_dir[:12])
    ic("finish rename directory")

def get_parser():
    parser = argparse.ArgumentParser(
        description = "Version 2.0: change sac head  and filename in a work directory"
    )
    parser.add_argument(
        'work_dir',
        metavar = 'WORK_DIR',
        type = str,
        nargs = 1,
        help = 'the directory where to change sac head file',
    )
    # parser.add_argument(
    #     'fime_ext', metavar='FILE_EXT', type=str, nargs=1, help='file extension'
    # )
    return parser

def main():
    '''
    This will be called if the script is directly invoked.
    '''
    # adding commend line argument
    parser = get_parser()
    args = vars(parser.parse_args())

    # Set the variable work_dir with the first argument passed
    work_dir = args["work_dir"][0]

    station_dic = get_dic(station_cat)
    event_dic = get_dic(event_cat)

    batch_sac_ch_evst(work_dir, station_dic, event_dic[work_dir])
    batch_sac_ch_kcmpnm(work_dir)

    batch_sac_rename(work_dir)

if __name__ == "__main__":
    main()

# batch_sacfile_ch.py
# -*- coding: utf-8 -*-

'''
author  : sonder merak winona
version : 1.0.5
'''
'''

This py will plus stla stlo stel evla evlo evdp 
to head file in sac file.

'''
from icecream import ic
import os
import argparse
import subprocess

station_cat = 'station.cat' # lo la dp
event_cat = 'event.cat' # lo la dp

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
def batch_sac_ch(work_dir, station_dic, event_dic):
    os.chdir(work_dir)
    # ch evla evlo evdp
    ic("ching event")
    os.putenv("SAV_DISPLAY_COPYRIGHT", "0")

    s = "wild echo off \n"
    s += "r *sac \n"
    s += "lh evla {} \n".format(event_dic['la'])
    s += "lh evlo {} \n".format(event_dic['lo'])
    s += "lh evdp {} \n".format(event_dic['dp'])
    s += "wh \n"

    # ch stla stlo stel
    for sta in station_dic():
        s += "r *{}* \n".format(sta)
        s += f"lh stla {station_dic[sta]['la']} \n"
        s += f"lh stlo {station_dic[sta]['lo']} \n"
        s += f"lh stel {station_dic[sta]['dp']} \n"

    s += "q \n"
    subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
    ic("finish ch event and station")
    ic()
        


def get_parser():
    parser = argparse.ArgumentParser(
        description = "Version 1.0: change sac files' names in a work directory"
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

    batch_sac_ch(work_dir, station_dic, event_dic[work_dir])

if __name__ == "__main__":
    main()

# batch_sacfile_rename.py
# created: 6th April 2022

'''
This will batch rename a group of sac files in given directory,

time should be the same form as directory.

From 
TE.BD259.00.HHZ.D.202201011051.sac

To
20220011051.BD201.HHZ.sac
'''

# just checking
_author_ = 'Sonder M. W.'
_version_ = '1.0.2'

from icecream import ic
import argparse
import os

def batch_sac_rename(work_dir):
    ic(work_dir)
    for filename in os.listdir(work_dir):
        if os.path.splitext(filename)[1] == ".sac":
            ic(filename)
            namesplits = filename.split('.')
            new_namelist = [namesplits[i] for i in [1, 3, 6]]
            new_namelist.insert(0, work_dir)
            new_name = ".".join(new_namelist)
            os.rename(work_dir+"/"+filename, work_dir+"/"+new_name)
            ic("sucess rename")

    #print('rename is done')
    #print(os.listdir(work_dir))
    ic('rename is done')
    ic(os.listdir(work_dir))


def get_parser():
    parser = argparse.ArgumentParser(
        description = "Version 1.0: change sac files' names in a work directory"
    )
    parser.add_argument(
        'work_dir',
        metavar = 'WORK_DIR',
        type = str,
        nargs = 1,
        help = 'the directory where to change sac file names',
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

    batch_sac_rename(work_dir)


if __name__ == "__main__":
    main()



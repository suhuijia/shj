# coding=utf-8

import os
import time
import datetime

DB_HOST = 'xxx'
DB_USER = 'xxx'
DB_USER_PASSWD = 'xxx'
DB_NAME = './dbbackup/dbnames.txt'
BACKUP_PATH = './dbbackup/'

CURRENTDATE = time.strftime('%Y%m%d')


def run_backup():
    in_file = open(DB_NAME,"r")
    for dbname in in_file.readlines():
        dbname = dbname.strip()
        print("now starting backup database %s" %dbname)
        dumpcmd = "mysqldump -h" +DB_HOST + " -u"+DB_USER + " -p"+DB_USER_PASSWD+ " " +dbname+" > "+TODAYBACKUPPATH +"/"+dbname+".sql"
        print(dumpcmd)
        os.system(dumpcmd)
    file1.close()


def run_tar():
    compress_file = TODAYBACKUPPATH + ".tar.gz"
    compress_cmd = "tar -czvf " +compress_file+" "+DATETIME
    os.chdir(BACKUP_PATH)
    os.system("pwd")
    os.system(compress_cmd)
    print("compress complete!")
    #删除备份文件夹
    remove_cmd = "rm -rf "+TODAYBACKUPPATH
    os.system(remove_cmd)

while True:
    DATE = time.strftime('%Y%m%d')
    DATETIME = time.strftime('%Y%m%d-%H%M%S')
    TODAYBACKUPPATH = BACKUP_PATH + DATETIME
    if CURRENTDATE == DATE:
        time.sleep(600)
        continue
    else:
        CURRENTDATE = DATE
        print("createing backup folder!")
        if not os.path.exists(TODAYBACKUPPATH):
            os.makedirs(TODAYBACKUPPATH)

        print("checking for databases names file")
        pass

    if os.path.exists(DB_NAME):
        file1 = open(DB_NAME)
        print("starting backup of all db listed in file "+DB_NAME)
        run_backup()
        # run_tar()
        print("backup success!")
    else:
        print("database file not found..")
        exit()

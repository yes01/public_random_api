import os
from reptile import *
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler


def job_huya():
    logger.info("正在执行虎牙直播流数据更新...")
    jobs = "python /data/webapp/utils/up_huya.py"
    m3u_checker = "python /data/webapp/utils/m3uChecker.py"
    os.system(jobs)
    os.system(m3u_checker)
    logger.info("执行虎牙直播流数据更新定时任务-->success")


def job_douyu():
    logger.info("正在执行斗鱼直播流数据更新...")
    jobs = "python /data/webapp/utils/up_douyu.py"
    m3u_checker = "python /data/webapp/utils/m3uChecker.py"
    os.system(jobs)
    os.system(m3u_checker)
    logger.info("执行斗鱼直播流数据更新定时任务-->success")


def job_douyin():
    logger.info("正在执行抖音直播流数据更新...")
    jobs = "python /data/webapp/utils/up_douyin.py"
    m3u_checker = "python /data/webapp/utils/m3uChecker.py"
    os.system(jobs)
    os.system(m3u_checker)
    logger.info("执行抖音直播流数据更新定时任务-->success")


def job_bilibili():
    logger.info("正在执行B站直播流数据更新...")
    jobs = "python /data/webapp/utils/up_bilibili.py"
    m3u_checker = "python /data/webapp/utils/m3uChecker.py"
    os.system(jobs)
    os.system(m3u_checker)
    logger.info("执行B站直播流数据更新定时任务-->success")


def job():
    logger.info("正在执行直播流数据更新...")
    jobs_b = "python /data/webapp/utils/up_bilibili.py"
    jobs_hu = "python /data/webapp/utils/up_bilibili.py"
    jobs_douyin = "python /data/webapp/utils/up_douyin.py"
    jobs_douyu = "python /data/webapp/utils/up_douyu.py"
    os.system(jobs_b)
    logger.info("执行直播流数据更新定时任务-->success")


logger.info("定时任务启动...")
scheduler = BlockingScheduler()
# 采用corn的方式
scheduler.add_job(job_huya, 'cron', hour='19-23', minute='20')
scheduler.add_job(job_douyu, 'cron', hour='19-23', minute='40')
scheduler.add_job(job_douyin, 'cron', hour='19-23', minute='05')
scheduler.start()

#!/usr/bin/python
# -*-coding:utf-8-*-
from bs4 import BeautifulSoup
from paramDefine import *
from courseLearn import projectread

'''
模块名称：课程同步（方案二）
模块功能：实现远程培训系统中“我的项目”和“我的课程”下的课程学习（包括自测练习，自动检测）。
功能实现：利用系统中“同步课程状态“的漏洞实现课程学习一步完成。（但具体课程完成度为0）
'''


# B计划，B for beitai.
def planb(s):
    claim = input("A计划失效之日，备胎归来之时！ ")
    claim = claim.lower()
    if claim == "B":
        # 1.获取项目页面并打印出来
        project = s.get(project_url).content.decode("utf-8")
        # 2.根据用户选择的ID读取对应项目课程,读取课程ID，提交同步
        projectpickId = projectread(project)
        sysnCourse(projectpickId, s)
        return
    else:
        return


# 根据远程培训系统网页端“同步”按钮代码获取方法
def sysnCourse(id, s):
    data = {'projectId': id,
            'loginId': ''}
    page = s.get(course_url, params=data).content.decode("utf-8")
    Soup = BeautifulSoup(page, "html.parser")
    all_td_complete = Soup.find_all(name="td", class_="complete")
    passIds = ""
    for i in range(len(all_td_complete)):
        passIds += all_td_complete[i].get("id") + ","
    data = {"passIds": passIds}
    response = s.post(sysn_url, data=data)
    res = response.json()
    print(res)
    return

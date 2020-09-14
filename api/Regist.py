#!/usr/bin/python
# -*-coding:utf-8-*-

import re

from bs4 import BeautifulSoup
from api.paramDefine import *


class Regist:
    '''
    模块名称：项目/课程注册
    模块功能：实现远程培训系统中的项目/课程搜索并注册。
    @param s: 保存用户登陆成功状态的session  requsts.session()
    @param keyword：搜索课程关键词（可为空） str
    @param year：搜索课程年份（可为空） str
    '''
    def __init__(self, s, keyword, year):
        self.s = s
        self.keyword = keyword
        self.year = year
        self.loginId = self.getUserId()

    def regist(self, info):
        type = info['type']
        id = info['id']
        if type == 'project':
            regist_message = self.projectRegister(id)
        elif type == 'course':
            regist_message = self.courseRegister(id)
        return regist_message

    def search(self):
        projectInfos = self.projectSearch()
        courseInfos = self.courseSearch()
        infos = projectInfos + courseInfos
        return infos

    # 课程注册
    def courseRegister(self, courseId):
        data = {'loginId': self.loginId,
                'courseId': courseId
                }
        response = self.s.post(courseregister_url, data=data)
        regist_message = response.content.decode('utf-8')
        return regist_message

    # 项目注册
    def projectRegister(self, pid):
        # code含义未知，参考网页注册按钮java函数而确定为-1,等待进一步研究
        # code变动为0 原因未知 2020年3月27日
        code = 0
        data = {'loginId': self.loginId,
                'projectId': pid,
                'registCode': code}
        response = self.s.post(projectregister_url, data=data)
        regist_message = response.content.decode('utf-8')
        return regist_message

    # 获取用户ID，后续注册需要。
    def getUserId(self):
        page = self.s.get(student_url).content.decode('utf-8')
        Soup = BeautifulSoup(page, "html.parser")
        userid = Soup.find(onclick=re.compile(r"logout\(\'\d+\'\)"))
        loginId = userid.get('onclick').split("'")[1]
        return loginId

    # 项目搜索，显示50条 pagesize控制。
    # @return [projectName,projectId]
    def projectSearch(self):
        userId = self.loginId
        year = self.year
        keyword = self.keyword
        pageNum = ''
        categoryId = ''
        pageSize = '50'
        # ckey为必须项目，其他可忽略。loginID会控制搜索范围（空值搜索更多）
        data = {'loginId': userId,
                'ckey': keyword,
                'year': year,
                'pageNum': pageNum,
                'categoryId': categoryId,
                'pageSize': pageSize
                }
        c = self.s.post(projectsearch_url, data=data)
        ctext = c.content.decode("utf-8")
        Soup = BeautifulSoup(ctext, "html.parser")
        all_projectname = Soup.find_all('a', class_='font_tit')
        all_projectid = Soup.findAll(
            name="div", attrs={"id": re.compile(r"projectList(\w+).?")})
        all_projectstatus = Soup.find_all('a',class_='font_xa2')
        all_projectname_len = len(all_projectname)
        projectInfos = []
        if all_projectname_len != 0:
            for i in range(all_projectname_len):
                projectName = all_projectname[i].get_text()
                projectId = all_projectid[i].get('id')[12:]
                projectStatus = all_projectstatus[i].get_text().strip()
                if projectStatus == '开始学习':
                    projectStatus = '已注册'
                elif projectStatus == '注册项目':
                    projectStatus = '未注册'
                projectInfo = {
                    'type': 'project',
                    'name': projectName,
                    'id': projectId,
                    'status':projectStatus
                }
                projectInfos.append(projectInfo)
        elif all_projectname_len == 0:
            projectInfos = []
        return projectInfos

    # 课程搜索。
    # @return [courseName,courseId]
    def courseSearch(self):
        loginId = self.loginId
        keyword = self.keyword
        year = self.year
        courseTag = ''  # 标签  暂不实现
        pageNum = ''
        # ckey为必须项目，其他可忽略。
        data = {'loginId': loginId,
                'ckey': keyword,
                'year': year,
                'pageNum': pageNum,
                'courseTag': courseTag
                }
        c = self.s.post(coursesearch_url, data=data)
        ctext = c.content.decode("utf-8")
        Soup = BeautifulSoup(ctext, "html.parser")
        all_coursename = Soup.find_all('a', class_='font_tit')
        all_courseid = Soup.find_all(
            'div', attrs={'id': re.compile("clbutton(\w+).?")})
        all_coursestatus = Soup.find_all('a',class_ ='font_xa2')
        all_coursename_len = len(all_courseid)
        courseInfos = []
        if all_coursename_len != 0:
            for i in range(all_coursename_len):
                courseName = all_coursename[i].get_text()
                courseId = all_courseid[i].get('id')[8:]
                courseStatus = all_coursestatus[i].get_text()
                if courseStatus == '开始学习':
                    courseStatus = '已注册'
                elif courseStatus == '注册课程':
                    courseStatus = '未注册'
                courseInfo = {
                    'type': 'course',
                    'name': courseName,
                    'id': courseId,
                    'status':courseStatus
                }
                courseInfos.append(courseInfo)
        elif all_coursename_len == 0:
            courseInfos = []
        return courseInfos

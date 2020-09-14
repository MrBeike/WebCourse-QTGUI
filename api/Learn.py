#!/usr/bin/python
# -*-coding:utf-8-*-
import random
import re

from bs4 import BeautifulSoup
from api.paramDefine import *
from math import ceil

from api.Test import Test
from api.Notify import Notify

class Learn:
    '''
    模块名称：课程学习
    模块功能：实现远程培训系统中的课程学习，包括视频轨迹完成。
    @param s: 保存用户登陆成功状态的session  requsts.session()
    '''
    def __init__(self,s):
        self.s = s
        self.notify = Notify()
        self.studentCenter()

    # 访问项目和课程前需先访问学员中心，否则无法获取用户头像等参数导致freemaker模板出错（2020年9月14日 HZJ反馈）
    def studentCenter(self):
        studentCenter_page = self.s.get(studentCenter_url).content.decode('utf-8')
            
    def projectReader(self):
        '''
        获取登陆后“我的项目”网页信息，并筛选出项目信息。
        @return projectLists：  用户所有项目信息  list [{,,,},{,,,}]
        '''
        project_page = self.s.get(project_url).content.decode('utf-8')
        Soup = BeautifulSoup(project_page, "html.parser")
        # 读取所有TD calss = cal_td标签项目
        all_tds = Soup.find_all('td', class_="cal_td")
        # 将TD内文字遍历并按8分组写入数组 
        all_tds_len = len(all_tds)
        all_tds_group = int(all_tds_len / 8)
        projectLists = []
        for i in range(all_tds_group):
            # 每组数据列表初始化
            projectList = []
            for j in range(8):
                id_text = str(all_tds[i * 8].get('id'))
                td_text = all_tds[j + i * 8].get_text().strip()
                projectList.append(td_text)
            # 删除最后一个无用链接内容（项目中心），并加上项目ID
            del projectList[-1]
            projectList.append(id_text)
            #projectList = [ "项目编号", " 项目名称 ", "项目开始---结束时间", "课程数", "总学时", "总学分", "完成状态", "项目ID"]
            projectDict = {
                'name':projectList[1], 
                'period':projectList[2],
                'time':projectList[4],
                'status':projectList[6],
                'id':projectList[7]
            }
            projectLists.append(projectDict)
        return projectLists

    def courseReader(self):
        '''
        读取“我的课程”下的课程
        @return courseLists： 用户课程*信息 list [{,,,},{,,,}]   *用户课程  并非所有，实际数量因网页列表显示控制（因数量调整意义不大，故未实现）
        '''
        page = self.s.get(myproject_url).content.decode('utf-8')
        Soup = BeautifulSoup(page, "html.parser")
        # 读取所有TR class = add_app_list标签项目
        all_trs = Soup.find_all("tr", class_="add_app_list")
        courseLists = []
        for trs in all_trs:
            # tr标签内包含着所有信息，第一行tr:courseId,后8行td包含课程其他信息[其中2，3，7有用]
            courseId = str(trs.get('id'))[0:32]
            tds = trs.find_all("td", class_="cal_td")
            courseList = []
            for td in tds:
                td_text = td.get_text().strip()
                courseList.append(td_text)
            # courseDict.keys() = ["课程名称", "学时", "完成状态", "课程ID"]
            courseDict = {
                'name':courseList[1],
                'time':courseList[2],
                'status':courseList[6],
                'id':courseId
            }
            courseLists.append(courseDict)
        return courseLists

    def projectDetailReader(self,id):
        '''
        读取指定项目下的具体课程
        @param id： 项目ID  str
        @return courseLists： 指定项目包含的所有课程信息 list [{,,,},{,,,}]
        '''
        data = {'projectId': id,
                'loginId': ''}
        page = self.s.get(course_url, params=data).content.decode("utf-8")
        Soup = BeautifulSoup(page, "html.parser")
        # 读取所有TR class = add_app_list标签项目
        all_trs = Soup.find_all("tr", class_="add_app_list")
        all_td_time = Soup.findAll(name="td", attrs={"id": re.compile(r"PERIOD(\w+).?")})
        all_td_name = Soup.findAll(name="td", attrs={"style": "text-align:left"})
        # 将TR内文字遍历写入数组
        all_trs_len = len(all_trs)
        courseLists = []
        for j in range(all_trs_len):
            id_text = str(all_trs[j].get("id"))
            courseInfo = self.getCourseStatue(id_text)
            time = all_td_time[j].get_text().strip()
            name = all_td_name[j].get_text().strip()
            # 截取32位课程代码
            id_text = id_text[0:32]
            # courseDict.keys() = ["课程名称", "学时", "课程ID", "已学时间", "测试成绩", "完成标志"]
            courseDict = {
                'name':name,
                'time':time,
                'id':id_text,
                'learnTime':round(eval(courseInfo['learnTime']) / 3600),
                'score':courseInfo['totalScore'],
                'finished':courseInfo['flagCourseFinish']
            }
            courseLists.append(courseDict)
        return courseLists

        if totalperiod / 8 >= 1:
            warning = "请注意，该项目一般学习时间为%d工作日\n!" % ceil(totalperiod / 8)
            print(warning * 3)
        return courseLists

    def learn(self,courseLists):
        '''
        模拟网页逻辑完成课程学习,包括视频轨迹的实现、测试自动完成等。
        @param courseLists：待学习的课程相关信息 list [{,,,},{,,,}] (单个课程学习时 list.__len__ = 1)
        '''
        s = self.s
        for courseList in courseLists:
            courseId = courseList['id']
            courseTime = courseList['time']
            courseTime = str(int(float(courseTime) * 3600 + random.randint(1000, 2000)))
            data = {"courseId": courseId,
                    "studyTime": courseTime}
            response = s.post(timeSave_url, data=data)
            learn_message = response.content.decode("utf-8")
            self.notify.add('学习时间',learn_message)
        self.points = self.pointDetect(courseLists)
        # 课程轨迹实现部分
        self.learnRecord()
        # 自动测试实现部分
        self.testDetect()
        return self.notify

    def pointDetect(self,courseLists):
        '''
        课程节点检测
        @param courserId: 课程ID str
        @return points: 课程节点信息  list [{,,,},{,,,},{,,,}] 
        '''
        s = self.s
        points = []
        for courseList in courseLists:
            courseId = courseList['id']
            data = {"params.courseId": courseId}
            response = s.post(courseware_url, data=data)
            courseware = response.content.decode("utf-8")
            pointcollect = re.findall(r"openLearnResItem\((.*)\)", courseware)
            for item in pointcollect:
                pointId = eval(item.split(",")[0])
                pointType = eval(item.split(",")[1])
                if pointType in("video", "courseware", "test"):
                    # point.keys() = [课程Id,节点Id，节点类型] 
                    point = {
                        'courseId':courseId,
                        'pointId':pointId,
                        'pointType': pointType
                    }
                    points.append(point)
        return points

    def learnRecord(self):
        '''
        增加视频轨迹功能，同步当前学习视频轨迹。
        '''
        points = self.points
        s = self.s
        videoPoints = []
        for point in points:
            pointType = point['pointType']
            if pointType == "video":
                videoPoint = {
                    'courseId':point['courseId'], 
                    'pointId': point['pointId']
                }
                videoPoints.append(videoPoint)
        videoPoint_lens = len(videoPoints)
        if videoPoint_lens:
            for videoPoint in videoPoints:
                # 预学习1秒，否则无法获取当前视频总时长
                savedataPre = {"videoStudyRecord.courseId": videoPoint['courseId'],
                            "videoStudyRecord.itemId": videoPoint['pointId'],
                            "videoStudyRecord.startTime": "00:00:00",
                            "videoStudyRecord.endTime": "00:00:01",
                            "videoStudyRecord.videoIndex": "0",
                            "videoStudyRecord.studyTimeLong": "1"}
                s.post(saveRecord_url, data=savedataPre)
                # 获取当前视频时间长度
                querydata = {"params.courseId": videoPoint['courseId'],
                            "params.itemId": videoPoint['pointId']}
                query = s.post(learnRecord_url, data=querydata).content
                learnRecordSoup = BeautifulSoup(query, "html.parser")
                totalLearnTime = learnRecordSoup.findAll(name="span", attrs={"name": "end_time"})[-1].get_text()
                totalLearnTimeNums = totalLearnTime.split(":")
                hours = int(totalLearnTimeNums[0])
                minutes = int(totalLearnTimeNums[1])
                seconds = int(totalLearnTimeNums[2])
                totalLearnTimeNum = hours * 3600 + minutes * 60 + seconds
                # 提交数据
                savedata = {"videoStudyRecord.courseId": videoPoint['courseId'],
                            "videoStudyRecord.itemId": videoPoint['pointId'],
                            "videoStudyRecord.startTime": "00:00:00",
                            "videoStudyRecord.endTime": totalLearnTime,
                            "videoStudyRecord.videoIndex": "0",
                            "videoStudyRecord.studyTimeLong": totalLearnTimeNum}
                save = s.post(saveRecord_url, data=savedata)
                learnRecord_message = save.content.decode("utf-8")
                self.notify.add('视频轨迹',learnRecord_message)

    def testDetect(self):
        '''
        自动检测课程中是否含有test,并调用autoTestAll函数做题
        '''
        points = self.points
        testIds = []
        for point in points:
            pointType = point['pointType']
            if pointType == "test":
                testIds.append(point['pointId'])
        if testIds:
            test = Test(self.s,testIds)
            test_notify = test.test()
            self.notify.extend(test_notify)
    
    def getCourseStatue(self,courseId):
        '''
        获取指定课程学习相关信息（可单个，也可多个Id用逗号连接）
        '''
        s = self.s
        data = {"electiveIds": courseId}
        response = s.post(courseStatue_url, data=data)
        json = response.json()
        if json['success'] == 'true':
            data = json['data']
            print(data)
            for key in data:
                courseId = key
                courseInfo = data[key]
                courseInfo['courseId'] = courseId
            return courseInfo
        else:
            print('返回数据出错')
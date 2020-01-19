#!/usr/bin/python
# -*-coding:utf-8-*-
import os

# ----------------------------------------------------------------------------------------#
# ************************************** 参数维护 *******************************************#
# ----------------------------------------------------------------------------------------#
'''
1.网址维护
'''
# 我的课程地址
myproject_url = 'http://11.129.195.195/learning/entity/student/student_studentCourseList.action?page.pageSize=80&page.orderBy=createDate'
# 课程课件地址
mycourse_url = "http://11.129.195.195/learning/entity/student/student_getMyProjectCourses.action"
# 登陆表单提交地址
login_url = "http://11.129.195.195/center/center/login_login.action"
# 我的项目地址
project_url = "http://11.129.195.195/learning/entity/student/student_sear" \
              "chProject.action?page.pageSize=80&page.orderBy=createDate"
# 项目课件地址
course_url = "http://11.129.195.195/learning/entity/student/student_getMy" \
             "ProjectCourses.action"
# 用户页面，ID所在页面
student_url = "http://11.129.195.195/learning/entity/student/student_index.action"
# 项目注册地址
projectregister_url = "http://11.129.195.195/entity/cms/peCms_eleProject.action"
# 课程注册地址
courseregister_url = "http://11.129.195.195/entity/cms/peCms_eleCourse.action"
# 项目搜索地址
projectsearch_url = "http://11.129.195.195/entity/first/peCmsNoLogin_getProject.action"
# 课程搜索地址
coursesearch_url = "http://11.129.195.195/entity/first/peCmsNoLogin_getCourse.action"
# 课程同步地址
sysn_url = "http://11.129.195.195/learning/entity/student/student_sysnCourseState.action"
# 查看答案地址
answerPage_url = "http://11.129.195.195/space/course/test/coursewareTest_intoTestAnswerPage.action"
# 进入测试地址
testPage_url = "http://11.129.195.195/space/course/test/coursewareTest_intoTestPage.action"
# 再做一遍地址
testRedo_url = "http://11.129.195.195/space/course/test/coursewareTest_intoRedoTestPage.action"
# 提交答案地址
submitPage_url = "http://11.129.195.195/space/course/test/coursewareTest_handSubmitPaper.action"
# 课程课件地址（包括自测）
courseware_url = "http://11.129.195.195/space/learn/learn/templatetwo/courseware_index.action"
# 课件学习时间保存地址
timeSave_url = "http://11.129.195.195/space/course/study/learningTime_saveLearningTime.action"
# 课程视频地址
videocontent_url = "http://11.129.195.195/space/learn/learn/templatetwo/content_video.action"
coursewarecontent_url = "http://11.129.195.195/space/learn/learn/templatetwo/content_courseware.action"
learnRecord_url = "http://11.129.195.195/space/learn/learn/common/video_learn_record_detail.action"
saveRecord_url = "http://11.129.195.195/space/course/study/learningTime_saveVideoLearnDetailRecord.action"
courseStatue_url = "http://11.129.195.195/learning/entity/student/student_getStuCourseStatus.action"
'''
2.其他参数维护
'''
# 数据库定义
# 1.Table User
user_create = '''
CREATE TABLE IF NOT EXISTS USER( 
ACCOUNT  NOT NULL UNIQUE ON CONFLICT REPLACE,
 PASSWD  NOT NULL,
 NAME    NOT NULL);
'''
# user_add_data  = '\"replace into user(account,passwd,name) values ({loginId},{passwd},{name})\"'
user_add_data = '\"REPLACE INTO USER (ACCOUNT,PASSWD,NAME) VALUES (?,?,?)\",(data["loginId"], data["passwd"], data["name"])'
user_read_data = 'select * from user'
userSQL = {'db_name': 'userinfo.db', 'create_table': user_create, 'add_data': user_add_data,
           'read_data': user_read_data}

# 2.Table Course


# 欢迎词？
title = '''
=====================================================================================================================================================
                                             |************网络课程学习软件************|
                                             |              by 菜菜子                |
                                             1.本程序仅供代码学习研究使用，请勿用于其他用途
                                             2.可在网页直接注册项目，或使用本系统注册项目
                                             3.本程序目前无GUI制作计划，界面就凑合着看吧
                                             4.本程序部分功能无错误处理流程，如遇异常，请检查输入并重开程序
                                             5.PlanB跳过学习和做题，修改成绩单显示完成，有效性未测试，慎用
=====================================================================================================================================================
'''

'''
3.序
'''
xy = " 这个软件的想法很早就在脑子里了，只是一直懒得动手，拖了好久。\n " \
     "2018年4月29日，我见到了一个难以忘怀的人。短暂的相见固然美好，但我面对的现实却是残酷的分离。我给不了你想要的，" \
     "所以懦弱的选择了逃避。\n " \
     "那段时间真的是难熬，以至于凌晨2点都未能入睡，索性起来做点事，来度过这无奈的夜晚。然后便有了这个小项目。\n " \
     "          我很想你，心瑜小可爱。---菜菜子             "

xeroxYor = "我因为爱你，所以常常想跟你道歉。 \n" \
           "我的爱沉重，污浊，里面带有许多令人不快的东西，比如悲伤，忧愁，自怜，绝望，\n" \
           "我的心又这样脆弱不堪，自己总被这些负面情绪打败，好像在一个沼泽里越挣扎越下沉。 \n" \
           "而我爱你，就是想把你也拖进来，却希望你救我。\n" \
           "     ————所以，最后你选择了逃脱，留下我，困在原地。  "


# just for XY.
def missU(s,u=xy):
    print(u)
    return

#and diss myself
def dissM(s,m=xeroxYor):
    print(m)
    return



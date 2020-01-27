#!/usr/bin/python
# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
from paramDefine import *



class Test:
    '''
    模块名称：课程测试
    模块功能：自动完成所学课程测试（如果有）。
    @param：s: 保存用户登陆成功状态的session  requsts.session()
    @param：testId: 课程内试卷ID str
    '''
    def __init__(self,s,testIds):
        self.s = s
        self.testIds = testIds
        self.autoTest()

    def autoTest(self):
        testIds = self.testIds
        for testId in testIds:
            try:
                self.itemId = testId
                # pagefix(id)  这条当时为了修复BUG而写，如今反而导致程序出错？
                submitPackge = self.testPage()
                self.pagefix()
                answers = self.ansewerPage()
                self.submitPage(answers, submitPackge)
                self.resultPage()
            except AttributeError:
                continue
        return


    # 通过itemId获取一份试卷，并读取试卷三参数（testId,itemId,historyId）
    def testPage(self):
        s = self.s
        itemId = self.itemId
        testPageData = {"params.itemId": itemId}
        testPageResponse = s.post(testPage_url, data=testPageData)
        testPageContent = testPageResponse.content.decode('utf-8')
        testSoup = BeautifulSoup(testPageContent, "html.parser")
        testId = testSoup.find(name="input", attrs={"name": "testId"}).get("value")
        itemId = testSoup.find(name="input", attrs={"name": "itemId"}).get("value")
        historyId = testSoup.find(name="input", attrs={"name": "historyId"}).get("value")
        submitPackge = {"testId": testId,
                        "itemId": itemId,
                        "historyId": historyId,
                        "myAnswers": "",
                        }
        return submitPackge


    # 模拟初次做题，产生答案。解决ansewerPage无法正确获取答案的Bug 2018年6月12日16
    def pagefix(self):
        s = self.s
        itemId = self.itemId
        pagefixData = {"params.itemId": itemId}
        s.post(answerPage_url, data={"itemId": itemId})
        pagefixResponse = s.post(testPage_url, data=pagefixData)
        pagefixContent = pagefixResponse.content.decode('utf-8')
        pagefixSoup = BeautifulSoup(pagefixContent, "html.parser")
        courseId = pagefixSoup.find(name="input", attrs={"name": "courseId"}).get("value")
        historyId = pagefixSoup.find(name="input", attrs={"name": "historyId"}).get("value")
        pagefixPackge = {"params.itemId": itemId,
                        "params.historyId": historyId,
                        "params.courseId": courseId,
                        }
        s.post(answerPage_url, data={"itemId": itemId})  # 为了解决测试页面空白导致做题程序无法正常运行做的修补，执行顺序？ 2018年8月22日10:29:39
        s.post(testRedo_url, data=pagefixPackge)
        return


    # 通过itemId获取最近一次的答案
    def ansewerPage(self):
        s = self.s
        itemId = self.itemId
        answerPageData = {"itemId": itemId}
        answerPageResponse = s.post(answerPage_url, data=answerPageData)
        answerPageContent = answerPageResponse.content.decode('utf-8')
        answerSoup = BeautifulSoup(answerPageContent, "html.parser")
        all_answers = answerSoup.findAll("div", class_="test_item_key_tit")
        answer = ""
        answers = ""
        for i in range(len(all_answers)):
            answer += all_answers[i].get_text().split("：")[1] + "|"
            answers = answer[0:-1]
        return answers


    # 提交获取的试卷答案
    def submitPage(answers, submitPackge):
        s = self.s
        submitPackge["myAnswers"] = answers
        submitPageData = submitPackge
        submitPageResponse = s.post(submitPage_url, data=submitPageData)
        submitPageContent = submitPageResponse.content.decode('utf-8')
        # print("服务器返回信息:", submitPageContent)
        # TODO 测试-提交试卷-消息提示？
        return

    #测试结果页面，反馈成绩
    def resultPage(self):
        s = self.s
        itemId = self.itemId
        resultPageData = {"params.itemId": itemId}
        resultPageResponse = s.post(testPage_url, data=resultPageData)
        resultPageContent = resultPageResponse.content.decode('utf-8')
        resultSoup = BeautifulSoup(resultPageContent, "html.parser")
        thisRecord = resultSoup.find("span", class_="record_num_this").get_text()
        topRecord = resultSoup.find("span", class_="record_num_top").get_text()
        # print("本次成绩：", thisRecord, "最高成绩：", topRecord)
        # TODO 测试-测试结果-消息提示
        return

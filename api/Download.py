#!/usr/bin/python
# -*-coding:utf-8-*-
import re
import time

from bs4 import BeautifulSoup

from Wget import Wget
from Learn import pointDetect
from paramDefine import *



class Download:
    '''
    模块名称：视频下载
    模块功能：实现远程培训系统中的课程视频下载。
    @param s: 保存用户登陆成功状态的session  requsts.session()
    @param courseLists：项目/课程ID合集 list
    '''
    def __init__(self,s,courseLists)
        self.s = s
        points = pointDetect(courseLists)
        self.fileInfoLists = self.getVideoUrl(points)


    def getVideoUrl(self,points):
        '''
        通过分析节点信息，获取视频标题和下载地址
        @param points: 课程节点信息  list [{,,,},{,,,}]
        @return fileInfoLists: 视频文件信息合集  list [{,,,},{,,,}]
        '''
        s = self.s
        fileInfoLists = []
        for point in points:
            data = {"params.courseId": point['courseId'],
                    "params.itemId": point['pointId'],
                    "params.templateStyleType": "false",
                    # 待解决科学计数法可能的问题----
                    "_t": time.time() * 1000,
                    }
            if point['pointType'] == "video":
                response = s.post(videocontent_url, data=data)
                videoContent = response.content.decode("utf-8")
                videocontentSoup = BeautifulSoup(videoContent, "html.parser")
                videoTitle = videocontentSoup.find(name="div", attrs={'class': 's_title s_videoti'}).get_text()
                videoUrl = videocontentSoup.find("input", id="videoResource").get("value")
                # 视频是否能从本地服务器下载？newfile(通过Fiddler分析得知)
                try:
                    # urlPrefix = re.findall(r"resource = \"(.*)\"\+", videoContent)
                    urlPrefix = "http://11.129.199.51/NewFile.jsp?path=/content2"
                    videoUrl = urlPrefix + videoUrl.replace("/space", "")
                    videoUrlHeaders = s.head(videoUrl).headers
                    videoUrl = videoUrlHeaders["Location"]
                except TypeError:
                    urlPrefix = "http://11.129.195.195"
                    videoUrl = urlPrefix + videoUrl
                    fileInfoDict = {
                        'title':videoTitle,
                        'url':videoUrl
                    }
                fileInfLists.append(fileInfoDict)
            elif points['pointType'] == "courseware":
                response = s.post(coursewarecontent_url, data=data)
                coursewareContent = response.content.decode("utf-8")
                coursewareContentSoup = BeautifulSoup(coursewareContent, "html.parser")
                coursewareUrl = coursewareContentSoup.find("iframe").get("src")
                coursewareUrlHeaders = s.head(coursewareUrl).headers
                location = coursewareUrlHeaders["Location"]
                url1 = re.findall(r"(\d+\.\d+\.\d+\.\d)", location)[0]
                url2 = re.findall(r"service=/(.*?)&", location)[0]
                # 获取新页面地址
                # coursewareUrl ="http://"+ url1 + "/" + url2.replace("index.htm","imsmanifest1.xml") + "_=" + str(time.time()*1000)
                coursewareUrl = "http://" + url1 + "/" + url2.replace("index.htm", "imsmanifest1.xml")
                response = s.get(coursewareUrl).content.decode("utf-8")
                coursewareSoup = BeautifulSoup(response, "html.parser")
                videoTitleCase = coursewareSoup.findAll(name="item", attrs={"identifierref": re.compile(r"res(\d+)")})
                videoUrlCase = coursewareSoup.findAll(name="resource", attrs={"identifier": re.compile(r"res(\d+)")})
                for i in range(len(videoTitleCase)):
                    videoTitle = re.findall(r"<title>(.*)</title>", str(videoTitleCase[i]))[0]
                    videoUrl = videoUrlCase[i].get("href").replace("index.htm", "1.mp4")
                    videoUrl = coursewareUrl.replace("imsmanifest1.xml", videoUrl)
                    fileInfoDict = {
                        'title':videoTitle,
                        'url':videoUrl
                    }
                    fileInfoLists.append(fileInfoDict)
        return fileInfoLists

    # TODO 界面 文件浏览器 另存为
    def saveToPage(self):
        '''
        将课程下载信息保存到本地网页，包含标题和下载地址
        '''
        downloadLists =self.downloadLists
        with open("videolist.html", 'wb') as f:
            prelog = '<head><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"></head>'
            f.write(prelog.encode())
            for downloadList in downloadlists:
                fileName = downloadlists['title']
                fileUrl = downloadlists['url']
                log = "<p>" + "【" + str(i) + "】" + fileName + "</p>" + "<a href=" + fileUrl + ">" + fileUrl + "</a></br>"
                f.write(log.encode())
            saveToPage_message = "已经生成含有视频地址和名称的文件：videolist.html"
            # TODO 消息提示
        return

    # TODO 界面 文件浏览器 另存为
    def videoDownload(self,downloadLists):
        '''
        调用Wget下载所需文件
        @param downloadLists: 待下载文件信息  list [{,,,},{,,,}]
        '''
        for downloadList in downloadlists:
            fileUrl = downloadlist['url']
            fileName = downloadlist['title'] + ".mp4"
            Wget().download(fileUrl, fileName)

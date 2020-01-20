# search_result = [{'type': 'project', 'name': '我不知道你在想什么，还是那个季节那条街，噢噢噢噢，我还在这里干什么，我不知你是在看我啊', 'id': 111111111111111}, {
#     'type': 'project', 'name': 'mikeqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq', 'id': 2}, {'type': 'course', 'name': 'mikenqqqqqqqqqqqqqqqqq', 'id': 3}]


import os ,sys

myFolder = os.path.split(os.path.realpath(__file__))[0]
sys.path = [os.path.join(myFolder, 'ui'),
            os.path.join(myFolder, 'resource'),
            os.path.join(myFolder, 'api')
            ] + sys.path

os.chdir(myFolder)

from Login import Login().login as login

username = '342901199112091813'
password = '12091813'
rememberFlag = False
j,k,l = Login().login(username,password,rememberFlag)
print(j,k,l)
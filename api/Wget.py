#!/usr/bin/python
# encoding=utf-8
import os
import re
import requests
import sys
import time



class Wget:
    '''
    模块名称：wget下载组件（源码来自github wget）
    模块功能：实现简单的下载功能。
    '''
    def __init__(self, config={}):
        self.config = {
            'block': int(config['block'] if 'block' in config else 1024),
        }
        self.total = 0
        self.size = 0
        self.filename = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:39.0) Gecko/20100101 Firefox/39.0',
            'HOST': '11.129.195.195',
            'Range': 'bytes=0-4'
        }

    def touch(self, filename):
        with open(filename, 'w') as fin:
            pass

    def remove_nonchars(self, name):
        (name, _) = re.subn(r'[\\\/\:\*\?\"\<\>\|]', '', name)
        return name

    def support_continue(self, url):
        try:
            r = requests.head(url, headers=self.headers)
            crange = r.headers['Content-Range']
            self.total = int(re.match(r'^bytes 0-4/(\d+)$', crange).group(1))
            return True
        except:
            pass
        try:
            self.total = int(r.headers['Content-Length'])
        except:
            self.total = 0
        return False

    def download(self, url, filename, headers={}):
        finished = False
        block = self.config['block']
        local_filename = self.remove_nonchars(filename)
        tmp_filename = local_filename + '.downtmp'
        flag = self.support_continue(url)
        size = self.size
        total = self.total
        if flag:  # 支持断点续传
            try:
                with open(tmp_filename, 'rb') as fin:
                    self.size = int(fin.read())
                    size = self.size + 1
            except:
                self.touch(tmp_filename)
            finally:
                headers['Range'] = "bytes=%d-" % (self.size,)
        else:
            self.touch(tmp_filename)
            self.touch(local_filename)

        r = requests.get(url, stream=True, verify=False, headers=self.headers)
        if total > 0:
            print("[+] Size: %dKB" % (total / 1024))
        else:
            print("[+] Size: None")
        start_t = time.time()
        with open(local_filename, 'ab+') as f:
            f.seek(self.size)
            f.truncate()
            try:
                for chunk in r.iter_content(chunk_size=block):
                    if chunk:
                        f.write(chunk)
                        size += len(chunk)
                        f.flush()
                    sys.stdout.write('\b' * 64 + 'Now: %d, Total: %s' % (size, total))
                    sys.stdout.flush()
                finished = True
                os.remove(tmp_filename)
                spend = int(time.time() - start_t)
                speed = int((size - self.size) / 1024 / spend)
                sys.stdout.write('\n下载完成!\n共用时: %ss, 平均速度: %sk/s\n' % (spend, speed))
                sys.stdout.flush()
            except:
                import traceback
                print(traceback.print_exc())
                print("\n下载暂停.\n")
            finally:
                if not finished:
                    with open(tmp_filename, 'wb') as ftmp:
                        ftmp.write(str(size).encode())

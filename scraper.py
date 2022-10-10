'''
Downloads all the songs from general conference
'''

from selenium import webdriver
from selenium.common import exceptions as E
from selenium.webdriver.support.ui import Select
import time, sys, os
import requests
log = print

class GV:
    driver = None

def GetDriver():
    if GV.driver is not None:
        return GV.driver
    log('Starting browser...')
    driver = GV.driver = webdriver.Chrome()
    driver.set_window_size(1500, 800)
    return driver

def ElWait(elFunc, selector):
    # for some reason, implicit waits don't work in FF :(
    while 1:
        try:
            return elFunc(selector)
        except E.NoSuchElementException:
            time.sleep(0.25)
            # TODO: add a max-wait thing

def ES(what):
    return GetDriver().execute_script(what)

def LinkByText(t):
    return ElWait(GetDriver().find_element_by_link_text, t)

def Download(url, filename):
    if os.path.exists(filename):
        return
    log('DL:', url, '-->', filename)
    with open(filename + '.tmp', 'wb') as f:
        f.write(requests.get(url).content)
    time.sleep(0.1)
    os.rename(filename + '.tmp', filename)

for year in range(2008, 2023):
    for month in ('april', 'october'):
        url = f'https://churchofjesuschrist.org/study/manual/music-from-{month}-{year}-general-conference'
        #log(url)
        browser = GetDriver()
        browser.get(url)
        LinkByText('Contents') # just wait til something we expect has loaded
        for songURL in ES("return Array.from(document.querySelectorAll('a.list-tile')).map(el => el.href)"):
            filename = songURL.split('/')[-1].split('?')[0] + '.mp3'
            if os.path.exists(filename):
                continue
            log('Loading', songURL)
            browser.get(songURL)
            time.sleep(2)
            try:
                browser.find_element_by_css_selector('button[aria-label="Audio Player"]').click() # click the listen button
            except E.NoSuchElementException:
                # this happens with e.g. https://www.churchofjesuschrist.org/study/manual/music-from-april-2008-general-conference/2008-04-for-the-beauty-of-the-earth
                log('Skipping!')
                continue

            time.sleep(0.25)
            browser.find_element_by_css_selector('button[aria-label="More"]').click() # click the 3 dots
            mp3URL = LinkByText('Download Vocals').get_attribute('href')
            Download(mp3URL, filename)

sys.exit()



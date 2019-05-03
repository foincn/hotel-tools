#!/usr/bin/python
# -*- coding: UTF-8 -*- 
# filename: webdriver.py


from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

import string
import zipfile
 
def create_proxyauth_extension(proxy_host, proxy_port,
                               proxy_username, proxy_password,
                               scheme='http', plugin_path=None):
    """代理认证插件
 
    args:
        proxy_host (str): 你的代理地址或者域名（str类型）
        proxy_port (int): 代理端口号（int类型）
        proxy_username (str):用户名（字符串）
        proxy_password (str): 密码 （字符串）
    kwargs:
        scheme (str): 代理方式 默认http
        plugin_path (str): 扩展的绝对路径
 
    return str -> plugin_path
    """
    
 
    if plugin_path is None:
        plugin_path = 'vimm_chrome_proxyauth_plugin.zip'
 
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
 
    background_js = string.Template(
    """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "${scheme}",
                host: "${host}",
                port: parseInt(${port})
              },
              bypassList: ["foobar.com"]
            }
          };
 
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
 
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "${username}",
                password: "${password}"
            }
        };
    }
 
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """
    ).substitute(
        host=proxy_host,
        port=proxy_port,
        username=proxy_username,
        password=proxy_password,
        scheme=scheme,
    )
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
 
    return plugin_path



proxyauth_plugin_path = create_proxyauth_extension(
    proxy_host = 'http-dyn.abuyun.com',
    proxy_port = 9020,
    proxy_username = 'H557HX96M9Y0G15D',
    proxy_password = '8370941EDCC9ED02'
)




option = ChromeOptions()
#option.add_argument("--proxy-server=http://202.20.16.82:10152")
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_extension(proxyauth_plugin_path)



class webdriver():
    def __init__(self, limit=15):
        self.create_driver()
        self.limit = limit
    def create_driver(self):
        self.driver = Chrome('./chromedriver', options=option)
        self.driver.set_window_size(800, 900)
        self.count = 0
    def delete_driver(self):
        self.driver.exit()
    def get_page(self, url):
        self.driver.get(url)
        html = self.driver.page_source
        self.count += 1
        if self.count == self.limit:
            self.create_driver()
            print('重启浏览器')
        return html
    


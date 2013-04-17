# -*- coding: utf-8 -*-

# Copyright (C) 2013 ~ 2014 rapidhere
#
# Author:     rapidhere@gmail.com
# Maintainer: rapidhere@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Fix httplib's IncompleteRead Exception bug
import httplib
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

import err,constant,login,sign,json
import cookielib,sys,urllib2,urllib,BeautifulSoup,re,time

# Exceptions
class NotLoginError(err.rpbtman_Error):
    def __init__(self):
        err.rpbtman_Error.__init__(self,
            "Must login first!",
            "Haven't Login into baidu"
        )

class Tieba:
    def __init__(self,usr='',pss=''):
        self.set_username(usr)
        self.set_password(pss)

        self.cookiejar = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))

        self.login_man = login.Login(self.opener)
        self.sign_man = sign.SignMan(self.opener)

    def login(self):
        """
        Login into baidu
        Must set username and password at first
        """
        if self.login_man.has_login():
            return

        self.login_man.set_username(self.get_username())
        self.login_man.set_password(self.get_password())

        self.login_man.sign_in()

        if self.login_man.has_login():
            print "Login succeeded!"

    def sign(self,tb_kwd):
        """
        Sign the specified tieba
        Must login first
        """
        if not self.login_man.has_login():
            raise NotLoginError()
        self.sign_man.sign(tb_kwd)

        print "Sign in tieba %s succeeded!" % tb_kwd

    def sign_all(self,interval = 3):
        """
        Sign all tieba in your favourite list
        Must login first
        Note :
            If there are any error occuered ,the sign will be interrupted
            You must setup the interval,
            Beacause if you sign up too fast,the server will deny the request
        """
        if not self.login_man.has_login():
            raise NotLoginError()

        favo_list = self.get_favolist()
        for tb in favo_list:
            self.sign(tb)
            time.sleep(interval)

    def get_favolist(self):
        """
        return the favo_list of you tieba's keyword
        Encoded by utf-8
        Must login first
        """
        if not self.login_man.has_login():
            raise NotLoginError()

        url = 'http://tieba.baidu.com/i/sys/enter?ie=utf-8&kw=%s' % urllib2.quote(self.get_username().decode(constant.CODEC).encode("gbk"))
        buf = self.opener.open(url).read()

        favo_list_buf = re.findall(r'\$_likeForum=(.*?);',buf)[0]
        favo_list = []
        for b in json.loads(favo_list_buf):
            favo_list.append(b['name'].encode(constant.CODEC))
        return favo_list

    def set_username(self,uname): self.username = uname
    def set_password(self,pword): self.password = pword

    def get_username(self): return self.username
    def get_password(self): return self.password

if __name__ == "__main__":
    try:
        tb = Tieba("","")
        tb.login()
        for t in tb.get_favolist():
            print t
    except err.EXC_rpbtman,e:
        print e.FormatStr()

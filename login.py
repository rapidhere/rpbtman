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

import urllib,urllib2,cookielib,copy,re
import err

# Constant
BaiduLoginURL = r"https://passport.baidu.com/v2/api/?login"
BaiduLoginTokenURL = r"https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false"

HTTPHeader = {
    "Accept"            : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset"    : "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Language"   : "en-US,en;q=0.8",
    "Content-Type"      : "application/x-www-form-urlencoded",
    "User-Agent"        : "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.22 (KHTML, like Gecko) Ubuntu Chromium/25.0.1364.160 Chrome/25.0.1364.160 Safari/537.22",
    "Connection"        : "keep-alive",
    "Cache-Control"     : "max-age=0",
}

Datas = {
    "username"  : "",
    "password"  : "",
    "charset"   : "utf-8",
    "index"     : "0",
    "isPhone"   : "false",
    "loginType" : "1",
    "mem_pass"  : "on",
    "safeflg"   : "0",
    "tpl"       : "mn",
    "token"     : "",
}

# Exceptions:
class LoginError(err.rpbtman_Error):
    def __init__(self,ename,info):
        err.rpbtman_Error.__init__(self,ename,"Error while logining: " + info)

class NeedVerificatonCode(LoginError):  # Error = 257
    def __init__(self):
        LoginError.__init__(self,
            "Need Verification Code",
            "passport.baidu.com request a verification code,maybe you've login too much today"
        )

class PasswordError(LoginError):        # Error = 4
    def __init__(self):
        LoginError.__init__(self,
            "Password Error",
            "Wrong Password,login request denied"
        )

class InvalidUser(LoginError):          # Error = 2
    def __init__(self):
        LoginError.__init__(self,
            "Username doesn't exist",
            "Please check your syntax"
        )

class UnexpectedLoginError(LoginError):
    def __init__(self,ecode):
        LoginError.__init__(self,
                "Unexpected Error",
                "Unknow Error while logining into baidu,server return Error code %d" % ecode
            )
        self.ecode = ecode

class Login:
    """
    Set up the usrname and password and then login into baidu
    """
    def __init__(self,usrname = '',psswrd = ''):
        self.data = copy.deepcopy(Datas)

        self.set_username(usrname)
        self.set_password(psswrd)

        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

    def set_username(self,usrname): self.data["username"] = usrname
    def set_password(self,psswrd): self.data["password"] = psswrd

    def getToken(self):
        req = urllib2.Request(
                url = BaiduLoginURL,
                headers = HTTPHeader,
                data = urllib.urlencode(self.data)
            )
        self.opener.open(req)

        buf = self.opener.open(BaiduLoginTokenURL).read().decode("utf-8")
        return re.findall("login_token='(\w+)'",buf)[0]

    def sign_in(self):
        """
        Sign in into www.baidu.com
        You must set username and password at first

        NOTE :
            Cannot deal with vertification code now
            So if you enter the wrong password many times
            You have to enter the vertification code
            and that's would be awful beacause you can't get the vcode
        """
        self.data["token"] = self.getToken()

        req = urllib2.Request(
                url = BaiduLoginURL,
                headers = HTTPHeader,
                data = urllib.urlencode(self.data)
            )

        buf = self.opener.open(req).read().decode("utf-8")
        error_code = re.findall("error\=(\d+)",buf)

        if error_code:
            error_code = int(error_code[0])
            if error_code == 0:
                pass
            elif error_code == 257:
                raise NeedVerificatonCode()
            elif error_code == 4:
                raise PasswordError()
            elif error_code == 2:
                raise InvalidUser()
            else:
                raise UnexpectedLoginError(error_code)

if __name__ == "__main__":
    try:
        log = Login("844122492","QQcd9412")
        log.sign_in()
    except err.EXC_rpbtman,x:
        print x.FormatStr()

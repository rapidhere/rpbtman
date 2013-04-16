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
import err,constant
import urllib2,urllib,re

class SignError(err.rpbtman_Error):
    def __init__(self,eid,info):
        err.rpbtman_Error.__init__(self,
            "Sign Error ID :%d" % eid,
            info
        )
        self.eid = eid

class SignMan:
    def __init__(self,opener):
        self.opener = opener

    def get_tbs(self,kwd):
        kwd = kwd.decode(constant.CODEC).encode("gbk")
        buf = self.opener.open("http://tieba.baidu.com/f?ie=utf-8&kw=" + urllib.quote(kwd)).read()
        return re.findall("PageData.tbs = \"(\w+)\"",buf)[0]

    def sign(self,kwd):
        tbs = self.get_tbs(kwd)

        req = urllib2.Request(
                url = "http://tieba.baidu.com/sign/add",
                headers = constant.HTTPHeader,
                data = urllib.urlencode({"tbs":tbs,"kw":kwd,"ie":"utf-8"})
            )
        buf = self.opener.open(req).read().decode("utf-8")
        ret = re.match(
                r"""
                \{
                    "no":(?P<no>\d*),
                    "error":"(?P<error>.*)",
                    "data":"(?P<data>.*)"
                \}
                """,
                buf,
                flags = re.VERBOSE | re.DOTALL
            )
        if not ret:
            return

        ret = ret.groupdict()
        ret["no"] = int(ret["no"])
        ret["error"] = eval("u'" + ret["error"] + "'").encode(constant.CODEC)
        raise SignError(ret["no"],ret["error"])

if __name__ == "__main__":
    try:
        sm = SignMan(urllib2.build_opener())
        sm.sign("time")
    except err.EXC_rpbtman,e:
        print e.FormatStr()

__author__ = 'Junfeng'
# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
Function:
【已解决】BeautifulSoup已经获得了Unicode的Soup但是print出来却是乱码
http://www.crifan.com/beautifulsoup_already_got_unicode_soup_but_print_messy_code

Author:     Crifan Li
Version:    2013-05-30
Contact:    http://www.crifan.com/contact_me/
"""

import urllib
import urllib.request

from bs4 import BeautifulSoup


def scrapeW3school():
    html = urllib.request.urlopen("http://www.zhihu.com/question/30073693");
    # soup = BeautifulSoup(html); #此句效果是一样的：
    #实测结果是：不加fromEncoding，也是可以自动正确（去判断原始的字符编码为GB2312，然后去）解析（出后来的Unicode的soup）的
    soup = BeautifulSoup(html, from_encoding="GB2312");
    #print "soup=",soup;
    allTdSoup = soup.find_all("class", "zu-global-notify");
    print("type(allTdSoup)=", type(allTdSoup))  #type(allTdSoup)= <class 'BeautifulSoup.ResultSet'>，但是实际上算是个List
    print("len(allTdSoup)=", len(allTdSoup))  #len(allTdSoup)= 32，此处List的长度是32
    print("allTdSoup=", allTdSoup)
    # allTdSoup= [<td>row 1, cell 1</td>, <td>row 1, cell 2</td>, <td>row 2, ......, <td><a href="/tags/tag_tfoot.asp">&lt;tfoot&gt;</a></td>
    # , <td>瀹氫箟琛ㄦ牸鐨勯〉鑴氥€?/td>, <td><a href="/tags/tag_col.asp">&lt;col&gt;</a></td>, <td>瀹氫箟鐢ㄤ簬琛ㄦ牸鍒楃殑灞
    # 炴€с€?/td>, <td><a href="/tags/tag_colgroup.asp">&lt;colgroup&gt;</a></td>, <td>瀹氫箟琛ㄦ牸鍒楃殑缁勩€?/td>]

    #此处，看起来是乱码，但是实际上，此处得到的allTdSoup是个列表，而其中的每个soup，虽然内部编码都是正常的unicode了
    #但还是会打印出来乱码，那是因为：
    #1.先看官网的解释：
    #http://www.crummy.com/software/BeautifulSoup/bs3/documentation.zh.html
    #"当你调用__str__,prettify或者renderContents时， 你可以指定输出的编码。默认的编码(str使用的)是UTF-8。"
    #所以：
    #此处，对于去打印allTdSoup，即去打印一个soup的List，所以，针对List中的每个soup（其本质是个对象），而将其输出为字符串的话，默认是调用其__str__属性
    #所以就相当于：
    #针对allTdSoup中的每个soup：
    #   调用该soup的__str__获得对应的字符串（表示的该soup的内容）
    #最终组合输出你所看到的["xxx", "xxx", ...]之类的结果，
    #其中，"xxx"，就是对应的每个soup.__str__的结果
    #而此处的每个soup的__str__的值：
    #如官网所述，默认是UTF-8的编码
    #所以，此处获得的字符串是UTF-8编码的字符串，
    #所以print输出到此处cmd
    #而cmd是GBK编码
    #所以，将UTF-8编码的字符，在GBK的cmd中显示，就显示出乱码了
    #其中：
    #（1）如果对于cmd是GBK不了解，去看：
    #设置字符编码：简体中文GBK/英文
    #http://www.crifan.com/files/doc/docbook/soft_dev_basic/release/html/soft_dev_basic.html#cmd_encoding
    #（2）如果对于GBK，UTF-8本身不了解，去看：
    #字符编码详解
    #http://www.crifan.com/files/doc/docbook/char_encoding/release/html/char_encoding.html
    #（3）针对于soup本身，其实已经是Unicode编码，所以可以通过官网所说的，指定__str__输出时的编码为GBK，以使得此处正确显示非乱码的中文
    for eachTdSoup in allTdSoup:
        print("type(eachTdSoup)=", type(eachTdSoup))  #type(eachTdSoup)= <type 'instance'>，说明类型是BeautifulSoup的实例instance
        print("eachTdSoup.string=", eachTdSoup.string)  #输出soup的string属性，即该tag中的字符串内容部分，其本身已经是Unicode，所以可以正常输出非乱码的中文
        print("type(eachTdSoup.string)=", type(
            eachTdSoup.string))  #但是要注意一下，此处不是Unicode类型，而是：type(eachTdSoup.string)= <class 'BeautifulSoup.NavigableString'>
        print("eachTdSoup=", eachTdSoup)  #直接输出soup本身，所以相当于：eachTdSoup.__str__ == eachTdSoup.__str__("UTF-8")，所以遇到中文时是乱码
        print("eachTdSoup.renderContents()=", eachTdSoup.renderContents())  #直接输出内容本身，默认也是用的是UTF-8，所以遇到中文时也是乱码
        print("eachTdSoup.__str__('GBK')=", eachTdSoup.__str__('GBK'))  #专门指定了GBK编码，所以可以正常显示非乱码的中文
        #摘录其中部分输出：
        # type(eachTdSoup)= <type 'instance'>
        # eachTdSoup.string= row 1, cell 1
        # type(eachTdSoup.string)= <class 'BeautifulSoup.NavigableString'>
        # eachTdSoup= <td>row 1, cell 1</td>
        # eachTdSoup.renderContents()= row 1, cell 1
        # eachTdSoup.__str__('GBK')= <td>row 1, cell 1</td>
        # ......
        # type(eachTdSoup)= <type 'instance'>
        # eachTdSoup.string= 定义表格列的组。
        # type(eachTdSoup.string)= <class 'BeautifulSoup.NavigableString'>
        # eachTdSoup= <td>瀹氫箟琛ㄦ牸鍒楃殑缁勩€?/td>
        # eachTdSoup.renderContents()= 瀹氫箟琛ㄦ牸鍒楃殑缁勩€
        # eachTdSoup.__str__('GBK')= <td>定义表格列的组。</td>
        #
        #（4）另外，关于BeautifulSoup可以根据html中的charset猜测其编码的事情，不了解的去看：
        #【整理】关于HTML网页源码的字符编码（charset）格式（GB2312，GBK，UTF-8，ISO8859-1等）的解释
        #http://www.crifan.com/summary_explain_what_is_html_charset_and_common_value_of_gb2312_gbk_utf_8_iso8859_1


if __name__ == "__main__":
    scrapeW3school();
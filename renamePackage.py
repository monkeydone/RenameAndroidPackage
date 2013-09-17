#!/usr/bin/env python
#coding:utf-8
#author:lijunjie
#email:lijunjieone@gmail.com

import os
import codecs
import re
import sys

from optparse import OptionParser
from xml.etree import ElementTree as ET
import xml.dom.minidom as minidom



class Project:
    def __init__(self):
        pass


class RenameAndroidPackage:
    def __init__(self,p):
        self.project=p

    def modifyAndroidManifest(self):
        fx1=fixXml("%s/AndroidManifest.xml"%self.project.build_path)
        self.project.old_package_name=fx1.getOldPackageName()
        fx1.renamePackageName(self.project.new_package_name)
        fx1.saveXml()
    def modifySource(self,old_package_name):
        source_path="%s/src/"%(self.project.build_path)
        package_name_path=old_package_name.replace(".","/")
        for a,b,c in os.walk(source_path):
            if ".svn" not in a:
                for i in c:
                    file_path="%s/%s"%(a,i)
                    if ".java" in i and a.endswith(package_name_path):
                        replaceString(file_path,"%s;"%(old_package_name),"%s;\nimport %s.R;"%(old_package_name,self.project.new_package_name))
                    elif ".java" in i:
                        replaceString(file_path,"%s.R"%old_package_name,"%s.R"%self.project.new_package_name)

        
    def modifyResource(self,old_package_name):
        res_path="%s/res/"%(self.project.build_path)
        for a,b,c in os.walk(res_path):
            if ".svn" not in a:
                for i in c:
                    if ".xml" in i:
                        file_path="%s/%s"%(a,i)
                        replaceString(file_path,"http://schemas.android.com/apk/res/%s"%old_package_name,"http://schemas.android.com/apk/res/%s"%self.project.new_package_name)

    def modify(self):
        self.modifyAndroidManifest()
        self.modifySource(self.project.old_package_name)
        self.modifyResource(self.project.old_package_name)

class fixXml:
    def __init__(self,xml_path):
        self.xml_path=xml_path
        self.root=ET.parse(xml_path).getroot()
        self.ns_android="http://schemas.android.com/apk/res/android"
        ET._namespace_map["http://schemas.android.com/apk/res/android"]="android"
    def getOldPackageName(self):
        return self.root.attrib["package"]

    def renamePackageName(self,new_package):
        self.old_package=self.root.attrib["package"]
        self.new_package=new_package
        self.root.attrib["package"]=self.new_package
        for i in self.root:
            if i.tag=="application":
                app=i

        name_attr="{%s}name"%(self.ns_android)
        auth_attr="{%s}authorities"%(self.ns_android)
        if name_attr in app.attrib:
            b=app.attrib[name_attr]
            app.attrib[name_attr]="%s.%s"%(self.old_package,b)
            #print "test",app.tag,app.attrib[name_attr]

        for  i in app:
            if name_attr in i.attrib:
                b=i.attrib[name_attr]
                if b.startswith("."):
                    x="%s%s"%(self.old_package,b)
                    i.attrib[name_attr]=x
            if i.tag=="provider":
                i.attrib[auth_attr]=i.attrib[auth_attr].replace(self.old_package,self.new_package)
                b=i.attrib[name_attr]
                if not b.startswith(self.old_package) or not "." in b:
                    i.attrib[name_attr]="%s.%s"%(self.old_package,b)

        
    def formatXml(self):
        rough_string=ET.tostring(self.root,'utf-8')
        reparsed=minidom.parseString(rough_string)
        self.content=reparsed.toprettyxml(indent=' ',encoding='utf-8')
        return self.content
    def saveXml(self):
        self.formatXml()
        f=codecs.open(self.xml_path,"w","utf-8")
        content2=""
        for i in self.content.split("\n"):
            if i.strip() != '':
                content2+=i
                content2+="\n"
        f.write(content2)
        f.close()
def replaceString(filename,src_text,dest_text):
    print filename,src_text,dest_text
    src=u'%s'%src_text
    dest=u'%s'%dest_text

    aa=codecs.open(filename,"r","utf-8")
    a=aa.read()
    aa.close()

    b=re.sub(src,dest,a)
    c=codecs.open(filename,"w","utf-8")
    c.write(b)
    c.close()

def handleParameters(fakeArgs):
    msg_usage="%prog [ -p <project_path> ] [ -o <old_name> ] [ -n <new_name> ] "
    optParser=OptionParser(msg_usage)
    optParser.add_option("-p","--project_path",action="store",type="string",dest="project_path")
    optParser.add_option("-o","--old_package_name",action="store",type="string",dest="old_package_name")
    optParser.add_option("-n","--new_package_name",action="store",type="string",dest="new_package_name",default="")

    return optParser.parse_args(fakeArgs)
 


if __name__=="__main__":
    arg=sys.argv[1:]
    if len(arg)==0:
        arg.append("--help")
    print arg
    options,args=handleParameters(arg)
     

    p=Project()
    p.build_path=options.project_path
    p.old_package_name=options.old_package_name
    p.new_package_name=options.new_package_name
    #p.build_path="/tmp/b"
    #p.old_package_name="com.mx"
    #p.own_package_name="com.mx.test"
    r=RenameAndroidPackage(p)
    r.modify()

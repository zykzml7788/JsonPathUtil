#-*- coding: UTF-8 -*-
# 一个jsonpath调试工具

__author__ = '楷楷'
__date__ = '2019/06/06'

from tkinter import *
import jsonpath
import json
import tkinter.font as tkfont



def get_value(source_str,pattern):
    '''
    匹配Jsonpath结果
    :param source_str: 目标字符串
    :param pattern: jsonpath表达式
    :return: 匹配结果
    '''
    if not pattern.startswith("$."):
        write_result("JSONPATH表达式格式错误!")
        raise Exception("JSONPATH表达式格式错误!")
    result = jsonpath.jsonpath(source_str, pattern)
    return result if result else None

def write_result(msg):
    '''
    写入结果
    :param msg: 需要抛出的提示
    :return:
    '''
    result_text.delete("1.0", END)
    result_text.insert("1.0", msg)

def get_result():
    '''
    获取匹配结果
    :return:
    '''
    jsonstr = json_text.get("1.0",END)
    print(jsonstr)
    if jsonstr == "\n":
        write_result("JSON不能为空！")
        return
    try:
        jsonstr = json.loads(jsonstr)
        try:
            result = get_value(jsonstr,jsonpath_str.get())
            write_result("匹配到如下结果:\n\n{}".format('\n'.join(result) if result!=None else "null"))
        except Exception as e:
            write_result("出现异常啦~~异常原因:{}".format(e))
    except Exception as e:
        write_result("请检查JSON格式是否正确！")
        print(e)

def beauti_json():
    '''
    格式化JSON
    :param s: json字符串
    :return:
    '''
    if json_text.get('1.0',END) == '\n':
        write_result("JSON不能为空！")
        return
    try:
        s = json.dumps(json.loads(json_text.get('1.0',END)), indent=4,ensure_ascii=False)
        json_text.delete('1.0',END)
        json_text.insert('1.0',s)
        write_result("JSON格式化成功！")
    except:
        write_result("JSON格式错误,格式化失败！")

window = Tk() # 创建窗口实例
window.title("JsonPath调试工具——楷楷  V1.0") # 设置窗口标题
win_width = window.winfo_screenwidth() # 屏幕宽度
win_height = window.winfo_screenheight()  # 屏幕高度
window.geometry("{}x{}".format(win_width,win_height)) # 设置窗口大小
window.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认


frame = Frame(window) # 创建主页面Frame
frame.pack()

#json的窗口
json_frame = Frame(frame)
label = Label(json_frame, text="在线JsonPath调试", bg="black",fg="white", font=("微软雅黑",15,"bold"), width=win_width, height=3,anchor="w").pack()
json_text = Text(json_frame, width=win_width, height=25,font=("微软雅黑",10))
scroll = Scrollbar(json_frame)
# 将滚动条填充
scroll.pack(side=RIGHT,fill=Y)
json_text.insert("1.0","请在此处填写JSON")
json_text.pack(side=LEFT,fill=Y)
# 将滚动条与文本框关联
scroll.config(command=json_text.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
json_text.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框
json_frame.pack(side=TOP)

#jsonpath表达式填写窗口
pattern_frame = Frame(frame)
jsonpath_label = Label()
jsonpath_str = Variable() # 绑定变量
jsonpath_str.set("jsonpath表达式")
pattern = Entry(pattern_frame,width=int(win_width*0.03),textvariable=jsonpath_str,font=("微软雅黑",12)).pack(side=LEFT)
gs_btn = Button(pattern_frame,text="Beautiful JSON",command=beauti_json,font=("微软雅黑",12,"bold"))
btn = Button(pattern_frame,text="调试",command=get_result,font=("微软雅黑",12,"bold"))
gs_btn.pack(padx=10)
gs_btn.pack(side=RIGHT)
btn.pack(padx=10)
btn.pack(side=RIGHT)
pattern_frame.pack(side=TOP)

#匹配结果窗口
result_frame = Frame(frame)
result_text = Text(result_frame,width=win_width, height=50,font=("微软雅黑",10))
result_text.insert("1.0","匹配结果在此展示")
scroll = Scrollbar(result_frame)
# 将滚动条填充
scroll.pack(side=RIGHT,fill=Y)
result_text.pack(side=LEFT,fill=Y)
# 将滚动条与文本框关联
scroll.config(command=result_text.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
result_text.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框

result_frame.pack(side=TOP)
window.mainloop()
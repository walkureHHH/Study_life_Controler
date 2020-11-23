import os
import json
import time
import shutil
import pandas
import colorama
colorama.init()
from sys import argv
from prettytable import PrettyTable

def init(time_type,switch):
    courses=[]
    course_info=[]
    if switch=='T':
        info_switch=True
    elif switch=='F':
        info_switch=False
    PATH=os.getcwd()
    timetable_type=int(time_type)
    
    # generate folders and conf files
    num = 1
    while True:
        a = input(colorama.Fore.YELLOW+'name of course %d (. to finish): '%num + colorama.Fore.RESET)
        if a == '':
            pass
        elif a == '.':
            break
        else:
            if info_switch == True:
                while True:
                    b = input(colorama.Fore.CYAN+'info for course %d : '%num  + colorama.Fore.RESET)
                    if b == '':
                        pass
                    else:
                        break
            num+=1
            courses.append(a)
            if info_switch==True:
                course_info.append(b)
    os.mkdir(PATH+'/'+'Assignment')
    os.mkdir(PATH+'/'+'Resourse')
    os.mkdir(PATH+'/'+'Note')
    os.mkdir(PATH+'/'+'.controler.config')
    for i in courses:
        os.mkdir(PATH+'/'+'Assignment'+'/'+i)
    for j in courses:
        os.mkdir(PATH+'/'+'Resourse'+'/'+j)
    for p in courses:
        os.mkdir(PATH+'/'+'Note'+'/'+p)

    # begin generate timetable(.csv)
    if timetable_type==1:
        week=['Monday','Tuesday','Wednesday','Thursday','Friday']
    if timetable_type==2:
        week=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    while True:
        time_span=input('Time span(example:"8-21"):')
        if time_span != '':
            break
    begin_time=int(time_span.split('-')[0])
    end_time=int(time_span.split('-')[1])
    hours=[m for m in range(begin_time,end_time+1)]
    course_string=''
    index=0
    index_list=['']
    for course in courses:
        course_string+='['+str(index)+']'+course+' | '
        index_list.append(str(index))
        index+=1
    f1=open(PATH+'/'+'.controler.config/timetable.csv',encoding='utf-8',mode='a')
    for hour in hours:
        print(colorama.Back.RED+'The course in %d:00 - %d:00:'%(hour,hour+1)+colorama.Back.RESET)
        print(colorama.Fore.GREEN+'('+course_string+')'+colorama.Fore.RESET)
        temp1=[]
        temp2=[]
        for day in week:
            print('for '+colorama.Back.RED+day + colorama.Back.RESET)
            while True:
                in_of_course=input(colorama.Fore.RED+'Input the index of courses: ' + colorama.Fore.RESET)
                if in_of_course not in index_list:
                    a = input('Are you sure? Y for yes, N for reinputing: ')
                    if a == "Y":
                        break
                    elif a == 'N':
                        pass
                else:
                    break
            venue=input(colorama.Fore.BLUE+'The venue of it: ' + colorama.Fore.RESET)
            if in_of_course in index_list:
                if in_of_course != '':
                    temp1.append(courses[int(in_of_course)])
                else:
                    temp1.append('-')
            else:
                temp1.append(in_of_course)
            if venue=='':
                temp2.append('-')
            else:
                temp2.append(venue)
        string1=''
        for n in temp1:
            string1+=n+','
        string1+='\n'
        string2=''
        for o in temp2:
            string2+=o+','
        string2+='\n'
        f1.write(string1)
        f1.write(string2)
    f1.close()
    f = open(PATH+'/'+'.controler.config/conf',encoding='utf-8',mode='w')
    json_dict={'courses':courses,'information':course_info,'timetable type':timetable_type,'info_switch':info_switch,'begin time':begin_time,'end time':end_time}
    json_data=json.dumps(json_dict,sort_keys=True,indent=4)
    f.write(json_data)
    f.close()

def show_timetable(num_of_each_rows):
    PATH=os.getcwd()
    timetable=pandas.read_csv(PATH+'/.controler.config/timetable.csv',header=None)
    with open(PATH+'/'+'.controler.config/conf','r',encoding='utf-8') as f:
        json_dict=json.load(f,encoding='utf-8')
    if json_dict['timetable type']==1:
        num_of_days=5
        days=['Monday','Tuesday','Wednesday','Thursday','Friday']
    elif json_dict['timetable type']==2:
        num_of_days=7
        days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    if num_of_each_rows>num_of_days:
        num_of_each_rows=num_of_days
    begin_time=json_dict['begin time']
    end_time=json_dict['end time']
    x = PrettyTable()
    time_column=[]
    for k in range(begin_time,end_time+1):
        time_column.append('%d:00-%d:00'%(k,k+1))
        time_column.append(' ')
    x.add_column('Time',time_column)
    for j in range(0,num_of_days):
        x.add_column(days[j],timetable[j].tolist())
    num = 0
    for i in range(0,int(num_of_days/num_of_each_rows)):
        field=['Time']
        for l in range(num,num+num_of_each_rows):
            field.append(days[l])
        print(x.get_string(fields=field))
        num+=num_of_each_rows
    if num != num_of_days:
        field=['Time']
        for m in range(num,num_of_days):
            field.append(days[m])
        print(x.get_string(fields=field))


def resourse(download_path):
    PATH=os.getcwd()
    with open(PATH+'/'+'.controler.config/conf','r',encoding='utf-8') as f:
        json_dict=json.load(f,encoding='utf-8')
    
    if download_path=="[default]":
        try:
            download_path=json_dict['default download path']
        except:
            print('please init default path first, use "cler resourse your/default/path/"')
            return
    else:
        if download_path.endswith('/'):
            pass
        else:
            download_path+='/'
        json_dict['default download path']=download_path
        with open(PATH+'/'+'.controler.config/conf','w',encoding='utf-8') as f:
            json.dump(json_dict,f,sort_keys=True,indent=4)
    
    courses=json_dict['courses']
    support_format=['pdf','doc','docx','ipynb','c','cpp','py','java','ppt','pptx','mp3','mp4']      # available resourse format
    course_string=''
    index=0
    index_list=['']
    for course in courses:
        course_string+='['+str(index)+']'+course+' | '
        index_list.append(str(index))
        index+=1
    print(colorama.Back.RED+"Now default download PATH is %s"%download_path+colorama.Back.RESET)
    set_before=set(os.listdir(download_path))
    count = 0
    resourse_file=set()
    print(course_string)
    index=input(colorama.Fore.YELLOW+'Choose the index of the course which these files belong to: '+colorama.Fore.RESET)
    course=courses[int(index)]

    while True:
        try:
            while True:
                num=count%6
                set_after=set(os.listdir(download_path))
                diff=set_after^set_before
                for i in diff:
                    for j in support_format:
                        try:
                            if i.split('.')[1]==j:
                                resourse_file.add(i)
                        except:
                            pass
                print('\rtotal: %03d    '%len(resourse_file)+'waitting'+num*'.'+(5-num)*' '+'    (Ctrl-c to finish)',end='')
                time.sleep(1)
                count+=1
        except KeyboardInterrupt:
            resourse_file_list=list(resourse_file)
            for k in range(0,len(resourse_file_list)):
                if k ==0 :
                    print('\n'+resourse_file_list[k])
                else:
                    print(resourse_file_list[k])
                shutil.move(download_path+resourse_file_list[k],PATH+'/Resourse/'+course+'/'+resourse_file_list[k])
            resourse_file=set()
            if_break=input(colorama.Fore.YELLOW+'\nFinish? Y/N: '+colorama.Fore.RESET)
            if if_break=='Y':
                break
            elif if_break=='N':
                pass

def bill(name,bill_):
    try:
        append_list=[float(j) for j in bill_.split(',')]
    except:
        print('ERROR input %s'%bill_)
        return
    PATH=os.getcwd()+'/'+'.controler.config/'+name+'.bill'
    cur_time=time.strftime('%Y-%m-%d %X')
    if os.path.exists(PATH):
        with open(PATH,'r') as f:
            json_dict=json.load(f)
        bill_list=json_dict['bill']
        date_list=json_dict['date']
    else:
        while True:
            a = input(colorama.Fore.RED+'Creat a new bill named '+name+'?  Y/N : '+colorama.Fore.RESET)
            if a == 'Y':
                break
            elif a == 'N':
                return
            else:
                print('input error, please input again')
        bill_list=[]
        date_list=[]
        json_dict={}
    for i in append_list:
        bill_list.append(i)
        date_list.append(cur_time)
    json_dict['bill']=bill_list
    json_dict['date']=date_list
    with open(PATH,'w') as f:
        json.dump(json_dict,f,sort_keys=True,indent=4)
    print('Add %s to %s in %s'%(bill_,name,cur_time)) 

def show_bill_detail(name):
    PATH=os.getcwd()+'/'+'.controler.config/'+name+'.bill'
    if os.path.exists(PATH)==False:
        print('Bill is not exits!')
        return
    with open(PATH,'r') as f:
        json_dict=json.load(f)
    bill_list=json_dict['bill']
    date_list=[i.split(' ')[0] for i in json_dict['date']]
    sum_bill=0
    for j in bill_list:
        sum_bill+=j
    sum_days=0
    counted_date=[]
    for k in date_list:
        if k not in counted_date:
            counted_date.append(k)
            sum_days+=1
        else:
            pass
    print('From %s to %s'%(date_list[0],date_list[-1]))
    print('Record days: %d ,  Totle comsumeption: %.2f ,  Average: %.2f/day'%(sum_days,sum_bill,sum_bill/sum_days))

argument_list=['init','tb','resourse','bill','version','help']
option_list=[['-t','-i'],['show'],['path'],['add','show'],None,None]
if argv[1] not in argument_list:
    raise Exception('Argument ERROR!   %s'%argv[1])
if argv[1] == 'init':
    op=argv[2:]
    op_dic={}
    if len(op)%2!=0:
        raise Exception('number of argument is wrong!   %d'%len(op))
    for i in range(0,len(op)):
        if i%2==0:
            if op[i] not in option_list[0]:
                raise Exception('options ERROR!   %s'%op[i])
            op_dic[op[i]]=op[i+1]
    t=1
    i='T'
    if '-t' in op_dic:
        t=op_dic['-t']
    if '-i' in op_dic:
        i=op_dic['-i']
    init(t,i)
elif argv[1] == 'tb':
    op=argv[2:]
    op_dic={}
    if len(op)%2!=0:
        raise Exception('number of argument is wrong!   %d'%len(op))
    for i in range(0,len(op)):
        if i%2==0:
            if op[i] not in option_list[1]:
                raise Exception('options ERROR!   %s'%op[i])
            op_dic[op[i]]=op[i+1]
    row = 5
    if 'show' in op_dic:
        row = int(op_dic['show'])
    print(row)
    show_timetable(row)
elif argv[1] == 'resourse':
    op=argv[2:]
    if len(op)==0:
        resourse('[default]')
    else:
        path = op[-1]
        resourse(path)
elif argv[1] == 'bill':
    if argv[2] == 'add':
        op=argv[3:]
        bill_name=''
        bill_num=''
        if len(op)%2!=0 or len(op)<=0:
            raise Exception('number of argument is wrong!   %d'%len(op))
        for i in range(0,len(op)):
            if i%2==0:
                bill_name = op[i+1]
                bill_num = op[i]
        bill(bill_name,bill_num)
    elif argv[2] == 'show':
        op=argv[3:]
        name = op[-1]
        show_bill_detail(name)
    else:
        raise Exception('Argument options!')
elif argv[1] == 'version':
    print('Studying controler version 1.0.1 @Kylis\ngithub: https://github.com/walkureHHH/Study_life_Controler\n(argument branch)')
elif argv[1] == 'help':
    print("""~ init
    -t: timetable type, 1 for Monday-Friday(default), 2 for Monday-Sunday
    -i:if you want add information for each course, T or F(default)

~ tb show [number of days each rows]

~ resourse [default path(optional, but when you first use the command, you must have it)]

~ bill add [num] [name]

~ bill show [name]
""") 
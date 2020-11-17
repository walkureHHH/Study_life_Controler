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
    time_span=input('Time span(example:"8-21"):')
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
            print('please init default path first, use "con resourse your/default/path/"')
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
    support_format=['pdf','doc','docx','ipynb','c','cpp','py','java','ppt','pptx']      # available resourse format
    course_string=''
    index=0
    index_list=['']
    for course in courses:
        course_string+='['+str(index)+']'+course+' | '
        index_list.append(str(index))
        index+=1
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
            if_break=input(colorama.Fore.YELLOW+'Finish? Y/N: '+colorama.Fore.RESET)
            if if_break=='Y':
                break
            elif if_break=='N':
                pass      

def bill(name,bill_):
    append_list=[float(j) for j in bill_.split(',')]
    PATH=os.getcwd()+'/'+'.controler.config/'+name
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
        

def show_bill_detail(name):
    PATH=os.getcwd()+'/'+'.controler.config/'+name
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
    print('Record days: %d ,  Totle comsumeption: %.2f ,  Average: %.2f'%(sum_days,sum_bill,sum_bill/sum_days))


init_o=['-t','-i'] # all legal options for init
# t for timetable type, i for information switch
if argv[1] == 'init':
    tt="1"  # default value for timetable type
    info='F' # default value for information switch
    init_option=[]  # used to store all options the process got
    if len(argv) > 2:
        for i in argv[2:]: # find all options inputed
            if i.startswith('-'):
                init_option.append(i)
        for j in init_option: # find if there are some illegal options
            if j in init_o:
                pass
            else:
                print('illegal option %s'%j)
                exit(0)
        reverse_argv=argv[2:] # Reverse the argv list, because if there are some option appear more than once, we use the last one.For example "-t 1 -t 2" equivalent to "-t 2"
        reverse_argv.reverse()
        for k in init_option: # get the value for all legal options
            a = reverse_argv.index(k)
            if k == '-t':
                tt=reverse_argv[a-1]
            if k == '-i':
                info=reverse_argv[a-1]
    if tt in ['1','2'] and info in ['T','F']:  # check if values of options are legal
        init(tt,info)  # call the init function
    else:
        print('illegal option for timetable type')

if argv[1] == 'show':
    if len(argv)!=3:
        print(len(argv))
        print('input ERROR')
    elif argv[2].isdigit()==False:
        print(argv[2])
        print('input ERROR')
    else:
        show_timetable(int(argv[2]))

if argv[1] == 'resourse':
    if len(argv)==3:
        resourse(argv[2])
    elif len(argv)==2:
        resourse("[default]")

if argv[1] == 'bill':
    if len(argv)==4:
        bill(argv[2],argv[3])
    else:
        print('input error!')

if argv[1] == 'bill_show' or argv[1] == 'show_bill':
    if len(argv)==3:
        show_bill_detail(argv[2])
    else:
        print('input error!')
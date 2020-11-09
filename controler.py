import os
import json
import pandas
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
        a = input('name of course %d (. to finish): '%num)
        if a == '':
            pass
        elif a == '.':
            break
        else:
            if info_switch == True:
                while True:
                    b = input('info for course %d : '%num)
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
        f = open(PATH+'/'+'Resourse'+'/'+j+'/'+'download.py','w')
        f.close()
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
    index_list=[]
    for course in courses:
        course_string+='['+str(index)+']'+course+' | '
        index_list.append(str(index))
        index+=1
    index_list.append('')
    f1=open(PATH+'/'+'.controler.config/timetable.csv',encoding='utf-8',mode='a')
    for hour in hours:
        print('The course in %d:00 - %d:00:'%(hour,hour+1))
        print('('+course_string+')')
        temp1=[]
        temp2=[]
        for day in week:
            print('for '+day)
            while True:
                in_of_course=input('Input the index of courses: ')
                if in_of_course in index_list:
                    break
                else:
                    print('ERROR index please input again')
            venue=input('The venue of it: ')
            if in_of_course != '':
                temp1.append(courses[int(in_of_course)])
            else:
                temp1.append('-')
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

def assignment():
    print('developing')
    pass

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


def modify_timetable():
    pass

def timetable_to_html(path):
    pass

def import_conf():
    pass
        
init_o=['-t','-i'] # all legal options for init
# t for timetable type, i for information switch
pull_o=['-a','-l','-s'] # all legal options for pull
# 
st_o=['-r'] # all legal options for timetable
# a for add, s for show, l for list

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

if argv[1] == 'assi':
    assignment()

if argv[1] == 'pull':
    print('this part is in development')
    pass

if argv[1] == 'st':
    if len(argv)<=2:
        print('options lack! -s for show')
    else:
        if argv[2] not in st_o:
            print('options ERROR!')
        elif argv[2]=='-r':
            show_timetable(2)
import os
from sys import argv

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
    os.mkdir(PATH+'/'+'.controler.config')
    os.mkdir(PATH+'/'+'.controler.config/Timetable')
    for i in courses:
        os.mkdir(PATH+'/'+'Assignment'+'/'+i)
    for j in courses:
        os.mkdir(PATH+'/'+'Resourse'+'/'+j)
        f = open(PATH+'/'+'Resourse'+'/'+j+'/'+'download.py','w')
        f.close()
    f = open(PATH+'/'+'.controler.config/conf',encoding='utf-8',mode='a')
    for k in courses:
        f.write(k+'|')
    if info_switch == True:
        f.write('\n')
        for l in course_info:
            f.write(l+'|')
    f.close()

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
                temp1.append('')
            temp2.append(venue)
        string1=''
        for n in temp1:
            string1+=n+','
        string1+='\n'
        string2=''
        for o in temp2:
            string2+=o+','
        string2+='\n'
        f1=open(PATH+'/'+'.controler.config/Timetable/courses.csv',encoding='utf-8',mode='a')
        f2=open(PATH+'/'+'.controler.config/Timetable/venue.csv',encoding='utf-8',mode='a')
        f1.write(string1)
        f2.write(string2)
    f1.close()
    f2.close()

def assignment():
    print('developing')
    pass

def show_timetable():
    pass

def modify_timetable():
    pass

def timetable_to_html(path):
    pass

def import_conf():
    pass
        
init_o=['-t','-i'] # all legal options for init
pull_o=['-a','-l','-s'] # all legal option for pull

if argv[1] == 'init':
    tt="1"
    info='F'
    init_option=[]
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
    print(tt, info)
    if tt in ['1','2'] and info in ['T','F']:
        init(tt,info)
    else:
        print('illegal option for timetable type')

if argv[1] == 'assi':
    assignment()

if argv[1] == 'pull':
    print('this part is in development')
    pass
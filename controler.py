import os
from sys import argv

def init(type):
    courses=[]
    timetable=[]
    venue_map=[]
    imfo_map=[]
    PATH=os.getcwd()
    timetable_type=1
    num = 1
    while True:
        a = input('name of course %d (. to finish): '%num)
        if a!= '.':
            if a == '':
                pass
            else:
                courses.append(a)
                num+=1
        else:
            break
        num
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
        f.write(k+',')
    f.close()

def assignment():
    print('developing')
    pass

def show_timetable():
    pass

def modify_timetable():
    pass

def timetable_to_html(path):
    pass
        
init_o=['-t'] # all legal options for init
pull_o=['-a','-l','-s'] # all legal option for pull

if argv[1] == 'init':
    tt="1"
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
    if tt in ['1','2']:
        init(tt)
    else:
        print('illegal option for timetable type')

if argv[1] == 'assi':
    assignment()

if argv[1] == 'pull':
    print('this part is in development')
    pass
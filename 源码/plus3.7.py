import pygame,sys,os,configparser
from pygame.locals import *

version='R1.0 (250611.307.1 Released)'
packagename='随机点名plus版'
titleofprogramme=f"随机点名Plus版 v{version}"

updatelog="""
--==更新日志==--
[v250611.307.1]增加了“启动界面帧率调整平衡比例系数”，即init_fpsk，并修正几处错误，还增强了性能
[v250611.306.6]改为从ini文件中读取配置；性能修复(但是没做完 T_T ……animationchoice紧急修复性能，但砍掉了一些功能，或留下了小bug)
[v250610.305.1]小调整~
[v250610.304.0]修正进入动画中全屏按钮的bug
[v250604.303.1]完善进入动画（doge）
[v250604.302.0]加个进入的动画（doge）
[v250604.301.5]更新了太多内容，我无法总结
[v250604.300.0]增加了酷炫的启动界面MH_init_animation[v1.0]，并修正bar高度的bug
[v250516.237.0]采用convert_alpha()加载背景图，提升了背景图的渲染性能
[v250515.236.2]增加了鼠标放在按钮上的效果（抽选&全屏）
[v250514.235.0]修复bar不丝滑的bug，修复bar_gone中潜在的bug(for i in range(int(64*fpsk)))
"""

def load_config_to_globals(filepath):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(filepath)
    
    for section in config.sections():
        for key, value in config.items(section):
            var_name = f"{key}"              #f"{section}_{key}"
            try:
                globals()[var_name] = int(value)
            except:
                try :
                    globals()[var_name] = eval(value)
                except :
                    globals()[var_name] = value

def init():
    global MHicon
    load_config_to_globals('config.ini')
    if is_already_running():
        sys.exit()
    global initbarsurface,screen,lastlength,init_background,mask,currentamount
    itemscount=7          #要加载的项数
    if startwindowpositioncontrol:
        try:
            os.environ['SDL_VIDEO_WINDOW_POS'] = startwindowposition
        except:
            pass
    pygame.init()    #初始化pygame
    screen = pygame.display.set_mode((960,540),RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA | NOFRAME )      #界面大小
    init_background=pygame.image.load(init_background).convert_alpha()
    init_background= pygame.transform.smoothscale(init_background,(int(init_background.get_width()*max(screen.get_width()/init_background.get_width(), screen.get_height()/init_background.get_height())), int(init_background.get_height()*max(screen.get_width()/init_background.get_width(), screen.get_height()/init_background.get_height()))))
    screen.blit(init_background,(0,0))
    mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    mask.fill((0,0,0,init_background_alpha))
    MHicon=pygame.image.load(MHicon)        #商标
    MHicon= pygame.transform.smoothscale(MHicon,(int(MHicon.get_width()*0.08), int(MHicon.get_height()*0.08)))
    mask.blit(MHicon,((mask.get_width()-MHicon.get_width())/2,0))
    MHtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(33)).render('Macrohard®',True,(255,255,255))
    mask.blit(MHtext,((mask.get_width()-MHtext.get_width())/2+10,MHicon.get_height()-25))
    screen.blit(mask,(0,0))
    pygame.display.flip()
    pygame.time.Clock().tick(1)
    screen.blit(init_background,(0,0))
    softwaretext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(40),bold=True ).render(packagename,True,(255,255,255))
    mask.blit(softwaretext,((mask.get_width()-softwaretext.get_width())/2,MHicon.get_height()+MHtext.get_height()-25))
    versiontext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(20),bold=True ).render(version,True,(255,255,255))
    mask.blit(versiontext,((mask.get_width()-softwaretext.get_width())/2+softwaretext.get_width()+10,MHicon.get_height()+MHtext.get_height()-25+softwaretext.get_height()-versiontext.get_height()))
    screen.blit(mask,(0,0))
    pygame.display.flip()
    pygame.time.Clock().tick(30)
    screen.blit(init_background,(0,0))
    initbarsurface=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    pygame.draw.rect(mask, (127,127,127,180), ((screen.get_width()-720)/2,screen.get_height()/2+150,720,5), border_radius=2)
    screen.blit(mask,(0,0))
    pygame.display.flip()
    pygame.time.Clock().tick(30)
    lastlength=0
    currentamount=0
    globals()['init_fpsk']=init_fps/360
    for i in range(itemscount):       #载入内容的循环
        init_items(i,itemscount,100,animation)                 #加载的某一项
        pygame.event.get()
    screen.blit(init_background,(0,0))
    screen.blit(mask,(0,0))
    loadingpercent=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(('100.00%'),True,(255,255,255))
    screen.blit(loadingpercent,((screen.get_width()-720)/2+730,screen.get_height()/2+140))
    ldtext='已完成！正在载入……'
    loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
    screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
    if animation:
        for i in range(int(63*init_fpsk)):
            pygame.draw.rect(initbarsurface, (0,191,0,int(4/init_fpsk)), ((screen.get_width()-720)/2,screen.get_height()/2+150,720,5), border_radius=2)
            screen.blit(initbarsurface,(0,0))
            pygame.display.flip()
            pygame.time.Clock().tick(init_fps)
    else:
        pygame.draw.rect(screen, (0,191,0,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,720,5), border_radius=2)
        pygame.display.flip()
        pygame.time.Clock().tick(init_fps)
    tempsurface=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    pygame.draw.rect(tempsurface,(0,0,0,int(10/init_fpsk)),(0,0,tempsurface.get_width(),tempsurface.get_height()))
    for i in range(int(63*init_fpsk)):
        screen.blit(tempsurface,(0,0))
        pygame.display.flip()
        pygame.time.Clock().tick(init_fps)
    screen = pygame.display.set_mode((960,540),RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA)
    pygame.time.Clock().tick(init_fps)
    backgroundimage=proportional_scale(background_img, window_width, window_height)
    global tempsurface_2
    tempsurface_2=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
    tempsurface_2.blit(backgroundimage,(0,0))
    global lastname
    lastname="       ？      "
    draw_lastname(flush=False,temp=True)
    lastmessage='欢迎使用随机点名系统，本软件由 巨硬 开发，欢迎汇报BUG'     #修复bug:一闪而过……
    message_time = time.time()
    message(lastmessage,flush=False,temp=True)
    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180,temp=True)  
    fullscreenbutton(flush=False,temp=True)
    for i in range(int(63*init_fpsk)):
        tempsurface.fill((0,0,0,0))
        screen.blit(tempsurface_2,(0,0))
        showclock(flush=False)
        pygame.draw.rect(tempsurface,(0,0,0,int(255-4*i/init_fpsk)),(0,0,tempsurface.get_width(),tempsurface.get_height()))
        screen.blit(tempsurface,(0,0))
        pygame.display.flip()
        pygame.time.Clock().tick(init_fps)
    pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
    rootmainloop()

def init_items(num,total,totalamount,animation):
    global initbarsurface,lastlength,currentamount,namelist,_name_,init_fpsk
    currentlength=lastlength
    match num:
        case 0:
            global time,threading,random,copy,datetime,tk,buttonx,buttony,sizex,sizey,fps,used_times,screen,is_fullscreen,barsurface,buttonsurface,window_width, window_height,k,version,screen,clock,settings_img,bar_screen,background_img,name,clocksurface,namesurface
            currentamount+=5
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='载入变量……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 1:
            import time,threading,random,copy,datetime
            import tkinter as tk
            used_times=0
            is_fullscreen=False
            try:
                background_img=pygame.image.load(background_img).convert_alpha()
            except:
                pass
            currentamount+=33
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='读取背景……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 2:
            pygame.display.set_caption(titleofprogramme)#标题
            try:
                pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
            except:
                pass
            currentamount+=3
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='设定窗口……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 3:
            window_width, window_height = pygame.display.get_surface().get_size()
            _k_()
            global fullscreensurface,exitfullscreenbutton_img,fullscreenbutton_img
            fullscreensurface=pygame.Surface((36*k,36*k) ,SRCALPHA)
            fullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
            exitfullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
            currentamount+=7
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='计算比例系数……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 4:
            namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA)
            namesurface.fill((0, 0, 0, 0))
            pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
            clocksurface=pygame.Surface((140*k,40*k),SRCALPHA)
            clocksurface.fill((0, 0, 0, 0))
            buttonsurface=pygame.Surface((100*k,30*k),SRCALPHA)
            buttonsurface.fill((0,0,0,0))
            barsurface=pygame.Surface((0,0),SRCALPHA)
            barsurface.fill((0,0,0,0))
            pygame.draw.rect(clocksurface, (0,0,0,100), (0,0,130*k,40*k), border_radius=int(5*k))
            currentamount+=32
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='创建表面……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 5:
            buttonx=int((window_width-100*k)/2)
            buttony=int((window_height-30*k)/2+200*k)
            sizex=int(100*k)
            sizey=int(30*k)
            currentamount+=6
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='创建变量……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        case 6:
            with open('name.txt','r') as namelist :
                _name_=namelist.read().split('\n')
            currentamount+=14
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            ldtext='读取名单……'
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
    if animation:
        while currentlength<720*(currentamount)/totalamount:
            if currentlength<4:
                currentlength=4
            screen.blit(init_background,(0,0))
            screen.blit(mask,(0,0))
            loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
            screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
            pygame.draw.rect(screen, (255,255,255,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,currentlength,5), border_radius=2)
            loadingpercent=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render((str("%.2f"%(currentlength*100/720))+'%'),True,(255,255,255))
            screen.blit(loadingpercent,((screen.get_width()-720)/2+730,screen.get_height()/2+140))
            currentlength+=animationspeed/init_fpsk
            pygame.display.flip()
            pygame.time.Clock().tick(init_fps)
        lastlength=currentlength
    else :
        screen.blit(init_background,(0,0))
        screen.blit(mask,(0,0))
        loadingtext=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render(ldtext,True,(255,255,255))
        screen.blit(loadingtext,((screen.get_width()-720)/2,screen.get_height()/2+160))
        pygame.draw.rect(screen, (255,255,255,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,currentlength,5), border_radius=2)
        loadingpercent=pygame.font.SysFont("MicrosoftYaHei UI",size=int(15)).render((str("%.2f"%(currentlength*100/720))+'%'),True,(255,255,255))
        screen.blit(loadingpercent,((screen.get_width()-720)/2+730,screen.get_height()/2+140))
        pygame.draw.rect(screen, (255,255,255,255), ((screen.get_width()-720)/2,screen.get_height()/2+150,720/totalamount*(currentamount),5), border_radius=2)
        pygame.display.flip()
    if 720/total*(num+1)<720:
        pygame.time.Clock().tick(15)
    else:
        pygame.time.Clock().tick(init_fps)

def is_already_running():
    from ctypes import windll, wintypes
    return windll.user32.FindWindowW(0, titleofprogramme)

def _k_():
    global k,window_width, window_height
    k=min(window_width/960,window_height/540)
    return k

def proportional_scale(img, max_width, max_height):
    global window_width, window_height, bg
    ratio = max(window_width/img.get_width(), window_height/img.get_height())
    bg= pygame.transform.smoothscale(img, 
        (int(img.get_width()*ratio), int(img.get_height()*ratio)))
    return bg

def showclock(flush=True):
    global screen,k,window_width, window_height,clocksurface
    clock_time=pygame.font.SysFont("MicrosoftYaHei UI",int(30*k)).render(datetime.datetime.now().strftime("%H:%M:%S"),True,(255,255,255))
    screen.blit(clocksurface,((window_width-130*k),0))
    screen.blit(clock_time,((130*k-clock_time.get_width())/2-2*k+(window_width-130*k),(40*k-clock_time.get_height())/2))
    if flush:
        pygame.display.update(((window_width-130*k),0,140*k,40*k))

def draw_button(place,size,text,rad=3,color=(50,50,50),_alpha_=255,temp=False):
    global tempsurface_2
    buttonsurface.fill((0,0,0,0))
    sizeoftext=min(int(size[1]*2/3),int(size[0]/len(text)-1))
    pygame.draw.rect(buttonsurface, (*color,_alpha_), (0,0,size[0],size[1]), border_radius=rad)
    buttonsurface.blit(pygame.font.SysFont("MicrosoftYaHei UI",sizeoftext).render(text,True,(255,255,255)),((size[0]-sizeoftext*len(text))/2,((size[1]-sizeoftext*3/2)/2)))
    if temp:
        tempsurface_2.blit(buttonsurface,place)
        return 
    screen.blit(buttonsurface,place)

def event_listening(items):
        global lastmessage,dpup,name,buttonx,buttony,sizex,sizey,k,window_width, window_height,lastname,bg,background_img,reset_namelist,message_time,ww,wh,animation,fullscreensurface,clocksurface,namesurface,buttonsurface,barsurface,screen,is_fullscreen
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:#退出
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    # 判断具体按键（1左键/2中键/3右键）
                    #if event.button == 1:  
                        click_pos = pygame.mouse.get_pos()  # 始终返回当前鼠标坐标
                        window_width, window_height = pygame.display.get_surface().get_size()
                        if click_pos[0] in range(buttonx,buttonx+sizex) and click_pos[1] in range(buttony,buttony+sizey) and 'button' in items:
                          if reset_namelist==1:
                            a=0
                            background()
                            draw_button((buttonx,buttony),(sizex,sizey),"重置",rad=int(3*k),color=(127,127,127),_alpha_=180)
                            showclock()
                            draw_lastname()
                            fullscreenbutton()
                            pygame.display.update((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k),100*k,30*k))
                            pygame.display.update((int(window_width-4.5*150*k)/2+8*k,int(window_height-150*k)/2-30*k,4.5*150*k+30*k,150*k+60*k))
                            pygame.time.Clock().tick(30)
                            while a==0:
                                if not any(pygame.mouse.get_pressed()):
                                    a=1
                                for event in pygame.event.get():
                                    match event.type:
                                        case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                                            a=1
                                        case pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                background()
                                draw_lastname()
                                showclock()
                                pygame.time.Clock().tick(fps)
                            if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos[1] in range(buttony,buttony+sizey):
                                draw_button((buttonx,buttony),(sizex,sizey),"重置",rad=int(3*k),_alpha_=180)
                                pygame.display.update((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k),100*k,30*k))
                                pygame.time.Clock().tick(30)
                                name=copy.deepcopy(_name_)
                                reset_namelist=0
                                lastmessage='已重置人名单'
                                message(lastmessage)
                                message_time = time.time()
                          else:
                            a=0
                            background()
                            draw_button((buttonx,buttony),(sizex,sizey),"抽选",rad=int(3*k),color=(127,127,127),_alpha_=180)
                            showclock()
                            pygame.display.update((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k),100*k,30*k))
                            pygame.time.Clock().tick(30)
                            while a==0:
                                if not any(pygame.mouse.get_pressed()):
                                    a=1
                                for event in pygame.event.get():
                                    match event.type:
                                        case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                                            a=1
                                        case pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                background()
                                showclock()
                                pygame.time.Clock().tick(fps)
                            if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos()[1] in range(buttony,buttony+sizey):
                                draw_button((buttonx,buttony),(sizex,sizey),"抽选",rad=int(3*k),_alpha_=180)
                                pygame.display.update((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k),100*k,30*k))
                                pygame.time.Clock().tick(30)
                                animation_choice()
                                if len(name)==0:
                                    reset_namelist=1
                        elif click_pos[0] in range(int(window_width-36*k),window_width) and click_pos[1] in range(int(window_height-36*k),window_height):
                            a=0
                            fullscreenbutton('click')
                            while a==0:
                                background()
                                draw_lastname()
                                showclock()
                                if not any(pygame.mouse.get_pressed()):
                                    a=1
                                for event in pygame.event.get():
                                    match event.type:
                                        case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                                            a=1
                                        case pygame.QUIT:
                                            pygame.quit()
                                            sys.exit()
                                pygame.time.Clock().tick(fps)
                            if pygame.mouse.get_pos()[0] in range(int(window_width-36*k),window_width) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
                                is_fullscreen = not is_fullscreen
                                root = tk.Tk()
                                width = root.winfo_screenwidth()
                                height = root.winfo_screenheight()
                                root.destroy()
                                print(f"屏幕分辨率: {width}x{height}")
                                if is_fullscreen:
                                    ww,wh= pygame.display.get_surface().get_size()
                                    screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN  | HWSURFACE | DOUBLEBUF | SRCALPHA )
                                    window_width, window_height = pygame.display.get_surface().get_size()
                                else:
                                    screen = pygame.display.set_mode((width,height), RESIZABLE | HWSURFACE | DOUBLEBUF )#| SRCALPHA)
                                    screen = pygame.display.set_mode((ww,wh), RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA)
                                    window_width, window_height = pygame.display.get_surface().get_size()
                                try:
                                    proportional_scale(background_img, window_width, window_height)
                                except :
                                    pass
                                background()
                                showclock()
                                draw_lastname()
                                fullscreenbutton()
                                if time.time()-message_time>=5 and message_time!=0:
                                    message('')
                                    message(lastmessage)
                                    message_time=0
                                if reset_namelist==1:
                                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180) 
                                else:
                                    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
                                k=_k_()
                                clocksurface=pygame.Surface((140*k,40*k),SRCALPHA)
                                clocksurface.fill((0,0,0,0))
                                pygame.draw.rect(clocksurface, (0,0,0,100), (0,0,130*k,40*k), border_radius=int(5*k))
                                buttonsurface=pygame.Surface((100*k,30*k),SRCALPHA)
                                namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA)
                                pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
                                dpup=time.time()
                                pygame.display.update()
                            else:
                                fullscreenbutton()
                case pygame.VIDEORESIZE:
                     window_width, window_height = pygame.display.get_surface().get_size()
                     k=_k_()
                     try:
                         proportional_scale(background_img, window_width, window_height)
                     except:
                         pass
                     background()
                     showclock()
                     draw_lastname()
                     fullscreenbutton()
                     if time.time()-message_time>=5 and message_time!=0:
                         lastmessage=''
                         message(lastmessage)
                         message_time=0
                     if reset_namelist==1:
                         draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180) 
                     else:
                         draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
                     clocksurface=pygame.Surface((140*k,40*k),SRCALPHA)
                     clocksurface.fill((0,0,0,0))
                     pygame.draw.rect(clocksurface, (0,0,0,100), (0,0,130*k,40*k), border_radius=int(5*k))
                     buttonsurface=pygame.Surface((100*k,30*k),SRCALPHA)
                     namesurface=pygame.Surface((4.5*150*k+30*k,150*k+60*k),SRCALPHA)
                     pygame.draw.rect(namesurface, (0,0,0,155), (0,0,4.5*150*k+30*k,150*k+60*k), border_radius=int(33*k))
                     buttonx=int((window_width-100*k)/2)
                     buttony=int((window_height-30*k)/2+200*k)
                     sizex=int(100*k)
                     sizey=int(30*k)
                     dpup=time.time()
                case pygame.ACTIVEEVENT:
                     background()
                     showclock()
                     draw_lastname()
                     #fullscreenbutton()
                     if time.time()-message_time>=5 and message_time!=0:
                         lastmessage=''
                         message(lastmessage)
                         message_time=0
                     if reset_namelist==1:
                         draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180) 
                     else:
                         draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
                     dpup=time.time()

def animation_choice():
    global fpsk,kkk,lastlengthofbar,dpup,namesurface,used_times,fps,buttonx,buttony,sizex,sizey,lastname,k,window_width, window_height,lastname
    global lastmessage,buttonx,buttony,sizex,sizey,k,window_width, window_height,lastname,bg,background_img,message_time,ww,wh,animation,fullscreensurface,clocksurface,namesurface,buttonsurface,barsurface,screen,is_fullscreen
    current_time_seconds = time.time()
    lastlengthofbar=0
    background()
    draw_button((buttonx,buttony),(sizex,sizey),"正在抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
    pygame.display.update((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k),100*k,30*k))
    fpsk=fps/180
    a=0
    kkk=0.75
    fullscreenbutton('disable')
    message(lastmessage)
    tempfps=int(fps*k*3/kkk)
    dpup=0
    for i in range(int(240*fpsk*kkk)):
        background()
#         message(lastmessage)
        if time.time()-message_time>=5 and message_time!=0:
            lastmessage=''
            message(lastmessage)
            message_time=0
        if a%(6*fpsk)==0:
            showclock()
            lastname=randomchoice()
        bar(k*3*i/kkk/fpsk,720*k)
        if time.time()-current_time_seconds>=2:
            break
        if time.time()-dpup>=0.01 and time.time()-dpup<=1 and dpup!=0:
            buttonx,buttony=int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)
            sizex,sizey=int(100*k),int(30*k)
            draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"正在抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
            global fullscreensurface,exitfullscreenbutton_img,fullscreenbutton_img
            fullscreensurface=pygame.Surface((36*k,36*k) ,SRCALPHA)
            fullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
            exitfullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
            fullscreenbutton()
            pygame.display.flip()
            dpup=0
        a=a+1
        event_listening([])
        pygame.time.Clock().tick(tempfps)
    background()
    lastname=randomchoice()
    name.remove(lastname)
    used_times=used_times+1
    bar_gone(720*k)

def bar(lenth,total):
    global k,window_width, window_height,barsurface,lastlengthofbar,barspeed
    barsurface=pygame.Surface((total,5*k),SRCALPHA)
    deltalenth=k*barspeed/kkk/fpsk
    while lastlengthofbar<=lenth:
        pygame.draw.rect(barsurface, (200,200,200,255), (0,0,lastlengthofbar,5*k), border_radius=2)
        screen.blit(barsurface,((window_width-total)/2,window_height/2+130*k))
        pygame.display.update((window_width-total)/2,window_height/2+130*k,total,5*k)
        lastlengthofbar+=deltalenth
        pygame.time.Clock().tick(int(fps*k*3/kkk))
    
def bar_gone(total):
    global lastmessage,dpup,buttonx,buttony,sizex,sizey,k,window_width, window_height ,barsurface,fps,buttonx,buttony,sizex,sizey,k,window_width, window_height,lastname,bg,background_img,used_times,message_time,ww,wh,animation,fullscreensurface,clocksurface,namesurface,buttonsurface,barsurface,screen,is_fullscreen
    fpsk=fps/120
    x=(window_width-total)/2
    y=window_height/2+130*k
    barsurface=pygame.Surface((total,5*k),SRCALPHA)
    for i in range(int(64*fpsk)):  
        background()
        showclock()
        if pygame.mouse.get_pos()[0] in range(int(window_width-36*k),window_width) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
            fullscreenbutton('puton')
        else:
            fullscreenbutton()
        if time.time()-message_time>=5 and message_time!=0:
            lastmessage=''
            message(lastmessage)
            message_time=0
        barsurface.fill((0,0,0,0))
        pygame.draw.rect(barsurface, (200,200,200,int(255-i*4/fpsk)), (0,0,total,5*k), border_radius=2)
        screen.blit(barsurface,(x,y))
        pygame.display.update((x,y,total,5*k))
        event_listening(['bar_gone'])
        if time.time()-dpup>=0.01 and time.time()-dpup<=1 :
            background()
            x=(window_width-total)/2
            y=window_height/2+130*k
            screen.blit(barsurface,(x,y))
            window_width, window_height = pygame.display.get_surface().get_size()
            k=_k_()
            buttonx=int((window_width-100*k)/2)
            buttony=int((window_height-30*k)/2+200*k)
            sizex=int(100*k)
            sizey=int(30*k)
            draw_lastname()
            global fullscreensurface,exitfullscreenbutton_img,fullscreenbutton_img
            fullscreensurface=pygame.Surface((36*k,36*k) ,SRCALPHA)
            fullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
            exitfullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
            fullscreenbutton()
            message(lastmessage)
            showclock()
            draw_button((buttonx,buttony),(sizex,sizey),"正在抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
            pygame.display.flip()
            dpup=0
        pygame.time.Clock().tick(fps)
    background()
    barsurface.fill((0,0,0,0))
    pygame.draw.rect(barsurface, (200,200,200,0), (0,0,total,5*k), border_radius=2)
    screen.blit(barsurface,(x,y))
    pygame.display.update((x,y,total,5*k))

def draw_lastname(flush=True,temp=False):
    global tempsurface_2
    text=pygame.font.SysFont("MicrosoftYaHei UI",size=int(150*k)).render(lastname,True,(255,255,255))
    if temp:
        tempsurface_2.blit(namesurface,((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k))
        tempsurface_2.blit(text, ((4.5*150*k+30*k-text.get_width())/2-2*k+(window_width-4.5*150*k)/2+8*k,(150*k+60*k-text.get_height())/2-10*k+(window_height-150*k)/2-30*k))
        return 
    screen.blit(namesurface,((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k))
    screen.blit(text, ((4.5*150*k+30*k-text.get_width())/2-2*k+(window_width-4.5*150*k)/2+8*k,(150*k+60*k-text.get_height())/2-10*k+(window_height-150*k)/2-30*k))
    if flush:
        pygame.display.update(((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k,4.5*150*k+30*k,150*k+60*k))

def randomchoice():
    global name,_name_,k,window_width, window_height
    temp=random.choice(name)
    text=pygame.font.SysFont("MicrosoftYaHei UI",size=int(150*k)).render(temp,True,(255,255,255))
    screen.blit(namesurface,((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k))
    screen.blit(text, ((4.5*150*k+30*k-text.get_width())/2-2*k+(window_width-4.5*150*k)/2+8*k,(150*k+60*k-text.get_height())/2-10*k+(window_height-150*k)/2-30*k))
    pygame.display.update(((window_width-4.5*150*k)/2+8*k,(window_height-150*k)/2-30*k,4.5*150*k+30*k,150*k+60*k))
    return temp

def background():
    global window_width, window_height,background_img,bg
    try:
        screen.blit(bg,((window_width-bg.get_width())/2,(window_height-bg.get_height())/2))
    except :
        screen.fill((0,0,0))
        errorbackground=pygame.font.SysFont("MicrosoftYaHei UI",int(20*k)).render("加载背景失败，已使用黑色背景",True,(255,255,255))
        screen.blit(errorbackground,(0,0))
        pygame.display.update((0,0,errorbackground.get_width(),errorbackground.get_height()))

def fullscreenbutton(style=0,flush=True,temp=False):
    global k,fullscreensurface,is_fullscreen,window_width,window_height,tempsurface_2,fullscreenbutton_img,exitfullscreenbutton_img
    if temp:
        pygame.draw.rect(fullscreensurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
        tempsurface_2.blit(fullscreensurface,(960-36,540-36))
        tempsurface_2.blit(fullscreenbutton_img,(960-36,540-36))
        return 
    if is_fullscreen:
        fullscreensurface.fill((0,0,0,0))
        if style=='click':
            pygame.draw.rect(fullscreensurface, (127,127,127,100), (0,0,36*k,36*k), border_radius=int(5*k))
        elif style=='puton':
            pygame.draw.rect(fullscreensurface, (63,63,63,100), (0,0,36*k,36*k), border_radius=int(5*k))
        else:
            pygame.draw.rect(fullscreensurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
        fullscreensurface.blit(exitfullscreenbutton_img,(0,0))
        screen.blit(fullscreensurface,(window_width-36*k,window_height-36*k))
        if flush:
            pygame.display.update((window_width-36*k,window_height-36*k,36*k,36*k))
    else:
        fullscreensurface.fill((0,0,0,0))
        if style=='click':
            pygame.draw.rect(fullscreensurface, (127,127,127,100), (0,0,36*k,36*k), border_radius=int(5*k))
        elif style=='puton':
            pygame.draw.rect(fullscreensurface, (63,63,63,100), (0,0,36*k,36*k), border_radius=int(5*k))
        else:
            pygame.draw.rect(fullscreensurface, (0,0,0,100), (0,0,36*k,36*k), border_radius=int(5*k))
        fullscreensurface.blit(fullscreenbutton_img,(0,0))
        screen.blit(fullscreensurface,(window_width-36*k,window_height-36*k))
        if flush:
            pygame.display.update((window_width-36*k,window_height-36*k,36*k,36*k))

def message(text,flush=True,temp=False):
    global k,size,messagesurface,pos,updatearea,tempsurface_2
    window_width, window_height = pygame.display.get_surface().get_size()
    if text!='':
        window_width, window_height = pygame.display.get_surface().get_size()
        textfont=pygame.font.SysFont("MicrosoftYaHei UI",int(20*k))
        _text_=textfont.render(text,True,(255,255,255))
        size=(_text_.get_width()+20*k,_text_.get_height()+10*k)
        messagesurface=pygame.Surface(size,SRCALPHA)
        messagesurface.fill((0,0,0,0))
        pygame.draw.rect(messagesurface, (0,0,0,127), (0,0,_text_.get_width()+20*k,_text_.get_height()+10*k), border_radius=int(5*k))
        messagesurface.blit(_text_,(10*k,5*k))
        pos=((window_width-(_text_.get_width()+20*k))/2,60*k)
        if temp:
            tempsurface_2.blit(messagesurface,pos)
        screen.blit(messagesurface,pos)
        updatearea=((window_width-(_text_.get_width()+20*k))/2,60*k,_text_.get_width()+20*k,_text_.get_height()+10*k)
    else:
        messagesurface.fill((0,0,0,0))
        screen.blit(messagesurface,pos)
    if flush:
        pygame.display.update(updatearea)

def rootmainloop():
    global lastmessage,dpup,name,buttonx,buttony,sizex,sizey,k,window_width, window_height,lastname,bg,background_img
    global reset_namelist,message_time,ww,wh,animation,fullscreensurface,clocksurface,namesurface,buttonsurface,barsurface,screen,is_fullscreen
    window_width, window_height = pygame.display.get_surface().get_size()
    name=copy.deepcopy(_name_)
    pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
    try:
        proportional_scale(background_img, window_width, window_height)
    except:
        pass
    lastname="       ？      "
    background()
    fullscreenbutton()
    draw_lastname()
    pygame.display.update()
    _k_()
    fullscreenbutton()
    reset_namelist=0
    message_time=0
    dpup=0
    lastmessage='欢迎使用随机点名系统，本软件由 巨硬 开发，欢迎汇报BUG'     #修复bug:一闪而过……
    message_time = time.time()
    message(lastmessage)
    while 1:
        background()
        showclock()
        if time.time()-message_time>=5 and message_time!=0:
            lastmessage=''
            message(lastmessage)
            message_time=0
        if reset_namelist==1:
            if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos()[1] in range(buttony,buttony+sizey):
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(63,63,63),_alpha_=180)
            else:
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180)
        else:
            if pygame.mouse.get_pos()[0] in range(buttonx,buttonx+sizex) and pygame.mouse.get_pos()[1] in range(buttony,buttony+sizey):
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(63,63,63),_alpha_=180)
            else:
                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
        pygame.display.update((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k),100*k,30*k))
        if pygame.mouse.get_pos()[0] in range(int(window_width-36*k),window_width) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
            fullscreenbutton('puton')
        else:
            fullscreenbutton()
        if time.time()-dpup>=0.01 and time.time()-dpup<=1 :
            buttonx=int((window_width-100*k)/2)
            buttony=int((window_height-30*k)/2+200*k)
            sizex=int(100*k)
            sizey=int(30*k) 
            draw_lastname()
            global fullscreensurface,exitfullscreenbutton_img,fullscreenbutton_img
            fullscreensurface=pygame.Surface((36*k,36*k) ,SRCALPHA)
            fullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
            exitfullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
            message(lastmessage)
            pygame.display.flip()
            dpup=0
        event_listening(['button'])
        pygame.time.Clock().tick(fps)


init()
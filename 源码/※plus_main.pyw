import pygame,sys,os,configparser
from pygame.locals import *

version='3.14 (build250627.314.5)'
packagename='随机点名plus版'
titleofprogramme=f"随机点名Plus版 v{version}"

def function_loader():
    import ast, chardet    
    with open('function_file_list.txt', 'r') as f:
        function_file_list = [line.strip() for line in f]
    for function_file in function_file_list:
        # 动态检测编码
        with open(function_file, 'rb') as f:
            raw = f.read()
            encoding = chardet.detect(raw)['encoding'] or 'utf-8'
        
        # 带编码声明读取
        with open(function_file, 'r', encoding=encoding) as f:
            try:
                node = ast.parse(f.read())
            except SyntaxError:
                print(f"文件 {function_file} 包含语法错误或编码异常")
                continue
        
        funcs = [n for n in node.body if isinstance(n, ast.FunctionDef)]
        for func in funcs:
            code = compile(ast.Module(body=[func], type_ignores=[]), '<string>', 'exec')
            exec(code, globals())

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
    lastlength=0
    currentamount=0
    globals()['init_fpsk']=init_fps/360
    for i in range(itemscount):       #载入内容的循环
        init_items(i,itemscount,100,animation)   #加载的某一项
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
    lastname=firstdraw_lastname
    draw_lastname(flush=False,temp=True)
    lastmessage=welcomemessage
    message(lastmessage,flush=False,temp=True)
    draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180,temp=True)  
    fullscreenbutton(flush=False,temp=True)
    settingsbutton(flush=False,temp=True)
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

def is_already_running():
    from ctypes import windll, wintypes
    return windll.user32.FindWindowW(0, titleofprogramme)

function_loader()
init()
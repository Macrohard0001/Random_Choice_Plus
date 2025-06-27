def event_listening(items):
        global lastmessage,dpup,name,buttonx,buttony,sizex,sizey,k,window_width, window_height,lastname,bg,background_img,reset_namelist,message_time,ww,wh,animation,fullscreensurface,clocksurface,namesurface,buttonsurface,barsurface,screen,is_fullscreen
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:#退出
                    exitwindow()
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
                                import ctypes
                                user32 = ctypes.windll.user32
                                width = user32.GetSystemMetrics(0)
                                height = user32.GetSystemMetrics(1)
                                print(f"屏幕分辨率: {width}x{height}")
                                if is_fullscreen:
                                    ww,wh= pygame.display.get_surface().get_size()
                                    screen = pygame.display.set_mode((width,height), pygame.FULLSCREEN  | HWSURFACE | DOUBLEBUF | SRCALPHA )
                                    window_width, window_height = pygame.display.get_surface().get_size()
                                else:
                                    screen = pygame.display.set_mode((width,height), RESIZABLE | HWSURFACE | DOUBLEBUF )#| SRCALPHA)
                                    screen = pygame.display.set_mode((ww,wh), RESIZABLE | HWSURFACE | DOUBLEBUF | SRCALPHA)
                                    window_width, window_height = pygame.display.get_surface().get_size()
                                proportional_scale(background_img, window_width, window_height)
                                background()
                                showclock()
                                draw_lastname()
                                fullscreenbutton()
                                settingsbutton()
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
                                settingsbutton()
                        elif click_pos[0] in range(0,int(36*k)) and click_pos[1] in range(int(window_height-36*k),window_height):
                            a=0
                            background()
                            settingsbutton('click')
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
                            settingsbutton()
                            if pygame.mouse.get_pos()[0] in range(0,int(36*k)) and pygame.mouse.get_pos()[1] in range(int(window_height-36*k),window_height):
                                settingsmainloop()
                            else:
                                fullscreenbutton()
                                settingsbutton()
                            window_width, window_height = pygame.display.get_surface().get_size()
                            background()
                            showclock()
                            draw_lastname()
                            fullscreenbutton()
                            settingsbutton()
                            if time.time()-message_time>=5 and message_time!=0:
                                lastmessage=''
                                message(lastmessage)
                                message_time=0
                            if reset_namelist==1:
                                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"重置",rad=int(3*k),color=(15,15,15),_alpha_=180) 
                            else:
                                draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
                            dpup=time.time()
                            pygame.display.flip()
                case pygame.VIDEORESIZE:
                     window_width, window_height = pygame.display.get_surface().get_size()
                     k=_k_()
                     proportional_scale(background_img, window_width, window_height)
                     background()
                     showclock(flush=False)
                     draw_lastname(flush=False)
                     fullscreenbutton(flush=False )
                     settingsbutton(flush=False )
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
                     showclock(flush=False)
                     draw_lastname(flush=False )
                     if time.time()-message_time>=5 and message_time!=0:
                         lastmessage=''
                         message(lastmessage,flush=False )
                         message_time=0
                     dpup=time.time()
def settingsmainloop():
        global namesurface,buttonsurface,clocksurface,window_width,window_height,screen_surface,window_width , window_height , lastmessage , k,sizex,sizey,buttonx,buttony
        draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
        fullscreenbutton(flush=False)
        screensurface=pygame.display.get_surface()
        screen_surface=pygame.Surface(pygame.display.get_surface().get_size(),SRCALPHA)
        screen_surface.blit(screensurface,(0,0))
        mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
        mask.fill((0,0,0,127))
        a=0
        text=pygame.font.SysFont("MicrosoftYaHei UI",int(36*k)).render("还没做好呢……   点击任意位置返回~",True,(255,255,255))
        while a==0:
            screen.blit(screen_surface,(0,0))
            screen.blit(mask,(0,0))
            screen.blit(text,((screen.get_width()-text.get_width())/2,(screen.get_height()-text.get_height())/2))
            pygame.display.flip()
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT :
                        exitwindow()
                    case pygame.VIDEORESIZE:
                        for i in range(2):
                            window_width, window_height = pygame.display.get_surface().get_size()
                            k=_k_()
                            text=pygame.font.SysFont("MicrosoftYaHei UI",int(36*k)).render("还没做好呢……   点击任意位置返回~",True,(255,255,255))
                            mask=pygame.Surface((screen.get_width(),screen.get_height()),SRCALPHA)
                            mask.fill((0,0,0,127))
                            globals()['k']=_k_()
                            proportional_scale(background_img, window_width, window_height)
                            background()
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
                            globals()['fullscreensurface']=pygame.Surface((36*k,36*k) ,SRCALPHA)
                            showclock(flush=False)
                            draw_lastname(flush=False)
                            fullscreenbutton(flush=False )
                            settingsbutton(flush=False )
                            screensurface=pygame.display.get_surface()
                            screen_surface=pygame.Surface(pygame.display.get_surface().get_size(),SRCALPHA)
                            screen_surface.blit(screensurface,(0,0))
                            globals()['fullscreenbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
                            globals()['exitfullscreenbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
                            globals()['settingsurface']=pygame.Surface((36*k,36*k),SRCALPHA)
                            globals()['settingbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\settings.png'),(int(36*k), int(36*k)))
                            pygame.time.Clock().tick(120)
                    case pygame.MOUSEBUTTONDOWN | pygame.FINGERDOWN :
                        b=0
                        while b==0:
                            if not any(pygame.mouse.get_pressed()):
                                a,b=1,1
                            for event in pygame.event.get():
                                match event.type:
                                    case pygame.MOUSEBUTTONUP | pygame.FINGERUP:
                                        a,b=1,1
                                    case pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                            pygame.time.Clock().tick(120)
        window_width, window_height = pygame.display.get_surface().get_size()
        globals()['k']=_k_()
        proportional_scale(background_img, window_width, window_height)
        background()
        showclock(flush=False)
        draw_lastname(flush=False)
        fullscreenbutton(flush=False )
        settingsbutton(flush=False )
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
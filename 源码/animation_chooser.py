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
    settingsbutton()
    message(lastmessage)
    tempfps=int(fps*k*3/kkk)
    dpup=0
    for i in range(int(240*fpsk*kkk)):
        background()
        if time.time()-message_time>=5 and message_time!=0:
            lastmessage=''
            message(lastmessage)
            message_time=0
        if a%(6*fpsk)==0:
            showclock()
            lastname=randomchoice()
        bar(k*3*i/kkk/fpsk,720*k)
#         if time.time()-current_time_seconds>=2:
#             break
        event_listening([])
        if time.time()-dpup>=0 and time.time()-dpup<=1 and dpup!=0:
            buttonx,buttony=int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)
            sizex,sizey=int(100*k),int(30*k)
            draw_button((int((window_width-100*k)/2),int((window_height-30*k)/2+200*k)),(100*k,30*k),"正在抽选",rad=int(3*k),color=(15,15,15),_alpha_=180)
            global fullscreensurface,exitfullscreenbutton_img,fullscreenbutton_img
            fullscreensurface=pygame.Surface((36*k,36*k) ,SRCALPHA)
            fullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\fullscreen.png'),(int(36*k), int(36*k)))
            exitfullscreenbutton_img=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\exitfullscreen.png'),(int(36*k), int(36*k)))
            globals()['settingsurface']=pygame.Surface((36*k,36*k),SRCALPHA)
            globals()['settingbutton_img']=pygame.transform.smoothscale(pygame.image.load('.\\images\\buttons\\settings.png'),(int(36*k), int(36*k)))
            message(lastmessage,flush=False)
            showclock(flush=False )
            fullscreenbutton(flush=False)
            settingsbutton(flush=False)
            bar(k*3*i/kkk/fpsk,720*k)
            pygame.display.flip()
            dpup=0
        a=a+1
        pygame.time.Clock().tick(tempfps)
    background()
    lastname=randomchoice()
    name.remove(lastname)
    used_times=used_times+1
    bar_gone(720*k)
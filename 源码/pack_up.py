# pack_up.py
def pack_up():
    globals()['screensize'] = pygame.display.get_surface().get_size()
#     window_position = pygame.display.get_window_pos()
# Windows 系统示例（需安装 pywin32）
    if sys.platform == "win32":
        import win32gui
        hwnd = pygame.display.get_wm_info()["window"]
        rect = win32gui.GetWindowRect(hwnd)
        globals()['window_position'] = (rect[0],rect[1])
#         print(f"窗口位置: X={rect[0]}, Y={rect[1]}")
        print(f"窗口位置: {window_position}")
    
    pygame.quit()
    
    # 重置加载状态
    globals()['load'] = 0
    
    # 显示悬浮按钮
    from floatingbutton import show_floating_button
    show_floating_button()
    
    # 重新初始化PyGame
    os.environ['SDL_VIDEO_WINDOW_POS'] = f"{window_position[0]},{window_position[1]}"
    pygame.init()
    globals()['screen'] = pygame.display.set_mode(screensize, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SRCALPHA | pygame.RESIZABLE)
    pygame.display.set_icon(pygame.image.load(".\\images\\14.ico"))
    pygame.display.set_caption(titleofprogramme)#标题
    
    # 恢复界面
    background()
    showclock()
    draw_lastname()
    fullscreenbutton()
    settingsbutton()
    
    if reset_namelist == 1:
        draw_button((int((window_width-100*k)/2), int((window_height-30*k)/2+200*k)), 
                   (100*k, 30*k), "重置", rad=int(3*k), color=(15,15,15), _alpha_=180)
    else:
        draw_button((int((window_width-100*k)/2), int((window_height-30*k)/2+200*k)), 
                   (100*k, 30*k), "抽选", rad=int(3*k), color=(15,15,15), _alpha_=180)
    
    globals()['dpup'] = time.time()
    return
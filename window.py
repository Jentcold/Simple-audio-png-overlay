import pygame
import ctypes
import ctypes.wintypes
import win32api
import win32con
import win32gui
import audioengine


# Define window ( You may configure this ) 
WIDTH, HEIGHT = 250, 250
FPS = 30
CHROMA_KEY = (0, 255, 0)

# Transparency function 
def make_transparent(hwnd, chroma_key):
    # Get current window styles
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    # Set window style value to (old style OR layerd)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
    # Set chroma key
    r, g, b = chroma_key
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(r, g, b), 0, win32con.LWA_COLORKEY)


# PyGame window init 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
clock = pygame.time.Clock()
hwnd = pygame.display.get_wm_info()['window'] # Get window handle (ID)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
make_transparent(hwnd,CHROMA_KEY)

# Load animations
idle_img = pygame.image.load("assets/idle.png").convert_alpha()
talk_img = pygame.image.load("assets/talk.png").convert_alpha()

# I recommend prescaling your image and removing this scaling as it is not exactly the best 
idle_img = pygame.transform.scale(idle_img, (WIDTH, HEIGHT))
talk_img = pygame.transform.scale(talk_img, (WIDTH, HEIGHT))

# Get audio session ( Configure this for the correct app audio session )
session = audioengine.get_session("Discord.exe")

# Loop definitions (for dragging and the window loop itself)
dragging = False
drag_offset = (0, 0)
running = True

# Running Loop 
while running:
    # Quit and ESC handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Set window BG 
    screen.fill(CHROMA_KEY)
    
    # Check if audio is above threshhold
    talking = audioengine.talk_check(session)
    # Set animation
    if talking > 0.0001:  
        screen.blit(talk_img, (0, 0))
    else:
        screen.blit(idle_img, (0, 0))

    # Set window fps
    pygame.display.flip()
    clock.tick(FPS)

    # Window Drag handler 
    # Check if mousebutton is held down 
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Checks if LEFT mouse button is held down
        if event.button == 1:
            # Set current mode to dragging
            dragging = True
            # Create window position/rectangle pointer for windows api 
            pos = ctypes.wintypes.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            # Calculate dragging offset to avoid snapping
            drag_offset = (pos.x - rect.left, pos.y - rect.top)

    # Check mouse LEFT mousebutton release 
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            # Turn off dragging mode
            dragging = False

    # Check for mouse motion 
    if event.type == pygame.MOUSEMOTION:
        # check for dragging mode
        if dragging:
            # Set new window poistion 
            pos = ctypes.wintypes.POINT() 
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
            ctypes.windll.user32.SetWindowPos(hwnd, 0, pos.x - drag_offset[0], pos.y - drag_offset[1], 0, 0, 0x0001 | 0x0010)

pygame.quit()

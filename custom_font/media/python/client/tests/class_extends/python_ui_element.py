from com.asledgehammer import Pythoid
from zombie.core.fonts import AngelCodeFont
from zombie.Lua import LuaManager
from zombie.ui import UIManager, UIElement, UIFont

class PythonUIElement(UIElement):
    
    def __init__(self):
        super(PythonUIElement, self).__init__()
        print("Adding AngelCodeFont..")
        mod = LuaManager.GlobalObject.getModInfoByID('pymod')    
        modDir = mod.getDir()
        self.font = AngelCodeFont(
            modDir + '/media/fonts/daggersquare.fnt',
            modDir + '/media/fonts/daggersquare_0.png')
        print('font: ' + str(self.font))


    def renderText(self, x, y, font, text, red, green, blue, alpha):
        # type: (int, int, UIFont | AngelCodeFont, str, float, float, float, float) -> None
        if isinstance(font, UIFont):
            self.DrawText(font, text, x, y, red, green, blue, alpha)
        elif isinstance(font, AngelCodeFont):
            font.drawString(x, y, text, red, green, blue, alpha)

    def render(self):
        super(PythonUIElement, self).render()
        self.renderText(64, 64, self.font, "Hello, Python 2!", 1, 1, 1, 1)
    
    def isMouseOver(self):
        return super(PythonUIElement, self).isMouseOver()

# This allows for Kahlua to play with the object like a Java class
Pythoid.expose(PythonUIElement)

def mainmenu_enter():
    print('Adding Custom UI..')
    element = PythonUIElement()
    UIManager.AddUI(element)

Events['OnMainMenuEnter'].add(mainmenu_enter)

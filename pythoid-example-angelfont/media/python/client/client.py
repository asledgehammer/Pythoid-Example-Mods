import sys

def mainmenu_enter():
    # print("Hello, Main Menu!")
    print(getCore())

Events['OnMainMenuEnter'].add(mainmenu_enter)

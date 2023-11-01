from func import *

root = Tk()
root.title("Minesweeper by VegaPac")
root.resizable(False, False)

icon = PhotoImage(file="assets/mine128x128.png")
root.iconphoto(True, icon)

menu = Menu(root)
menu.create_menu()

root.mainloop()

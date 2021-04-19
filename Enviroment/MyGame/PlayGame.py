import threading
import Gui
import Ai

guiI = Gui.GuiInterface()
condition = threading.Event()


def main():
    guiI.setGuiI(guiI)
    guiI.setCondition(condition)
    guiI.showTableCaro()
    print("hello")
    ai = Ai.Play(condition, guiI, guiI.event)
    ai.setDaemon(True)
    ai.start()


if __name__ == '__main__':
    main()
    guiI.callInfinite()

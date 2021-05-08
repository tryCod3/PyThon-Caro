import threading
import Gui
import Ai

guiI = Gui.GuiInterface()
condition = threading.Event()
condition_choise = threading.Event()


def main():
    guiI.setGuiI(guiI)
    guiI.setCondition(condition)
    guiI.setCondition_Choise(condition_choise)
    guiI.showTableCaro()
    ai = Ai.Play(condition, condition_choise, guiI, guiI.event)
    ai.setDaemon(True)
    ai.start()


if __name__ == '__main__':
    main()
    guiI.callInfinite()

import MaxPlus


class VpGrab():
    def __init__(self):
        pass

    def grabtofile(self, filename):
        command = MaxPlus.Core_EvalMAXScript('''grab = gw.GetViewportDIB()
        grab.filename = @"''' + filename + '''"
        save grab
        close grab''')
        return True
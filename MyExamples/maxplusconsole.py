from PySideKick import Console
from maxhelpers import MaxPlusConsole

main = MaxPlusConsole.MaxWidget()
main.setCentralWidget(Console.QPythonConsole())
main.show()
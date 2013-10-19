(
	clearlistener()
	
	currdir = getFilenamePath(getThisScriptFilename())
	ini = currdir + "settings.ini"
	pyfile = getINISetting ini "Settings" "Filename"
	pyfile = pyfile
	
	python.ExecuteFile pyfile
)
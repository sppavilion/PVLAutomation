from os import listdir
import os
import lib.Constants as constants
API_DICT={}
path = os.getcwdu()
projectDir = path.strip().split("/"+constants.project_name)[0]
projectDir = projectDir + "/" + str(constants.project_name)

tmplDir = projectDir + "/resources/tmpl"
for tmpl in listdir(tmplDir):
    if tmpl.endswith('.tmpl'):
        with open(tmplDir+"/"+tmpl, 'r') as content_file:
            API_DICT[tmpl[:-5]]=content_file.read()
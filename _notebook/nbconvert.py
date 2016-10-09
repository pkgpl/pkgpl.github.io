import sys
import os
import time

if len(sys.argv) < 2:
    print("input: notebook file")
    sys.exit(1)

def run(cmd):
    print(cmd)
    os.system(cmd)

def nbrename(nbname):
    nbext='.ipynb'
    if nbname.endswith(nbext):
        nbname=nbname.split(nbext)[0]
    today=time.strftime("%Y-%m-%d")
    return today+"-"+nbname.lower().replace(' ','-')

f=sys.argv[1]
codedir="./markdown/"
configpy=codedir+"jekyll.py"

nbname=nbrename(f)
md=nbname+".md"
nbfilesdir=nbname+"_files"

linenos=False
if linenos:
    tpl=codedir+"jekyll_linenos.tpl"
else:
    #tpl=codedir+"jekyll.tpl"
    tpl=codedir+"jekyll_noyml.tpl"

run("jupyter nbconvert --to markdown {0:s} --config {1:s} --template={2:s} --output={3:s}".format(f,configpy,tpl,nbname))
run("python {0:s}markdown_imgcopy.py {1:s} {2:s}".format(codedir,md,md))
run("python {0:s}markdown_eqnos.py < {1:s} > ../_posts/{1:s}".format(codedir,md))
os.remove(md)

if os.path.exists(nbfilesdir):
    print(nbfilesdir)
    run("mv {0:s}/* ../images".format(nbfilesdir))
    os.rmdir(nbfilesdir)


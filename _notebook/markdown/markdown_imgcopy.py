# Copy imgs in markdown file to jekyll image directory

imgdir="../images/"
imgdirjk="{{site.baseurl}}/images/"

import sys,re,os,shutil

if len(sys.argv) < 3:
    print("{0:s} [input markdown file name] [output markdown file name]".format(sys.argv[0]))
    print("no space is allowed in the file names")
    sys.exit(1)

mdname=sys.argv[1]
mdout=sys.argv[2]
print("processing "+mdname)
mdbase=os.path.splitext(os.path.split(mdout)[1])[0]
filesdir=mdbase+'_files'

f=open(mdname,'r')
md=f.read()
f.close()

imgs=re.findall('!\[.*?\]\(.+?\)',md)
for img in imgs:
    imgpath=re.search('\((.+)\)',img).group(1)
    imgname=os.path.split(imgpath)[1]
    if imgname.startswith(mdbase):
        imgcopy=imgdir+imgname
        imgjk=imgdirjk+imgname
    else:
        imgcopy=imgdir+mdbase+'-'+imgname
        imgjk=imgdirjk+mdbase+'-'+imgname
    print(imgpath+" => "+imgcopy)

    md=re.sub('\]\('+imgpath+'\)',']('+imgjk+')',md)
    shutil.copy2(imgpath,imgcopy)
    os.remove(imgpath)

f=open(mdout,'w')
f.write(md)
f.close()

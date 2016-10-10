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

f=open(mdname,'r')
md=f.read()
f.close()

imgs=re.findall('!\[.*?\]\(.+?\)',md)
for img in imgs:
    imgname=re.search('\((.+)\)',img).group(1)
    imgbase=os.path.split(imgname)[1]
    imgcopy=imgdir+'/'+mdbase+'-'+imgbase
    imgjk=imgdirjk+'/'+mdbase+'-'+imgbase
    print(imgname+" => "+imgcopy)
    md=re.sub('\]\('+imgname+'\)',']('+imgjk+')',md)
    shutil.copy2(imgname,imgcopy)
    os.remove(imgname)

f=open(mdout,'w')
f.write(md)
f.close()

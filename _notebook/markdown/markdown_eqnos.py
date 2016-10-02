# Markdown preprocessor 
# equation, table, figure numbering
#
# reference,cite: @eq:label, @tbl:label, @fig:label

# 2015.10.27. Wansoo Ha (wansooha@gmail.com)

import sys,re
out=sys.stdin.readlines()

def counter(reg,lines):
	queue={} # cross-ref info
	out=[]
	count=0 # eq, tbl, fig number (from 1)
	for line in lines:
		mt=re.findall(reg,line)
		st=line
		for item in mt:
			if not item in queue:
				count+=1
				queue[item]=count
			st=st.replace(item,"%d"%queue[item])
		out.append(st)
	return out

base="(@%s:\w+)"
out=counter(base%"eq",out)
out=counter(base%"tbl",out)
out=counter(base%"fig",out)

for line in out:
	sys.stdout.write(line)

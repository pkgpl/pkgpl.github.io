---
layout: post
title: GNU Quick Plot (gnuqp)
date: 2014-07-27 23:25:06.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- gnuplot
- gpl
- python
- automation
---
<p><a href="http://www.gnuplot.info" target="_blank">Gnuplot</a>은 리눅스에서 텍스트파일에 저장된 값을 빠르게 그림으로 그려주는 프로그램입니다. 다양한 기능을 가지고 있지만, 제 경우에는 주로 수치해석 후 결과 확인용으로 씁니다.<br />
gnuplot으로 그림을 그릴 때에는 command line 상에서 <code>gnuplot</code>이라고 치고 들어가서 gnuplot 명령어들을 이용하여 그림을 그리고 <code>q</code>를 입력하여 빠져나옵니다.<br />
그런데 간단히 결과를 확인해보기 위해서 gnuplot에 들어가서</p>
```
p 'file1' w l,'file1' u 1:3 w l,'file1' u 1:4 w p
```
<p>또는</p>
```
set grid
set xrange[:10]
set log y
p 'file1' w l,'file2' w l,'file3' w l
```
<p>과 같이 매번 치려니 귀찮다는 생각이 들었습니다. 그래서 gnuqp (GNU Quick Plot)를 만들었습니다. 이 script를 사용하면 command line 상에서 바로 gnuplot 명령어를 사용하여 그림을 그릴 수 있습니다. 사용 방법은 아래와 같습니다.</p>
```
Usage :
gnuqp [options] filename1 [u 1:2] [w l], filename2 [u 1:2] [w l], filename3 ...
```
<p>실행파일 이름, 몇 가지 setting 관련 옵션들, 이후에는 gnuplot의 plot 명령어를 입력합니다.</p>
```
Required parameters :
filename1
Empty filename[2,3,...] will be replaced by the filename1
```
<p>두 번째 위치부터는 파일명을 생략하면 첫 번째 파일명으로 대체합니다. 하나의 파일에서 여러 column들을 그릴 때 편리합니다.</p>
```
Optional parameters :
u 1:2   : columns you want to plot
w [lp..]: line style- line, point, dot or impulse ..etc (default: w l)
```
<p>plot 명령어의 옵션들 중에는 using (columns)과 with (line style)만 지원합니다. 그 외의 명령은 제가 잘 안 써서요^^.<br />
위의 옵션을 주지 않았을 때 기본적으로 <code>with line</code> 옵션으로 그립니다.</p>
```
-p      : do not run gnuplot. just print the gnuplot command
-c      : no comma seperation - the arguments are filenames seperated with a blank- use with glob pattern
-l       : set logscale y
-g      : set grid
-x[:10] : set xrange [:10]
-y[1:5] : set yrange [1:5]
```
<p>위의 옵션들은 gnuplot의 setting을 간편하게 하기 위해 만들었습니다.</p>
<p><code>-p</code> 옵션을 붙이면 gnuplot의 명령어만 출력하고 그림은 안 그립니다.</p>
<p><code>-c</code> 옵션을 붙이면 파일들을 기본 옵션(with line)으로 그립니다. 이 때 파일명들 사이의 “,”를 생략하고 파일명만 씁니다. command line상에서 glob pattern을 이용하여 여러 그림을 그릴 수 있도록 하기 위한 옵션입니다. 예를 들면, 다음과 같은 경우죠.</p>
```
./gnuqp.py -p -c file.00*
->; p 'file.0010' w l,'file.0020' w l,'file.0030' w l,'file.0040' w l,'file.0050' w l
```
<p>나머지 gnuplot setting들은 위의 설명으로 충분할 것이라 생각합니다.<br />
앞에 예를 들었던 명령어들을 gnuqp를 이용하여 실행한다면 다음과 같습니다.</p>
```
(gnuplot)
p 'file1' w l,'file1' u 1:3 w l,'file1' u 1:4 w p
(q)
```
<p>는 <code>gnuqp file1, u 1:3, u 1:4 wp</code>,</p>
```
(gnuplot)
set grid
set xrange[:10]
set log y
p 'file1' w l,'file2' w l,'file3' w l
(q)
```
는 <code>gnuqp file1, file2, file3 -g -l -x[:10]</code>와 같이 실행할 수 있습니다. gnuqp는 [gpl]({% post_url 2014-07-26-geophysical-prospecting-library %})에 포함되어 있습니다.

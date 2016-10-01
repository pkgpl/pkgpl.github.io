---
layout: post
title: Makefile 사용법
date: 2014-07-12 22:09:28.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- Makefile
---
<p>Makefile의 기초적인 사용법을 알아봅시다.</p>
<h1>Makefile이 필요한 경우</h1>
<p>먼저, 다음과 같이 3개의 source 파일이 있을 때 컴파일하는 과정을 알아보겠습니다.</p>
<p>첫 번째 파일: main.f</p>
```fortran
       implicit none
       print *, 'main'
       call sub1()
       call sub2()
       end
```
<p>두 번째 파일: sub1.f</p>
```fortran
       subroutine sub1()
       print*, 'sub1'
       end
```
<p>세 번째 파일: sub2.f</p>
```fortran
       subroutine sub2()
       print*, 'sub2'
       end
```
<p>main.f 파일에서 sub1.f와 sub2.f에 있는 subroutine들을 불러오는 매우 간단한 프로그램입니다. 여기서는 하나의 파일 안에 subroutine을 다 넣는 것이 더 편하지만, Makefile 연습을 위해 세 개의 파일로 나누어 놓았습니다.<br />
이렇게 세 개의 파일을 가지고 실행 파일을 만들기 위한 명령은 다음과 같죠.</p>
```
f77 -c -O2 -o main.o main.f
f77 -c -O2 -o sub1.o sub1.f
f77 -c -O2 -o sub2.o sub2.f
f77 -o main main.o sub1.o sub2.o
```
<p>위 명령에서 <code>-c</code> 옵션은 source code를 가지고 object file을 생성하라는 의미입니다. 각각의 source file들에 대해 object file을 생성하고 나중에 링크시켜서 실행파일을 만듭니다. <code>-O2</code>는 compile 할 때 optimization level 을 2로 하라는 의미, <code>-o 파일명</code> 은 output file을 <code>-o</code> 다음에 나오는 파일명으로 만들라는 의미입니다. 마지막 줄에서 세 개의 objective file들을 링크시켜서 <code>main</code> 이라는 실행파일을 생성합니다. 실행 파일의 실행 결과는 다음과 같습니다.</p>
```
$ ./main
main
sub1
sub2
```
<p>잘 실행됩니다. 그런데 만약 sub1.f 파일을 수정했다면 어떻게 해야할까요? 다시 컴파일하기 위해서는</p>
```
f77 -c -O2 -o sub1.o sub1.f
f77 -o main main.o sub1.o sub2.o
```
<p>라고 수정한 파일만 다시 컴파일한 후, 다른 object file들과 링크시켜서 실행파일을 만들어야겠죠. 좀 귀찮습니다. 자동으로 할 수 있으면 좋겠죠. shell script를 하나 만들어서 처음의 컴파일 명령 4줄을 다 써 넣으면 자동으로 실행할 수 있습니다. 하지만, 그렇게 되면 sub1.f 파일을 고쳤을 때 main.f와 sub2.f 파일까지 새로 컴파일하게 됩니다. 프로그램이 간단할 때는 큰 문제가 없지만, 프로그램이 크고 복잡해지면 컴파일 시간이 오래 걸린다는 문제가 생기게 됩니다. Source code 내용에 따라서 특정 code는 다른 code보다 먼저 컴파일해야만 하는 경우도 생길 수 있습니다. 이런 경우에 편리하게 쓸 수 있는 프로그램이 바로 make입니다. make는 실행했을 때 현재 디렉토리에 있는 Makefile 이라는 파일을 찾아 build 작업을 수행합니다.</p>
<h1>Makefile 작성법</h1>
<p>Makefile의 작성법은</p>
```make
Target: Dependency list
[Tab] Command
```
<p>와 같습니다. Target은 만들고 싶은 대상, Dependency list는 Target을 만들기 전에 먼저 만들어져야 할 대상들, Command는 Target을 만드는 방법(command line 명령어)입니다. 한 가지 주의할 점은 Command 앞에는 Tab이 들어가야 한다는거죠. 그럼 위의 세 파일을 컴파일하기 위한 기초적인 Makefile을 살펴보겠습니다.</p>
```make
# target: dependency list
# [tab] command
F77=gfortran

all: main

main: main.o sub1.o sub2.o
    $(F77) -O2 -o main main.o sub1.o sub2.o
main.o: main.f
    $(F77) -O2 -c main.f
sub1.o: sub1.f
    $(F77) -O2 -c sub1.f
sub2.o: sub2.f
    $(F77) -O2 -c sub2.f
clean:
    rm main main.o sub1.o sub2.o
```
<p><code>F77=gfortran</code> 이라고 먼저 선언을 했습니다. 여기서 <code>F77</code>은 매크로(일종의 변수)입니다. 이런식으로 선언을 해두면 뒤에 <code>$(F77)</code>과 같이 필요할 때 불러서 쓸 수 있습니다. 컴파일러를 바꿀 때 <code>gfortran</code> 대신에 <code>f77</code> 이나 <code>ifort</code> 등으로 바꿔주면 되겠죠.</p>
<p>다음에 나오는게 <code>all</code> 이라는 Target입니다. Dependency list에는 <code>main</code>이 있고 Command는 없네요. Command line에서 make를 실행하면 현재 디렉토리에 있는 Makefile을 찾아 제일 처음에 나오는 Target만 실행합니다. <code>make target1</code>과 같이 실행하면 Makefile내에서 <code>target1</code> 이라는 Target을 찾아 실행합니다. 따라서 맨 처음 Target을 <code>all</code> 이라고 지정해두고 Dependency list에 자신이 만들고 싶은 Target들을 적어두면 make만 쳐서 원하는 Target들을 한 번에 만들 수 있겠죠. 전체적인 compile 과정은 다음과 같습니다.</p>
<ol>
<li>제일 처음에 나오는 <code>all</code> 이라는 Target을 만나서 Dependency list를 확인한다. <code>main</code>이라는 Dependency를 찾았다.</li>
<li>Dependency를 만족하기 위해 <code>main</code>이라는 Target을 찾는다. 그리고 <code>main</code>의 Dependency list - <code>main.o, sub1.o, sub2.o</code> 를 찾았다.</li>
<li><code>main.o</code>라는 Target을 찾아서 Dependency <code>main.f</code>를 찾고 현재 디렉토리에 <code>main.o</code> 파일이 없거나 <code>main.o</code> 파일의 수정 시간이 <code>main.f</code> 파일의 수정시간보다 이전일 때 <code>gfortran -O2 -c main.f</code> 라는 Command를 실행한다. 그렇지 않은 경우에는 아무 것도 실행하지 않는다.</li>
<li><code>main.o</code>가 잘 만들어졌으면 다시 <code>main</code> 이라는 Target으로 넘어가 <code>sub1.o</code>, <code>sub2.o</code>라는 Dependency를 같은 방법으로 만족하고 돌아온다.</li>
<li><code>main</code>의 Dependency 세 개가 다 만족되었으면 <code>gfortran -O2 -o main main.o sub1.o sub2.o</code> 라는 Command를 실행하여 <code>main</code>이라는 Target을 만든다.</li>
<li><code>main</code>이라는 Target이 만들어졌으면 <code>all</code>이라는 Target으로 돌아간다.</li>
<li><code>all</code>의 Dependency가 다 만족되었지만, Command가 없으므로 make가 끝난다.</li>
</ol>
<p><code>clean</code>이라는 Target은 처음에 나오지도 않고 다른 Target의 Dependency 에도 들어가지 않으니 실행이 안 됩니다. 명령줄에서 make clean이라고 실행했을 때만 실행이 되죠. <code>clean</code>은 Dependency list가 비어있으니까 make clean이라고 실행하면 해당하는 Command를 항상 실행하게 됩니다. 보통 make로 생성된 파일들을 지우기 위해 <code>clean</code>이라는 Target을 만듭니다.</p>
<p>여기까지만 배우고 끝내기에는 아쉽습니다. Makefile에는 강력한 기능들이 많기 때문이죠. 몇 개만 더 살펴봅시다.</p>
<h1>확장자 규칙</h1>
<p>아래의 Makefile은 compiler과 compile option이 약간 바뀐 것 말고는 위의 Makefile과 같은 기능을 합니다.</p>
```make
# $^ : dependency list
# $@ : target

F77=ifort
FFLAG=-assume byterecl -O2
TARGET=main
OBJECTS=main.o sub1.o sub2.o

all: $(TARGET)

$(TARGET): $(OBJECTS)
    $(F77) -o $@ $^

.SUFFIXES: .o .f
%.o: %.f
    $(F77) ${FFLAG} -c $&lt;

clean:
    rm $(TARGET) $(OBJECTS)
```
<p>Command 위치에서 <code>$^</code>는 Dependency list를 자동으로 입력해줍니다. 또한 <code>$@</code>는 Target 이름을 자동으로 입력해줍니다.</p>
```make
.SUFFIXES: .o .f
%.o: %.f
    $(F77) ${FFLAG} -c $&lt;
```
<p>는 확장자 규칙으로, <code>.SUFFIXES: .o .f</code> 는 <code>.o</code> 라는 확장자와 <code>.f</code>라는 확장자를 특별히 중요하게 생각하라는 뜻입니다. 그 아래에 나오는 내용은 <code>.o</code> 확장자를 가진 Target에 대해 <code>.f</code> 파일을 이용한 Dependency 와 Command를 자동으로 생성해주는 기능을 합니다. 따라서 처음의 Makefile에 있었던 <code>main.o, sub1.o, sub2.o</code> 라는 Target과 Dependency, Command를 자동으로 만들어줍니다. 한 가지 주의할 점은, 확장자 규칙에서는 앞서 나왔던 <code>$^</code>가 아닌, <code>$&lt;</code>를 사용한다는 점입니다. <code>$&lt;</code>는 확장자 규칙에서만 사용되며, 타겟보다 나중에 변경된 종속 항목들을 의미합니다. Build 과정이 복잡할 때 Makefile은 큰 힘을 발휘합니다.</p>
<p>더 자세한 내용을 알고 싶으신 분들은 <a href="http://wiki.kldp.org/KoreanDoc/html/GNU-Make/GNU-Make.html">임대영님의 GNU Make 강좌</a>를 참고하세요.</p>
<p><em>예전에 다른 블로그에 올렸던 글인데, 이곳에 복사해둡니다.</em></p>

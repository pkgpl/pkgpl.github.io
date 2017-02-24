---
layout: post
title: Rakefile 사용법
date: 2014-07-26 23:37:29.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- rakefile
- ruby
---
<h1>Rakefile 기본 사용법</h1>
Rakefile은 [Makefile]({% post_url 2014-07-12-makefile_basic %})과 비슷한 역할을 하는, Ruby script입니다. 따라서 Ruby라는 언어의 강력한 기능들을 그대로 가져다 쓸 수 있다는 장점이 있습니다. 단, Ruby를 알아야 제대로 사용할 수 있겠죠. Makefile을 <code>make</code>라는 명령어로 실행하듯이, Rakefile은 <code>rake</code>라는 명령어로 실행합니다. Rakefile 작성법을 Makefile 작성법과 비교하며 살펴보도록 하겠습니다. Makefile의 기본적인 작성법은
```make
Target: Dependency list
[Tab] Command
```
<p>였죠. Rakefile도 유사합니다. 단, Ruby syntax를 사용하죠. 기본적인 작성법은 다음과 같습니다.</p>
```ruby
task :name => [:prereq1, :prereq2] do
    Command
end
```
<p>Makefile에서 Target에 해당하는 것이 Rakefile의 task입니다. 잘 살펴보면 task라는 함수명과 Hash, Block 두 개의 argument로 이루어진 구조라는 것을 알 수 있습니다. Hash의 key는 target이 되고 value는 prerequisites (dependency list)가 됩니다. Block은 실행해야 할 명령들로 이루어집니다. 특별히 compile하는 경우와 같이 파일을 작성하는 task의 경우에는</p>
```ruby
file "name" => ["prereq1", "prereq2"] do
    Command
end
```
<p>와 같이 file task를 사용합니다. Command 부분에서 <code>name</code> 또는 dependency list (prereq1, prereq2, … )를 사용하고 싶을 때는</p>
```ruby
file "name" => ["prereq1", "prereq2"] do |t|
    sh "f77 -o #{t.name} #{t.prerequisites.join(' ')}"
end
```
<p>과 같이 사용하여 <code>f77 -o name prereq1 prereq2</code>와 같은 결과를 얻을 수도 있습니다.</p>
그럼 [앞에서 만들었던 Makefile]({% post_url 2014-07-12-makefile_basic %})과 같은 기능을 하는 Rakefile을 만들어 비교해 보겠습니다. 앞에서 만들었던 Makefile은 다음과 같고,

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

<p>이에 해당하는 Rakefile은 다음과 같습니다.</p>

```ruby
f90='gfortran'

task :default => ['main.e']
file 'main.e' => ['main.o','sub1.o','sub2.o'] do |t|
    sh "#{f90} -o #{t.name} main.o sub1.o sub2.o"
end

file 'main.o' => ['main.f'] do
    sh "#{f90} -c main.f"
end
file 'sub1.o' => ['sub1.f'] do
    sh "#{f90} -c sub1.f"
end
file 'sub2.o' => ['sub2.f'] do
    sh "#{f90} -c sub2.f"
end

require 'rake/clean'
CLEAN.include('*.o')
CLOBBER.include('main.e')
```
<p><code>task :default</code> 부분은 Makefile에서 <code>all</code> 이라는 target을 지정해서 사용했던 것과 같은 역할을 합니다. 단, Rakefile에서는 default task가 맨 처음에 나올 필요가 없습니다. 파일 내 아무데나 나와도 잘 인식합니다. 중간 부분은 Makefile과 매우 유사하므로 특별한 설명이 필요 없겠죠? 뒤에 있는 clean task는 rake에 이미 지정되어 있는 task입니다. 사용하기 위해서는 <code>rake/clean</code>을 불러옵니다. <code>rake clean</code>을 실행하면 <code>CLEAN</code>에 포함된 파일들을 지워주고 <code>rake clobber</code>를 실행하면 <code>CLOBBER</code>와 <code>CLEAN</code>에 지정된 파일들을 모두 지워줍니다. 위에서 볼 수 있는 것처럼, 최종 결과 파일만 <code>CLOBBER</code>에 포함시키고 중간에 생성되는 파일들은 <code>CLEAN</code>에 포함시키면 편리하게 사용할 수 있습니다.</p>
<h1>확장자 규칙</h1>
<p>Makefile에서는 확장자 규칙을 이용해 편리하게 compile할 수 있었죠? Rakefile에도 같은 기능이 있습니다. 비교해볼까요?</p>
<h3>Makefile</h3>
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
    $(F77) ${FFLAG} -c $^

clean:
    rm $(TARGET) $(OBJECTS)
```
<h3>Rakefile</h3>
```ruby
F90='ifort'
FFLAG='-assume byterecl -O2'
TARGET='main.e'
SRC=FileList['*.f']
OBJ=SRC.ext('o')

task :default => TARGET
file TARGET => OBJ do
    sh "#{F90} -o #{TARGET} #{OBJ}"
end
rule '.o' => '.f' do |t|
    sh "#{F90} #{FFLAG} -c #{t.source}"
end

require 'rake/clean'
CLEAN.include('*.o')
CLOBBER.include('main.e')
```
<p>Rakefile에서는 <code>rule</code>이라는 함수가 Makefile의 확장자법칙과 같은 역할을 합니다. <code>FileList</code> 명령은 glob pattern (여기서는 <code>‘*.f’</code>)을 받아들여서 해당하는 파일들의 목록을 만들어주고, <code>FileList</code> 객체의 <code>ext</code> method는 목록에 있는 파일들의 확장자를 원하는 확장자로 바꿔서 새로운 FileList를 만들어줍니다. 앞에서 dependency list를 불러올 때 <code>t.prerequisites.join(' ')</code>이라고 사용했었는데 여기서는 <code>t.source</code>라고 사용했습니다. 앞의 방법은 전체 dependency list를 문자열로 만들어주고(‘ ‘을 이용하여 각각을 합치죠), 뒤의 방법은 dependency list의 첫 번 째 항목만 문자열로 만들어줍니다. 위의 예에서는 dependency list에 <code>‘.o’</code>에 해당하는 <code>‘.f’</code> 파일 하나만 있으니까 <code>t.source</code>라고 사용해도 무관하겠죠?</p>
<h1>작업 설명</h1>
<p>Makefile에 없고 Rakefile에만 있는 기능 중 하나로, task에 설명을 달 수 있는 기능이 있습니다. task 또는 file task 바로 윗 줄에<br />
<code>desc "description"</code><br />
이라고 설명을 추가해주면 <code>rake -T</code>라고 실행했을 때 설명과 함께 task 목록을 보여줍니다. Rakefile을 직접 보지 않고도 안에 무슨 task가 있는지 확인할 수 있는 유용한 기능이죠^^</p>
<p>더 자세한 내용은 다음 <a href="http://docs.seattlerb.org/rake/">site</a>를 참고하세요.</p>
<p><em>예전에 다른 블로그에 올렸던 글인데, 이곳에 복사해둡니다.</em></p>

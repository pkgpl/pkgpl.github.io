---
layout: post
title: SConstruct 사용법
date: 2014-07-27 22:30:18.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- Python
- SConstruct
---
SConstruct는 [Makefile]({% post_url 2014-07-12-makefile_basic %})과 비슷한 역할을 하는, Python script입니다. 따라서 Python이라는 언어의 강력한 기능들을 그대로 가져다 쓸 수 있다는 장점이 있습니다. Makefile을 make라는 명령어로 실행하듯이, SConstruct는 scons라는 명령어로 실행합니다. SConstruct file의 작성법은 [Makefile]({% post_url 2014-07-12-makefile_basic %})이나 [Rakefile]({% post_url 2014-07-26-rakefile_basic %})의 작성법과는 차이가 있습니다. 작성법을 살펴보기 전에 먼저 ‘Environment’와 ‘Builder’라는 개념에 대해 살펴보겠습니다.</p>
<h1>Environments</h1>
<p>Makefile에서는 기본적으로 Shell의 환경변수들을 가져다가 썼습니다. 물론 PATH 환경변수도 가지고 오기 때문에 compiler의 절대경로를 써주지 않아도 알아서 잘 compile을 했었습니다.<br />
반면에, scons는 기본적으로 Shell의 환경변수들을 가져오지 않습니다. scons를 설치할 때 기본적인 compiler들(gcc, gfortran 등)은 알아서 찾아내기 때문에 보통은 문제가 없지만 특정한 compiler(icc, ifort 등)를 사용하고 싶은 경우 compile 관련 환경변수(construction variables)에 절대경로를 지정해주거나 Shell의 환경변수를 가지고 옵니다. Shell의 환경변수들을 전부 가지고 오고 compiler로 ifort를 사용할 경우 script에 다음과 같이 써줍니다.</p>

{% highlight python %}
import os
DefaultEnvironment(ENV=os.environ, FORTRAN='ifort',
    FORTRANFLAGS='-assume byterecl -O2', LINK='ifort')
{% endhighlight %}

<p>scons에는 위에 사용한 Default Environment외에도 사용자가 마음대로 Environment를 만들 수 있습니다. 아래와 같이 쓸 경우 myEnv라는 새로운 Environment를 만들어 사용할 수 있습니다. 이런 식으로 여러 개의 Environment들을 만들어 필요에 따라 같은 프로그램도 옵션을 바꿔가며 compile할 수 있습니다.</p>

```python
import os
DefaultEnvironment(ENV=os.environ, FORTRAN='ifort',
    FORTRANFLAGS='-assume byterecl -O2', LINK='ifort')
myEnv=Environment(ENV=os.environ, CFLAGS='-O3',
    FORTRANFLAGS='-O1')
```

<p>위의 환경 설정 내용을 이후에 사용하기 위해 <code>myenv.py</code>라는 파일에 저장해두었다고 가정 하겠습니다.</p>
<h1>Builders</h1>
<p>scons는 기본적으로 많이 사용되는 프로그램들의 compile 방법들을 알고 있습니다. Compile하는 object를 builder라고 하는데, c/c++, fortran, java, TeX, LaTeX, tar, zip 등 다수의 builder들이 존재합니다. 따라서 원하는 builder에 알맞은 target과 source 이름만 넣어주면 scons가 알아서 compile합니다. 필요한 변수(옵션)들은 해당 Environment에서 가지고 옵니다. 기본적인 작성법은 다음과 같습니다.</p>
<pre><code>Program('target1.e', 'source1.f')
myEnv.Program('target2.e', 'source2.c')
</code></pre>
<p>첫 번째 줄은 ‘source1.f’라는 파일로부터 ‘target1.e’ 라는 파일을 생성하는 명령입니다. 이 때 필요한 변수들은 Default Environment에서 가지고 옵니다. 두 번째 줄은 ‘source2.c’라는 파일로부터 ‘target2.e’라는 파일을 생성하는 명령이고, 필요한 변수는 <code>myEnv</code>라는 Environment에서 가지고 옵니다. 위에서 <code>Program</code>이라는 명령은 source code에 해당하는 builder를 불러오는 역할을 하죠. 지금까지의 SConstruct script와 실행 결과를 살펴볼까요?</p>
```python
from myenv import *
Program('target1.e','source1.f')
myEnv.Program('target2.e','source2.c')
```
<p><code>scons</code>라고 실행하면,</p>
```
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
ifort -o source1.o -c -assume byterecl -O2 source1.f
gcc -o source2.o -c -O3 source2.c
ifort -o target1.e source1.o
gcc -o target2.e source2.o
scons: done building targets.
```
<p>와 같은 화면을 얻게 됩니다. 복잡한 내용은 빼고 실행 결과만 보고 싶을 경우 <code>scons -Q</code> 라고 실행하면 결과를 다음과 같이 보여줍니다.</p>
```
ifort -o source1.o -c -assume byterecl -O2 source1.f
gcc -o source2.o -c -O3 source2.c
ifort -o target1.e source1.o
gcc -o target2.e source2.o
```
<p>위의 실행 결과를 보면 source file의 확장자에 따라 필요한 compiler를 사용하고 필요한 환경변수들을 가져다가 사용했음을 알 수 있습니다. 특정 Compiler가 사용하는 환경변수는 <a href="http://www.scons.org/documentation.html">scons user manual</a>에서 찾아볼 수 있습니다.</p>
<h1>예제</h1>
<p>그럼 [앞에서 살펴보았던 예제]({% post_url 2014-07-12-makefile_basic %}) – <code>main.f, sub1.f, sub2.f</code> 는 어떻게 compile하는지 살펴보겠습니다.</p>

```python
from myenv import *
Program('main.e',['main.f','sub1.f','sub2.f'])
```
<p>위와 같이 source file이 여러 개인 경우 source file들을 list로 묶어줍니다. 다른 방법으로 아래와 같이 쓸 수도 있습니다. Split이라는 함수는 문자열을 나눠서 list로 만들어줍니다.</p>
```python
from myenv import *
obj=Split('main.f sub1.f sub2.f')
Program('main.e',obj)
```
<p>Makefile이나 Rakefile에 비해 상당히 간단하죠? 실행 결과는 다음과 같습니다.</p>
```
ifort -o main.o -c -assume byterecl -O2 main.f
ifort -o sub1.o -c -assume byterecl -O2 sub1.f
ifort -o sub2.o -c -assume byterecl -O2 sub2.f
ifort -o main.e main.o sub1.o sub2.o
```
<p>또 앞의 Makefile, Rakefile 예제들과는 달리 clean 이라는 target이 없습니다. scons -c 라고 실행하면 scons는 compile 과정에서 새로 생긴 파일들을 알아서 지워줍니다. 실행 결과는 다음과 같습니다.</p>
```
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Cleaning targets ...
Removed main.o
Removed sub1.o
Removed sub2.o
Removed main.e
scons: done cleaning targets.
```
<p>물론 특정 target만 만들고 싶을 때는 <code>scons main.o</code>와 같이 실행하여 하나의 target만 만들 수도 있습니다. <code>main.o</code>라는 target은 script 내에서 지정해준 적이 없지만 확장자 규칙에 따라 compile 중에 생기는 파일이기 때문에 앞에서와 같이 실행하면 알아서 만들어줍니다. 또한, 많은 경우 dependency도 알아서 check해줍니다.</p>
<p>만약 <code>Program()</code>에서 target을 생략하고 source만 적어주면 list의 첫 번째 source file 이름을 기준으로 target file 이름을 만들어 줍니다.</p>
```python
Program(['main.f','sub.f']) ## -&gt; target='main'
```
<p><a href="http://www.scons.org">SCons Homepage</a></p>
<p><em>예전에 다른 블로그에 올렸던 글인데, 이곳에 복사해둡니다.</em></p>

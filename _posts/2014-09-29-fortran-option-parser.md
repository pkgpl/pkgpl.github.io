---
layout: post
title: Fortran option parser
date: 2014-09-29 23:55:09.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- fortran
- gpl
---
[gpl]({% post_url 2014-07-26-geophysical-prospecting-library %})에서 사용하기 위해 개발한 포트란 option parser를 소개합니다. Option parser는 command line option들을 분석해서 프로그램에서 사용할 수 있도록 변수로 저장해주는 역할을 합니다. 리눅스나 맥에서 명령을 실행할 때
<pre><code>$ gcc -c -o main.e main.c
$ tar -zxvf file.tgz
</code></pre>
<p>와 같은 유닉스 표준 형태의 옵션이 있고,</p>
<pre><code>$ suximage n1=101 d1=0.5 perc=99 &lt; file.su
</code></pre>
<p>와 같이 <a href="http://www.cwp.mines.edu/cwpcodes/">Seismic Un*x</a>나 <a href="http://www.ahay.org">Madagascar</a> 등에서 사용하는 형태의 옵션도 있는데, 지금 소개해드리는 option parser는 두 번째 형태의 옵션을 지원합니다. Option parser는 한 번 작성한 프로그램의 재사용을 위해 매우 유용한 기능입니다. 우선 테스트 프로그램을 통해 사용 예를 살펴본 후 자세한 사용법을 보겠습니다.</p>
<h2>테스트 프로그램</h2>
<p>다음의 테스트 프로그램은 다양한 종류의 변수를 command line option으로부터 읽어서 출력하는 프로그램입니다.<br />
지원하는 자료형은 integer, single precision real, double precision real, logical, character입니다(complex는 아직까지 필요가 없어서 안 넣었습니다). 단일 변수 뿐 아니라 각각의 배열도 지원합니다. 필수 입력 옵션과 기본값을 가진 옵션을 구분하여, 필수 입력 옵션들 중 하나라도 command line option에 없을 경우 도움말을 출력하고 프로그램을 종료합니다.</p>
```fortran
        program test_optparse
        use gpl_optparse
        implicit none
        integer,parameter:: mxlen=100,mxstr=100
        integer:: i,io,ia(mxlen)
        integer:: j,ni,nf,nb,nd,ns
        real:: f,fo,fa(mxlen)
        logical:: b,bo,ba(mxlen)
        real(kind=8):: d,d_o,da(mxlen)
        character(len=mxstr) :: s,so,sa(mxlen)

        ! required parameters
        call from_par('i',i,'integer number')
        call from_par('f',f,'float: single precision real number')
        call from_par('d',d,'double precision')
        call from_par('b',b,'boolean/logical')
        call from_par('s',s,'string')

        ! optional parameters
        call from_par('io',io,1,'1','optional integer')
        call from_par('fo',fo,1.0,'1.0','optional float')
        call from_par('do',d_o,1.0d0,'1.0d0','optional double')
        call from_par('bo',bo,.true.,'T','optional boolean')
        call from_par('so',so,'','empty','optional string')

        ! array, required parameters
        call from_par('ia',ia,ni,'integer array')
        call from_par('fa',fa,nf,'float array')
        call from_par('da',da,nd,'double array')
        call from_par('ba',ba,nb,'boolean array')
        call from_par('sa',sa,ns,'string array')

        call help_par()
        !call report_par()

        print*,'i=',i
        print*,'f=',f
        print*,'d=',d
        print*,'b=',b
        print*,'s=',trim(s)
        print*,''
        print*,'ia=',ia(1:ni)
        print*,'fa=',fa(1:nf)
        print*,'ba=',ba(1:nb)
        print*,'da=',da(1:nd)
        print*,'sa=',(trim(sa(j))//'_',j=1,ns)
        print*,''
        print*,'io=',io
        print*,'fo=',fo
        print*,'do=',d_o
        print*,'bo=',bo
        print*,'so=',so
        end program
```
<h2>실행 결과</h2>
<p>위의 프로그램을 컴파일하여 아래와 같이 실행하면 변수들이 제대로 입력된 것을 확인할 수 있습니다. 문자열의 경우 문자열을 둘러싼 따옴표는 제거하고 변수에 저장합니다. 배열은 쉼표를 기준으로 배열의 원소를 나눕니다. 기본값을 가지고 있는 변수의 경우 command line option에 있으면 주어진 값을 저장하고 없으면 기본값을 저장합니다.</p>
<pre><code>$ ./test_optparse s=test.dat i=2 f=2.5 d=3.0 b=T ia=1,2,3,4 fa=1.0,2.0,3.0,4.0 da=1.,2.,3. ba=T,F,T sa=st,'ri',&quot;ng&quot; io=5 so=&quot;gpl&quot;
 i=           2
 f=   2.50000000
 d=   3.0000000000000000
 b= T
 s=test.dat

 ia=           1           2           3           4
 fa=   1.00000000       2.00000000       3.00000000       4.00000000
 ba= T F T
 da=   1.0000000000000000        2.0000000000000000        3.0000000000000000
 sa=st_ri_ng_

 io=           5
 fo=   1.00000000
 do=   1.0000000000000000
 bo= T
 so=gpl
</code></pre>
<p>만약 기본값이 없는 필수 옵션 중 하나라도 command line option에 빠져있다면 다음과 같이 도움말을 표시하고 프로그램을 종료합니다.</p>
<pre><code>$ ./test_optparse
 Required parameters:
     [i] i=             : integer number
     [f] f=             : float: single precision real number
     [d] d=             : double precision
     [b] b=             : boolean/logical
     [s] s=             : string
     [I] ia=            : integer array
     [F] fa=            : float array
     [D] da=            : double array
     [B] ba=            : boolean array
     [S] sa=            : string array
 Optional parameters:
     [i] io=1           : optional integer
     [f] fo=1.0         : optional float
     [d] do=1.0d0       : optional double
     [b] bo=T           : optional boolean
     [s] so=empty       : optional string
</code></pre>
<p>위의 도움말에서 i=integer, f=real, d=real(kind=8), b=logical, s=character(len=?)을 의미하고, 각각의 대문자는 배열을 의미합니다.</p>
<h2>사용법</h2>
<p>그럼 실제 모듈의 사용법을 알아보겠습니다. 모듈은 <code>use gpl_optparse</code> 또는 간편하게 <code>use gpl</code>로 불러올 수 있습니다. 가장 중요한 <code>from_par</code> 서브루틴은 다음과 같이 세 가지 방식으로 사용할 수 있습니다.</p>
```fortran
call from_par('parname',variable,'help message') !! 필수 옵션
call from_par('parname',variable_arr,len_arr,'help message') !! 필수 배열
call from_par('parname',variable,default,'default message','help message') !! 기본값이 있는 변수
```
<p>Command line option은 <code>parname=value</code> 형태로 입력 받게 됩니다. 위의 서브루틴들에서 <code>'parname'</code>은 이 때 사용되는 이름이고, <code>value</code>는 <code>variable</code>에 저장됩니다. &#8217;help message&#8217;는 도움말 출력시 보여주는 변수 설명입니다.</p>
<p>배열의 경우 <code>parname=value1,value2,value3</code>과 같은 형태로 입력받고, 입력받은 값은 <code>variable_arr</code>에 저장됩니다. 이 때 입력받은 원소는 <code>len_arr</code> 개입니다.</p>
<p>기본값이 있는 변수의 경우 <code>default</code>는 기본값이고, <code>'default message'</code>는 도움말 출력시 기본값을 보여주기 위한 문자열입니다.</p>
[함수 오버로딩을]({% post_url 2014-07-12-fortran_function_overloading %}) 사용하였기 때문에 정수, 실수 등의 자료형에 상관없이 위의 서브루틴들을 이용할 수 있습니다.
<p>기타 사용할 수 있는 서브루틴들과 함수는 다음과 같습니다.</p>
```fortran
call help_par()
call help_header('msg before the parameter help msg')
call help_footer('msg after the parameter help msg')
call force_help()

call report_par()

if(given_par('parname')) call do_something()
call from_parfile('parfile.txt')
```
<p>에서 <code>help_par</code>는 도움말 출력을 위한 서브루틴입니다. 도움말과 관련된 서브루틴들로는 도움말을 보강하기 위한 <code>call help_header('msg')</code>, <code>call help_footer('msg')</code>, 필수 옵션이 주어졌는지와 무관하게 도움말을 출력하기 위한 <code>call force_help()</code>가 있습니다. <code>report_par</code>는 입력받은 변수들을 출력해서 확인하기 위한 서브루틴입니다. 이 외에도 옵션이 주어졌는지 확인하기 위한 <code>logical function given_par('parname')</code> 함수, 옵션들을 저장해놓은 텍스트파일로부터 옵션들을 읽어들이기 위한 <code>call from_parfile('parfile.txt')</code>와 같은 명령이 있습니다.</p>
<p>참고로, command line option에 <code>par=parfile.txt</code>와 같은 옵션이 있으면 <code>parfile.txt</code>에서 먼저 변수를 읽은 후 command line option을 읽습니다. <code>parfile.txt</code>에 주어진 변수가 command line option에 다시 나오면 command line에 주어진 값을 사용합니다.</p>
<code>gpl_optparse</code> 모듈의 소스코드는 [gpl]({% post_url 2014-07-26-geophysical-prospecting-library %})의 <a href="https://github.com/pkgpl/gpl">GitHub</a>에서 받으실 수 있습니다.

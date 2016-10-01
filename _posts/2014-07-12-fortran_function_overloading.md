---
layout: post
title: 포트란과 함수 오버로딩
date: 2014-07-12 23:07:02.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- Fortran
- OOP
---
<h1>포트란과 객체지향 프로그래밍</h1>
<p>포트란이라 하면 옛날 언어라고 생각하기 쉬운데, 포트란 언어도 시대의 흐름에 따라 계속 발전해 오고 있습니다. 특히, 2003버전부터는 클래스와 상속 등을 지원하는 객체지향 프로그래밍 언어라 할 수 있습니다. 안타깝게도, 한글로 된 포트란 서적이 별로 없고, 출판된 것도 95버전까지밖에 안 나와 있어서 앞으로 블로그에서 몇 가지 객체지향 프로그래밍과 관련된 기능들을 소개하고자 합니다.</p>
<h2>포트란과 함수 오버로딩</h2>
<p>함수 오버로딩이란 같은 이름의 서브프로그램(서브루틴, 함수, 메소드 등)이 인자에 따라 다른 기능을 하는 것을 말합니다. 객체지향 프로그래밍의 다형성과 관련된 개념인데, 포트란에서는 90버전에 도입된 <code>interface</code>문을 이용하여 적용 가능합니다.</p>
<p>아래 예제는 2차원 좌표라는 자료형을 정의하고 좌표들 사이의 거리를 구하는 함수를 구현한 예제입니다. 자료형을 정의할 때 single precision 자료형 <code>point_sp</code>와 double precision 자료형 <code>point_dp</code> 두 가지를 정의했고, 따라서 함수도 single precision용 <code>distance_sp</code>와 double precision용 <code>distance_dp</code> 두 가지를 정의했습니다.</p>
```fortran
module point2d

type point_sp
    real x, y
end type

type point_dp
    real(kind=8):: x,y
end type

contains

    real function distance_sp(p1, p2) result(dist)
    type(point_sp), intent(in):: p1, p2
    dist=sqrt((p1%x-p2%x)**2+(p1%y-p2%y)**2)
    end function

    real(kind=8) function distance_dp(p1, p2) result(dist)
    type(point_dp), intent(in):: p1, p2
    dist=dsqrt((p1%x-p2%x)**2+(p1%y-p2%y)**2)
    end function

end module

program test_point2d
use point2d
type(point_sp):: s1,s2
type(point_dp):: d1,d2
real:: dist_s
real(kind=8):: dist_d

s1%x=0.0 ; s1%y=0.0
s2%x=3.0 ; s2%y=4.0

d1%x=0.0d0 ; d1%y=0.0d0
d2%x=3.0d0 ; d2%y=4.0d0

dist_s=distance_sp(s1,s2)
dist_d=distance_dp(d1,d2)

print*, dist_s, dist_d
end program

```
<p>위의 예제에서 두 개의 함수가 하는 일은 같지만, 정적 자료형 언어의 특성상 자료형에 따라 두 개의 함수를 정의해야 했습니다. 이 프로그램은 간단해서 별 문제가 없지만, 프로그램이 복잡해지면 이렇게 같은 기능의 다른 함수들로 인해 인터페이스가 복잡해지게 됩니다. 같은 기능의 함수들을 single/double과 같은 자료형에 상관없이 같은 이름으로 사용할 수 있다면 프로그래밍 인터페이스가 좀 더 단순해지겠죠. 위의 모듈에 아래의 interface 구문을 넣으면 <code>distance_sp</code> 함수와 <code>distance_dp</code> 함수를 모두 <code>distance</code>라는 이름으로 사용할 수 있습니다.</p>
```fortran
interface distance
    module procedure:: distance_sp
    module procedure:: distance_dp
end interface
```
<p>위와 같이 선언해 놓으면 두 함수의 인자가 두 개의 <code>point_sp</code>와 두 개의 <code>point_dp</code>로 다르기 때문에 인자의 자료형을 가지고 어떤 함수를 사용해야하는지 판단할 수 있게 됩니다. 만약 두 함수의 인자가 동일하다면 <code>interface</code>문을 사용할 수 없습니다. 아래는 함수 오버로딩을 사용하도록 수정한 예제입니다.</p>
```fortran
module point2d

type point_sp
    real x, y
end type

type point_dp
    real(kind=8):: x,y
end type

interface distance
    module procedure:: distance_sp
    module procedure:: distance_dp
end interface

contains

    real function distance_sp(p1, p2) result(dist)
    type(point_sp), intent(in):: p1, p2
    dist=sqrt((p1%x-p2%x)**2+(p1%y-p2%y)**2)
    end function

    real(kind=8) function distance_dp(p1, p2) result(dist)
    type(point_dp), intent(in):: p1, p2
    dist=dsqrt((p1%x-p2%x)**2+(p1%y-p2%y)**2)
    end function

end module

program test_point2d
use point2d
type(point_sp):: s1,s2
type(point_dp):: d1,d2
real:: dist_s
real(kind=8):: dist_d

s1%x=0.0 ; s1%y=0.0
s2%x=3.0 ; s2%y=4.0

d1%x=0.0d0 ; d1%y=0.0d0
d2%x=3.0d0 ; d2%y=4.0d0

dist_s=distance(s1,s2)
dist_d=distance(d1,d2)

print*, dist_s, dist_d
end program

```
<p>자료형에 상관없이 <code>distance</code>라는 함수를 이용하여 거리를 계산하고 있음을 알 수 있습니다. 물론 위에서 <code>distance_sp</code>와 <code>distance_dp</code>도 사용 가능합니다. 함수 오버로딩을 사용한다고 프로그램의 실행 속도가 빨라지지는 않습니다. 하지만 서브프로그램들의 인터페이스를 단순화하여 프로그래밍을 좀 더 편하게 할 수 있다는 장점이 있습니다.</p>

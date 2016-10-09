---
layout: post
title: 포트란과 연산자 오버로딩
date: 2014-07-13 00:03:12.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- fortran
- oop
---
[함수 오버로딩]({% post_url 2014-07-12-fortran_function_overloading %})과 마찬가지로, <a href="http://ko.wikipedia.org/wiki/연산자_오버로딩">연산자 오버로딩도</a> 객체지향 프로그래밍의 다형성과 관련된 개념입니다. 포트란 90에서 연산자 오버로딩을 사용하는 방법을 살펴보겠습니다. 아래 코드는 이차원 좌표 자료형과 두 개의 점을 더하는 함수 예제입니다.

```fortran
module point2d_op

type point
    real x, y
end type

contains

    type(point) function add(p1, p2) result(p)
    type(point), intent(in):: p1, p2
    p%x=p1%x+p2%x
    p%y=p1%y+p2%y
    end function

end module

program test_point2d_op
use point2d_op
type(point):: p1,p2,p3

p1%x=1.0 ; p1%y=2.0
p2%x=3.0 ; p2%y=4.0

p3=add(p1,p2)

print*, p3%x,p3%y
end program
```

<p>새로운 자료형을 정의했으니 새로운 자료형에 대응하는 더하기 연산도 따로 정의할 필요가 있습니다. 그런데 <code>p3=add(p1,p2)</code>와 같이 쓰는 것보다는 <code>p3=p1+p2</code>로 쓰는 것이 더 직관적이고 이해하기 쉽겠죠. 이 때 사용하는 것이 연산자 오버로딩입니다.</p>
<h1>연산자 오버로딩</h1>
<p>포트란에서는 <code>interface</code>문을 사용하여 이미 존재하는 연산자를 오버로드 하거나 새로운 연산자를 정의할 수 있습니다. 아래 예제는 <code>+</code> 연산자를 오버로드 하는 예제입니다.</p>

```fortran
module point2d_op

type point
    real x, y
end type

interface operator (+)
    module procedure:: add
end interface

contains

    type(point) function add(p1, p2) result(p)
    type(point), intent(in):: p1, p2
    p%x=p1%x+p2%x
    p%y=p1%y+p2%y
    end function

end module

program test_point2d_op
use point2d_op
type(point):: p1,p2,p3

p1%x=1.0 ; p1%y=2.0
p2%x=3.0 ; p2%y=4.0

p3 = p1 + p2

print*, p3%x,p3%y
end program
```

<p>수학 연산자를 오버로딩할 때에는 수학적 정의에 합당하도록 또는 이해하기 쉽도록 정의하는 것이 좋습니다. 위의 <code>add</code> 함수를 <code>-</code> 연산자에 오버로딩하는 것도 가능하나 그렇게 되면 프로그래밍할 때 문제가 발생하겠죠.</p>
<h1>새로운 연산자 정의</h1>
<p>연산자를 오버로드하지 않고 새로 정의할 수도 있습니다. 새로 정의하는 연산자는 <code>.name.</code>과 같이 <code>'.'</code>으로 시작해서 <code>'.'</code>으로 끝나야 합니다. 아래 예제는 <code>add</code> 함수를 <code>.add.</code> 연산자로 정의한 경우입니다. <code>p3=add(p1,p2)</code> 대신 <code>p3=p1.add.p2</code>와 같이 사용한 것을 볼 수 있습니다.</p>
```fortran
module point2d_op

type point
    real x, y
end type

interface operator (.add.)
    module procedure:: add
end interface

contains

    type(point) function add(p1, p2) result(p)
    type(point), intent(in):: p1, p2
    p%x=p1%x+p2%x
    p%y=p1%y+p2%y
    end function

end module

program test_point2d_op
use point2d_op
type(point):: p1,p2,p3

p1%x=1.0 ; p1%y=2.0
p2%x=3.0 ; p2%y=4.0

p3 = p1 .add. p2

print*, p3%x,p3%y
end program
```

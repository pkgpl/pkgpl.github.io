---
layout: post
title: Unit number 자동 할당
date: 2014-07-27 00:56:35.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- fortran
- gpl
- automation
---
<p>포트란에서 파일을 열 때 파일에 번호(Logical unit number)를 할당하고 그 번호를 이용하여 파일 내용을 읽거나 파일에 출력을 하게 됩니다. 리눅스에서 다음 세 번호는 기본적으로 할당이 되어(입출력 스트림이 열려) 있습니다.</p>
```
0: stderr
5: stdin
6: stdout
```
<p>나머지 4바이트 정수 자료형으로 표현할 수 있는 양의 정수값은 사용자가 파일에 할당하여 사용할 수 있습니다 (컴파일러마다 범위는 차이가 있습니다). 보통은 사용하는데 문제가 없지만 하나의 프로그램에서 여러 개의 파일을 열 경우 앞에서 다른 파일에 할당하여 사용중인 번호를 피해 새로운 번호를 찾아야 합니다. 사용중인 번호를 피하기 위해 앞의 코드를 살펴본다든지, 파일 입출력 서브루틴을 위해 새로운 번호를 전달해줄 경우 귀찮다는 생각이 들게 됩니다. 예를 들면 다음과 같은 경우죠.</p>

```fortran
subroutine write_a_number(un, filename, n)
integer,intent(in):: un, n
character(len=*),intent(in):: filename
open(un,file=trim(filename))
write(un,*) n
close(un)
end subroutine
```

이럴 때 inquire함수를 사용하면 특정 번호가 사용중인지 알 수 있고, 따라서 새로운 번호도 자동으로 찾을 수 있습니다. 아래 서브루틴과 함수는 [gpl]({% post_url 2014-07-26-geophysical-prospecting-library %})의 포트란 모듈(module_base)에서 복사하였습니다. 파일 번호는 99번부터 10번까지만 사용하게 만들었습니다. 동시에 그 이상의 파일을 열 일은 없다고 생각하고 만들었는데, 많은 파일을 열어야 할 경우 do loop 범위를 조정하면 되겠습니다.

```fortran
subroutine assign_un(un)
integer, intent(out) :: un
logical :: oflag
integer :: i
do i=99,10,-1
    inquire(unit=i,opened=oflag)
    if(.not.oflag) then
        un=i
        return
    endif
enddo
stop &quot;Error: Logical unit assignment&quot;
end subroutine

logical function un_opened(un) result(val)
integer,intent(in):: un
inquire(unit=un,opened=val)
end function
```

<p>위의 서브루틴을 사용하면 앞에서 살펴본 <code>write_a_number</code> 서브루틴을 다음과 같이 고칠 수 있습니다. 서브루틴의 인터페이스가 좀 더 간단해졌고, 앞으로는 서브루틴을 사용할 때 파일 번호에 대해 고민할 필요가 없겠죠. 자동화의 간단한 예가 되겠습니다.</p>

```fortran
subroutine write_a_number_new(filename, n)
integer,intent(in):: n
character(len=*),intent(in):: filename
integer:: un
call assign_un(un)
open(un,file=trim(filename))
write(un,*) n
close(un)
end subroutine
```

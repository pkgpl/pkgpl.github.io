---
layout: post
date: 2017-02-27
title: Fortran config parser
tags: fortran
---

포트란 언어에서 사용할 수 있는 configuration file parser 모듈을 [github](https://github.com/pkgpl/cfgio)에 공개했습니다.

다음과 같은 configuration 파일에서 변수들을 읽어들일 수 있는 모듈입니다. 사용법은 [github](https://github.com/pkgpl/cfgio)에 올렸습니다.

```ini
[DEFAULTS]
path = ../include
use_abs = True

[Section 1]
nmax = 30
# comment 1
vmin = 1.0
freqs = 5.0, 10.0, 30.0, 50.0
amps = 0.0, 1.0, 1.0, 0.0
path = ../text

[Section 2]
use_abs = no
; comment 2
my file = $(Section 1:path)/file.txt
```
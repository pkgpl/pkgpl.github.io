---
layout: post
title: Geophysical Prospecting Library
date: 2014-07-26 23:58:25.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- gpl
- automation
---
## GPL (Geophysical Prospecting Library)
이 라이브러리는 제가 개인적으로, 대부분 직접 작성하여 사용하는 프로그램들이나 스크립트들을 모아놓은 라이브러리입니다. 연구를 위해 실용적으로 사용하는 잡동사니들의 모음으로, 반복되는 작업들을 자동화하는데 초점을 맞추고 작성한 라이브러리입니다. 내용은 수치해석 프로그래밍을 편리하게 하기 위한 포트란 모듈과 C 함수들, 컴파일을 쉽게 하기 위한 스크립트, 파일 수정 및 부분 추출 등을 위한 프로그램들, 결과 확인 및 논문 그림 그리기를 위한 스크립트들 등이 있습니다. 주로 포트란으로 작성하였고, 그 외에 프로그래밍 연습도 할 겸 C, 파이썬, 루비 등의 언어를 사용하였습니다.
라이브러리 정리 및 간단한 문서화를 위해 블로그를 통해 라이브러리의 기능을 하나 둘씩 공개하려고 합니다. 홈페이지를 방문해주신 누군가에게 도움이 되기를 바랍니다. 코드는 <a href="https://github.com/pkgpl/gpl">GitHub</a>를 통해 공개하겠습니다.

## 설치 방법

### 설치 전에
gpl을 제대로 사용하기 위해서는 Fortran 및 C 컴파일러가 필요하고, Python (2.7)과 Ruby (1.9) 인터프리터가 필요합니다. 모든 gpl 기능을 원활히 사용하기 위해서는 탄성파 자료처리 패키지인 <a href="http://www.cwp.mines.edu/cwpcodes/">Seismic Un*x</a>와 <a href="http://www.ahay.org">Madagascar</a>, Python의 <a href="http://www.numpy.org">Numpy</a> 및 <a href="http://matplotlib.org">Matplotlib</a> 라이브러리, <a href="http://www.scons.org">SConstruct</a> 그리고 <a href="http://www.gnuplot.info">Gnuplot</a>과 <a href="http://www.imagemagick.org">ImageMagick</a>이 필요합니다.

### 설치
1. <a href="https://github.com/pkgpl/gpl">GitHub</a>에서 파일을 받습니다.<br />
2. <code>path_to_gpl/gpl/compiler.py</code>에서 Fortran과 C compiler 관련 설정을 해줍니다.<br />
3. <code>make install</code>을 실행합니다.<br />
4. <code>~/.bash_profile</code> (Mac에서는 <code>~/.profile</code>)에 <code>path_to_gpl/etc/env.sh</code>의 내용을 추가해줍니다.

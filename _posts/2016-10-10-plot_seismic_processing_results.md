---
layout: post
date: 2016-10-09
title: 탄성파 자료처리 그림 그리기
tags:
- seismic
- data processing
- su
- python
- gpl
- automation
- plot
--- 
탄성파 자료처리 결과 그림을 쉽게 그리는 방법을 살펴보겠습니다.

탄성파 자료처리를 하다 보면 결과물을 그림으로 확인해야 하는 경우가 많습니다. 특별히 노력해서 그려야 하는 그림도 있지만 속도모델,
공통송신원모음 등 대부분의 그림은 거의 비슷한 명령으로 그릴 수 있습니다. 개인적으로 논문이나 발표자료에 넣을 그림을 그릴 때 [Seismic
Un*x](http://www.cwp.mines.edu/cwpcodes/)(SU)를 많이 이용하는데, 몇 가지 자주 그리는 그림들을 쉽게 그릴
수 있도록 파이썬 모듈을 만들었습니다. 모듈은 [gpl]({% post_url 2014-07-26-geophysical-prospecting-library %})라이브러리에 포함되어 있습니다. 최근 python 3 용으로 수정하였습니다.

먼저 속도모델을 예로 들어보겠습니다. 그림을 그리기 위한 코드는 다음과 같습니다.
 


{% highlight python %}
from gpl.psplot import plot

vel="marm16km.drt"
opt="n1=188 d1=0.016 d2=0.016 d1num=1 d2num=2"

plot.velocity_color("vel_color.png",vel,opt)
{% endhighlight %}
 
위 코드는 `gpl.psplot` 모듈에서 `plot`을 가져오고, `marm16km.drt` 파일로부터 `opt` 문자열의 옵션을 이용하여
`vel_color.png` 파일을 생성하는데, 컬러로 된 속도모델 그림으로 만들라는 코드입니다.

`velocity_color`는 그림 종류를 지정하는 명령인데, 현재 다음과 같은 명령들을 지원합니다.

- velocity(target, source, option, unit="km/s")
- velocity_color(target, source, option, unit="km/s")
- gradient(target, source, option)
- gradient_color(target, source, option)
- migration(target, source, option)
- contour(target, source, option)
- seismogram(target, source, option)
- spectrum(target, source, option)


위의 명령들은 SU를 이용해 해당 그림을 그리라는 명령으로, `contour`만 `pscontour`를 사용하고 나머지는 `psimage`를
사용합니다. 입력 파일이 SU 파일이라면 `supscontour` 또는 `supsimage`를 사용합니다.

인자들 중 `target`은 출력 파일, `source`는 입력 파일, `option`은 그림 그릴 때 사용할 옵션입니다. 그림 종류에 따라
기본적으로 몇 가지 옵션이 들어가있는데, `n1, d1, d2`와 같이 입력 파일에 따라 달라지는 옵션을 `option`에 넣어주면 됩니다.
그리고 기본 옵션을 덮어쓰고 싶은 경우에도 `option`에 추가해줍니다.

속도모델의 단위는 기본적으로 `km/s`로 지정해 놓았는데, 필요에 따라 바꿔서 사용할 수 있습니다. `g/cc`로 바꾸면 밀도 모델을 그릴
수도 있겠죠. `migration`은 snapshot을 그릴 때 사용할 수도 있습니다.

SU 명령은 기본적으로 eps 파일을 생성합니다. `target`을 eps 외의 다른 파일(png, tiff, jpg 등)로 지정하면
[ImageMagick](http://www.imagemagick.org/)의 `convert` 명령을 이용해 eps 파일을 변환합니다.

따라서 본 모듈의 모든 기능을 이용하려면 [Python](https://www.python.org),
[SU](http://www.cwp.mines.edu/cwpcodes/),
[ImageMagick](http://www.imagemagick.org/)이 필요합니다.

터미널에서 위의 코드를 실행했을 때 나오는 메시지는 다음과 같습니다.

```
psimage height=1.0 width=2.65 d2s=0.5 lwidth=0.1 lstyle="vertright" lheight=1.0
label2="Distance (km)" ghls="0.33,0.5,1" bps=24 whls="0,0.5,1" legend=1
bhls="0.67,0.5,1" labelsize=8 label1="Depth (km)" d1s=0.5  n1=188 d1=0.016
d2=0.016 d1num=1 d2num=2 < marm16km.drt > vel_color.eps

psimage: bclip=5.5 wclip=1.5

// adding velocity unit (km/s)

// fixing bounding box
Original:  %%BoundingBox: 66 41 353 207
Updated:   %%BoundingBox: 85 104 324 202

// converting .eps to .png ..

```

내용을 살펴보면 다음 순서로 실행됩니다.

1. SU의 `psimage` 명령을 이용해 속도모델 eps 파일을 생성합니다. 옵션은 컬러 속도모델에 맞춰서 들어갑니다. 참고로, 그림 크기는
Geophysics 논문 기준에 맞춘 것입니다.
2. `km/s`라는 단위를 넣어줍니다([postscript 수정]({% post_url 2015-01-05-postscript-language-editing %})).
3. 그림 여백을 조절합니다([bounding box 수정]({% post_url 2015-01-05-postscript-bounding-box %})).
4. eps 파일을 png 파일로 수정합니다.

그리고, 결과물인 `vel_color.png`은 다음과 같습니다.
![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-vel_color.png)
(vel_color.png)

아래 코드와 다른 그림 예시를 올리니 필요한 그림에 해당하는 명령을 사용하시면 되겠습니다. 


{% highlight python %}
from gpl.psplot import plot

vel="marm16km.drt"
opt="n1=188 d1=0.016 d2=0.016 d1num=1 d2num=2"

plot.velocity("vel.png",vel,opt+"lbeg=1.5 lend=5.5 lfnum=1.5")
plot.velocity_color("vel_color.png",vel,opt)
plot.velocity_color("density_color.png",vel,opt,unit="g/cc")
plot.gradient("grad.png",vel,opt)
plot.gradient_color("grad_color.png",vel,opt)
plot.migration("mig.png",vel,opt)
plot.contour("contour.png",vel,opt)

seismo="marm3000.su"
opt2="f2=0 d2=0.025 d1s=0.5 d2s=0.5"
plot.seismogram("seismo.png",seismo,opt2)

spec="marm3000fx.su"
plot.spectrum("spec.png",spec,opt2)
{% endhighlight %}
 
![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-vel.png)
(vel.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-vel_color.png)
(vel_color.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-density_color.png)
(density_color.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-grad.png)
(grad.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-grad_color.png)
(grad_color.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-mig.png)
(mig.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-contour.png)
(contour.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-seismo.png)
(seismo.png)

![output]({{site.baseurl}}/images//2016-10-10-plot_seismic_processing_results-spec.png)
(spec.png) 


{% highlight python %}

{% endhighlight %}

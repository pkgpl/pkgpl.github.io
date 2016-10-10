---
layout: post
date: 2016-10-10
title: Matplotlib을 이용한 탄성파 자료처리 그림 그리기
tags: 
- python
- matplotlib
- seismic
- data processing
- plot
--- 
[이전 글]({% post_url 2016-10-10-plot_seismic_processing_results %})에서는 SU 명령어들을
이용해 탄성파 자료처리 결과 확인용 그림을 그리는 방법을 살펴보았습니다. 이번에는 Python의
[Matplotlib](http://matplotlib.org)을 이용하여 그린 그림 예제들을 보겠습니다. 그림은 [IPython
Processing]({% post_url 2015-09-15-ipython-processing %}) 모듈을 이용해 그렸으며, 그릴 때 사용한
코드는 [github](https://github.com/pkgpl/IPythonProcessing/blob/master/pkprocess/pk
plot.py)에서 볼 수 있습니다.

### 속도모델, 구조보정 영상

우선, 다음과 같이 이진파일로부터 2차원 속도모델과 구조보정 결과를 그릴 수 있습니다. 기본적으로 속도모델은 컬러, 구조보정 영상은 흑백으로
그리도록 했지만, 필요에 따라 코드를 수정해서 색상을 바꿀 수 있습니다. 색상을 바꾸고 싶을 경우 [`imshow`](http://matplot
lib.org/api/pyplot_api.html?highlight=imshow#matplotlib.pyplot.imshow) 함수의
[`cmap`](http://scipy-
cookbook.readthedocs.io/items/Matplotlib_Show_colormaps.html) 인자를 이용하면 됩니다. 


<figure class="lineno-container">
{% highlight python linenos %}
%matplotlib inline
from pkprocess import *
import numpy as np
{% endhighlight %}
</figure>


<figure class="lineno-container">
{% highlight python linenos %}
vel=np.fromfile("marm16km.drt",dtype=np.float32)

nx=576
nz=188
h=0.016
vel.shape=(nx,nz)
{% endhighlight %}
</figure>


<figure class="lineno-container">
{% highlight python linenos %}
plot_vel(vel,h)
{% endhighlight %}
</figure>

 
![png]({{site.baseurl}}/images//2016-10-11-plot_seismic_processing_matplotlib-output_4_0.png) 



<figure class="lineno-container">
{% highlight python linenos %}
plot_mig(vel,h)
{% endhighlight %}
</figure>

 
![png]({{site.baseurl}}/images//2016-10-11-plot_seismic_processing_matplotlib-output_5_0.png) 

 
### 공통송신원 모음, 스펙트럼

그리고 SU 파일로부터 공통송신원 모음이나 F-X, F-K 스펙트럼을 그릴 수 있습니다. 공통송신원 모음은 Wiggle trace 또는 이미지로
그릴 수 있고, 이미지 색상은 [`cmap`](http://scipy-
cookbook.readthedocs.io/items/Matplotlib_Show_colormaps.html)으로 조절 가능합니다. 


<figure class="lineno-container">
{% highlight python linenos %}
su=read_su("marm3000.su")
{% endhighlight %}
</figure>


<figure class="lineno-container">
{% highlight python linenos %}
plot_wiggle(su,perc=97)
{% endhighlight %}
</figure>

    min=-616.05078125 max=613.4453125


 
![png]({{site.baseurl}}/images//2016-10-11-plot_seismic_processing_matplotlib-output_8_1.png) 



<figure class="lineno-container">
{% highlight python linenos %}
plot_image(su,perc=97)
{% endhighlight %}
</figure>

    min=-616.05078125 max=613.4453125


 
![png]({{site.baseurl}}/images//2016-10-11-plot_seismic_processing_matplotlib-output_9_1.png) 



<figure class="lineno-container">
{% highlight python linenos %}
plot_image(su,perc=97,cmap='bwr')
{% endhighlight %}
</figure>

    min=-616.05078125 max=613.4453125


 
![png]({{site.baseurl}}/images//2016-10-11-plot_seismic_processing_matplotlib-output_10_1.png) 



<figure class="lineno-container">
{% highlight python linenos %}
specfx(su)
{% endhighlight %}
</figure>

    dt=0.004, fmax=125.0


 
![png]({{site.baseurl}}/images//2016-10-11-plot_seismic_processing_matplotlib-output_11_1.png) 



<figure class="lineno-container">
{% highlight python linenos %}
specfk(su)
{% endhighlight %}
</figure>

    dt=0.004, fmax=125.0
    dx=0.025, kmax=20.0


 
![png]({{site.baseurl}}/images//2016-10-11-plot_seismic_processing_matplotlib-output_12_1.png) 

 
위의 그림들 모두 [Matplotlib](http://matplotlib.org)으로 그렸으므로, 수정이 필요할 경우 [Matplotlib
문서](http://matplotlib.org)를 참고하여 수정해서 사용하시면 되겠습니다. 

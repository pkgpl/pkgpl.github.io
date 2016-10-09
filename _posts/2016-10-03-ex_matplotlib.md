---
title: Matplotlib 연습 문제
author: Wansoo Ha
tags:
- gpl
- Python
- Matplotlib
---

{% highlight python %}
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
{% endhighlight %}
 
# 연습 문제 1: Principal Stress

다음 주응력을 계산하고 $\theta$에 따라 그리세요. ($\theta$는 -90도에서 90도까지 1도 간격으로)

법선응력:

$$\sigma_{nn}=\frac{\sigma_{xx}+\sigma_{yy}}{2}+\frac{\sigma_{xx}-\sigma_{yy}}{2
}\cos 2\theta + \tau_{xy}\sin 2\theta \qquad(1)$$

전단응력:

$$\tau_{ns}=-\frac{\sigma_{xx}-\sigma_{yy}}{2}\sin 2\theta + \tau_{xy}\cos
2\theta \qquad(2)$$

단, $\sigma_{xx}=-5$ MPa, $\sigma_{yy}=-8$ MPa, $\tau_{xy}=-3$ MPa 


{% highlight python %}
def sigma_nn(xx,yy,xy,theta): # equation 1
    return (xx+yy)/2.+(xx-yy)/2.*np.cos(2.*theta)+xy*np.sin(2.*theta)
def tau_ns(xx,yy,xy,theta): # equation 2
    return -(xx-yy)/2.*np.sin(2.*theta)+xy*np.cos(2.*theta)

deg=np.arange(-90,91,1)
theta=np.radians(deg)

sigma_xx=-5.
sigma_yy=-8.
tau_xy=-3.
snn=sigma_nn(sigma_xx,sigma_yy,tau_xy,theta)
tns=tau_ns(sigma_xx,sigma_yy,tau_xy,theta)

plt.figure(figsize=[12,8])
plt.plot(deg,snn,label=r"$\sigma_{nn}$")
plt.plot(deg,tns,label=r"$\tau_{ns}$")
plt.grid()
plt.xlim([-90.,90.])
plt.legend(loc='upper center')
plt.xlabel("Degree")
plt.ylabel("Principal stress (MPa)")
{% endhighlight %}




    <matplotlib.text.Text at 0x116bfb850>



 
![png]({{ site.baseurl }}/images/2016-10-03-ex_matplotlib_3_1.png) 

 
# 연습 문제 2: Fourier Series 1
다음 식에서 Cosine 항을 3개, 10개, 100개 더해서 그래프로 함께 그리세요. (x는 -2부터 2까지 0.01 간격으로 변화하게
만드세요)

$$f\left(x\right)=\frac{1}{2}+\frac{2}{\pi}\left(\cos\frac{\pi}{2}x-\frac{1}{3}\
cos\frac{3\pi}{2}x+\frac{1}{5}\cos\frac{5\pi}{2}x-\cdots\right)$$ 


{% highlight python %}
def fc(x,n):
    s=np.zeros_like(x)
    sgn=-1
    for i in range(n):
        sgn=-sgn
        odd=2*i+1.
        s+=sgn/odd*np.cos(odd*np.pi/2.*x)
    return s*2./np.pi+0.5

x=np.arange(-2.,2.01,0.01)

plt.figure(figsize=[12,8])
plt.plot(x,fc(x,3),label="3 terms")
plt.plot(x,fc(x,10),label="10 terms")
plt.plot(x,fc(x,100),label="100 terms")
plt.grid()
plt.xlim([-2.,2.])
plt.legend(loc="best")
plt.xlabel("x")
plt.ylabel("Amplitude")
{% endhighlight %}




    <matplotlib.text.Text at 0x116bbe2d0>



 
![png]({{ site.baseurl }}/images/2016-10-03-ex_matplotlib_5_1.png) 

 
# 연습 문제 3: Fourier Series 2
다음 식에서 Sine 항을 3개, 10개, 100개 더해서 그래프로 함께 그리세요. (x는 -10부터 10까지 0.1 간격으로 변화하게
만드세요)

$$f\left(x\right)=\pi+2\left(\sin x-\frac{1}{2}\sin 2x+\frac{1}{3}\sin
3x-\cdots\right)$$ 


{% highlight python %}
def fs(x,n):
    s=np.zeros_like(x)
    sgn=-1
    for i in range(n):
        sgn=-sgn
        j=i+1.
        s+=sgn/j*np.sin(j*x)
    return s*2.+np.pi

x=np.arange(-10.,10.1,0.1)

plt.figure(figsize=[12,8])
plt.plot(x,fs(x,3),label="3 terms")
plt.plot(x,fs(x,10),label="10 terms")
plt.plot(x,fs(x,100),label="100 terms")
plt.grid()
plt.xlim([-10.,10.])
plt.legend(loc="best")
plt.xlabel("x")
plt.ylabel("Amplitude")
{% endhighlight %}




    <matplotlib.text.Text at 0x1169c8310>



 
![png]({{ site.baseurl }}/images/2016-10-03-ex_matplotlib_7_1.png) 

 
# 연습 문제 4: 중력 이상
다음의 구에 의한 수직 방향 중력 이상을 계산하고 그리세요. (x는 -1000부터 1000까지 10간격으로 변화)

$$ g_z = \frac{G4\pi R^3 \rho_c}{3} \frac{z}{\left(x^2+z^2\right)^{3/2}} $$

- 중력상수: $G=6.6732 \times 10^{-8} dyne\cdot cm^2/g^2$, ($dyne=g\cdot cm/s^2$)
- 구의 반지름: R=200 m
- 구의 깊이: 500 m, 1000 m (두 경우를 함께 그리세요)
- 밀도차: $\rho_c=0.4 g/cm^3$ 


{% highlight python %}
def gz(R,rho_c,x,z):
    G=6.6732e-8
    return G*4.*np.pi*R**3*rho_c/3.*z/(x**2+z**2)**1.5

R=200.
rho_c=0.4
x=np.arange(-1000,1001,10)

plt.figure(figsize=[12,8])
for z in [500,1000]:
    plt.plot(x,gz(R,rho_c,x,z),label="%s"%z)
plt.grid()
plt.legend()
plt.xlabel("Distance (m)")
plt.ylabel("Gravity anomaly")
{% endhighlight %}




    <matplotlib.text.Text at 0x115026d10>



 
![png]({{ site.baseurl }}/images/2016-10-03-ex_matplotlib_9_1.png) 

 
# 연습 문제 5: Traveltime

수평 2층 구조에서 직접파, 반사파, 선두파의 주시 곡선을 함께 그리세요. (x는 0부터 10000 m까지 10 m 간격으로 변화)

$$ t_{direct}\left(x\right) = \frac{x}{v_1} $$

$$ t_{reflection}\left(x\right) = \frac{1}{v_1}\sqrt{x^2 + \left(2z\right)^2} $$

$$ t_{headwave}\left(x\right) = \frac{x}{v_2}+\frac{2z \cos\theta_c}{v_1} $$

단, $\theta_c = \sin^{-1}\left(\frac{v_1}{v_2}\right)$

- 선두파는 임계거리 이상에서만 존재 (임계거리: $x_c = 2z \tan \theta_c$)
- 반사경계면의 깊이 $z=2000$ m
- 상부층 속도 $v_1 = 2000$ m/s
- 하부층 속도 $v_2 = 4000$ m/s 


{% highlight python %}
def t_direct(x,v1):
    return x/v1

def t_reflection(x,z,v1):
    return np.sqrt(x**2+(2.*z)**2)/v1

def t_headwave(x,z,v1,v2):
    theta_c=np.arcsin(v1/v2)
    return x/v2+2.*z*np.cos(theta_c)/v1

z=2000.
v1=2000.
v2=4000.
theta_c=np.arcsin(v1/v2)
xc=2.*z*np.tan(theta_c)
x=np.arange(0,10001,10.)

plt.figure(figsize=[12,8])
plt.plot(x,t_direct(x,v1),label="Direct")
plt.plot(x,t_reflection(x,z,v1),label="Reflection")
xh=x[x>xc]
plt.plot(xh,t_headwave(xh,z,v1,v2),label="Headwave")
plt.grid()
plt.legend(loc="best")
{% endhighlight %}




    <matplotlib.legend.Legend at 0x1175c9610>



 
![png]({{ site.baseurl }}/images/2016-10-03-ex_matplotlib_11_1.png) 


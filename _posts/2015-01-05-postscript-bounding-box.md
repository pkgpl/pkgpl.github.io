---
layout: post
title: Postscript bounding box
date: 2015-01-05 12:28:24.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- gpl
- postscript
- Python
---
<p>SU(Seismic Un*x)에 있는 psimage로 Marmousi 속도모델을 그리면 다음과 같습니다.(그림 겉부분의 회색은 그림에 포함되어 있지 않은 부분으로, 경계를 표시하기 위해 넣었습니다.)</p>
<p><img class="size-full wp-image-120" title="eps_bbox_before" src="{{ site.baseurl }}/assets/eps_bbox_before.jpg" alt="original eps file" width="431" height="265" /> original eps file</p>
<p>여기서 사용한 명령은 다음과 같습니다.</p>
<pre><code>psimage par='../marm8m.txt' label1="Depth (km)" label2="Offset (km)" labelsize=8 height=1.0 width=2.4 legend=1 lstyle=vertright lwidth=0.1 lheight=1 units="m/s" &lt; ../marm8m.drt &gt; marm.eps</code></pre>
<p>이 때, psimage는 그림 주위로 지나치게 넓은 공간을 만들어 줍니다. Bounding box 정보가 정확하지 않기 때문이죠. 이 상태로는 eps 파일을 다른 그림파일로 변환하여 paper에 넣거나 power point 발표자료에 넣기에 좋지 않습니다(물론 자르기 crop 기능을 이용할 수도 있기는 하죠).</p>
<p>이 공간을 없애기 위해서는 아래 명령을 이용합니다.</p>
<pre><strong><code>gs -sDEVICE=bbox -dNOPAUSE -dBATCH marm.eps</code></strong></pre>
<p>그럼 다음과 같은 결과를 보여줍니다.</p>
<blockquote><p>GPL Ghostscript 8.63 (2008-08-01)<br />
Copyright (C) 2008 Artifex Software, Inc.  All rights reserved.<br />
This software comes with NO WARRANTY: see the file PUBLIC for details.<br />
Loading NimbusSanL-Regu font from /usr/share/fonts/default/Type1/n019003l.pfb... 2656772 1085343 2641408 1357198 2 done.<br />
Loading NimbusSanL-Bold font from /usr/share/fonts/default/Type1/n019004l.pfb... 2673436 1178370 2661504 1363393 2 done.<br />
<strong>%%BoundingBox: 87 107 327 200</strong><br />
%%HiResBoundingBox: 87.695997 107.509005 326.645990 199.601994</p></blockquote>
<p>위의 결과에서 마지막 두 줄에 나온 것이 흰 공간을 없앤 bounding box의 크기입니다. 둘 중 하나를 쓰시면 됩니다. 네 개의 숫자는 각각 왼쪽 아래 x좌표, 왼쪽 아래 y좌표, 오른쪽 위 x좌표, 오른쪽 위 y좌표를 의미합니다. Eps 파일을 텍스트 편집기로 열어서 %%BoundingBox 라고 써진 줄을 찾아 bounding box 크기를 위의 정보로 고쳐주면 아래와 같은 결과를 얻을 수 있습니다.</p>
<p><img class="size-full wp-image-119" title="eps_bbox_after" src="{{ site.baseurl }}/assets/eps_bbox_after.jpg" alt="after fixing bounding box" width="401" height="162" /> after fixing bounding box</p>
<p>또는 SU에 있는 psbbox 라는 프로그램을 이용할 수도 있습니다.</p>
<pre><code>psbbox llx=87 lly=107 urx=327 ury=200 &lt; marm.eps &gt;marmfx.eps</code></pre>
[Gpl]({% post_url 2014-07-26-geophysical-prospecting-library %})에 있는 fixbbox 프로그램은 위의 과정을 자동으로 실행하는 Python 프로그램으로,</p>
<pre><code>fixbbox &lt;input eps file&gt; &lt;output eps file&gt;</code></pre>
<p>과 같이 실행할 수 있습니다.</p>

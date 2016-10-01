---
layout: post
title: Postscript language editing
date: 2015-01-05 12:37:04.000000000 +09:00
type: post
published: true
status: publish
categories: []
tags:
- postscript
---
Postscript로 만들어진 .ps 또는 .eps 파일은 [앞의 글]({% post_url 2015-01-05-postscript-bounding-box %})에서 보셨던 것처럼, 일반적인 text 편집기로 편집할 수 있는 ascii 파일입니다. 파일의 내용은 출력물을 만들어내는 postscript 언어죠. 따라서 postscript 언어를 알면 eps 그림 파일도 마음대로 편집할 수 있습니다. Postscript language를 배우고 싶으신 분은 <a href="http://www.adobe.com/products/postscript/" target="_blank">Adobe site</a>에 가셔서 <a href="http://partners.adobe.com/public/developer/en/ps/sdk/sample/BlueBook.zip">매뉴얼</a>을 받아보시면 됩니다. 여기서는 [앞의 글]({% post_url 2015-01-05-postscript-bounding-box %})에서 만들었던 파일에서 legend unit의 위치를 바꾸는 법만 살펴보도록 하겠습니다. 앞에서 보았던 그림은 다음과 같습니다.
<p><img class="size-full wp-image-119" title="eps_bbox_after" src="{{ site.baseurl }}/assets/eps_bbox_after.jpg" alt="before editing" width="435" height="176" /> before editing</p>
<p>위 그림에서 오른쪽 끝에 있는 "m/s"를 legend(scale bar) 위로 옮겨봅시다. 결과는 다음과 같습니다.(옮긴 후 bounding box도 바꿔줬습니다.)</p>
<p><img class="size-full wp-image-131" title="eps_unit" src="{{ site.baseurl }}/assets/eps_unit.jpg" alt="after editing unit" width="419" height="177" /> after editing unit</p>
<p>위의 결과를 얻기 위해서는 .eps 파일을 열어서 'm/s'라는 문자열을 찾아 지워줍니다. 파일 끝에서 약간 앞에 두 개가 있을겁니다. 그런 후 아래의  코드를 .eps 파일 끝부분의 'showpage' 명령 앞에 넣어줍니다.</p>
<pre><code>%%%%% changed the position of unit
GS
270 190 TR
NP
/Helvetica findfont 8 scalefont setfont
0 0 0 setrgbcolor
21.96 -6.462 M
(m/s) SW exch -0.5 mul
exch -0.5 mul RM (m/s) SH
S
GR
%%%%%</code></pre>
<p>%%%%%는 comment이고, 'm/s'라는 문자열의 위치는 'GS' 아래에 있는 두 개의 숫자(x좌표, y좌표)로 조정합니다. 그림 크기에 따라 위치는 달라집니다.</p>

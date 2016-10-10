{% extends 'markdown.tpl' %}

{%- block header -%}
{%- endblock header -%}

{#
{% block in_prompt %}
**In [{{ cell.execution_count }}]:**
{% endblock in_prompt %}
#}

{% block input %}
<figure class="lineno-container">
{{ '{% highlight python linenos %}' }}
{{ cell.source }}
{{ '{% endhighlight %}' }}
</figure>
{% endblock input %}

{% block data_svg %} 
![svg]({{ output.metadata.filenames['image/svg+xml'] }}) 
{% endblock data_svg %} 

{% block data_png %} 
![png]({{ output.metadata.filenames['image/png'] }}) 
{% endblock data_png %} 

{% block data_jpg %} 
![jpeg]({{ output.metadata.filenames['image/jpeg'] }}) 
{% endblock data_jpg %} 

{% block markdowncell scoped %} 
{{ cell.source | wrap_text(80) }} 
{% endblock markdowncell %} 

{% block headingcell scoped %}
{{ '#' * cell.level }} {{ cell.source | replace('\n', ' ') }}
{% endblock headingcell %}

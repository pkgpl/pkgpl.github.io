# modification of config created here:
# https://gist.github.com/cscorley/9144544
# https://gist.github.com/tgarc/7d6901858ef708030c19
import os

c = get_config()

# modify this function to point your images to a custom path
# by default this saves all images to a directory 'images' in the root of the blog directory
def path2support(path):
    """Turn a file path into a URL"""
    return '{{ site.baseurl }}/images/' + os.path.basename(path)

c.MarkdownExporter.filters = {'path2support': path2support}


import re
import os
import requests

__all__ = ['Tomd', 'convert']

currpath = os.getcwd()
MARKDOWN = {
    'h1': ('\n# ', '\n'),
    'h2': ('\n## ', '\n'),
    'h3': ('\n### ', '\n'),
    'h4': ('\n#### ', '\n'),
    'h5': ('\n##### ', '\n'),
    'h6': ('\n###### ', '\n'),
    'code': ('`', '`'),
    'ul': ('', ''),
    'ol': ('', ''),
    'li': ('- ', ''),
    'blockquote': ('\n> ', '\n'),
    'em': ('**', '**'),
    'strong': ('**', '**'),
    'block_code': ('\n```\n', '\n```\n'),
    'span': ('', ''),
    'p': ('\n', '\n'),
    'p_with_out_class': ('\n', '\n'),
    'inline_p': ('', ''),
    'inline_p_with_out_class': ('', ''),
    'b': ('**', '**'),
    'i': ('*', '*'),
    'del': ('~~', '~~'),
    'hr': ('\n---', '\n\n'),
    'thead': ('\n', '|------\n'),
    'tbody': ('\n', '\n'),
    'td': ('|', ''),
    'th': ('|', ''),
    'tr': ('', '\n'),
    'article_start':('','\n'),
    'article_end':('','\n')
}

BlOCK_ELEMENTS = {
    'h1': '<h1.*?>(.*?)</h1>',
    'h2': '<h2.*?>(.*?)</h2>',
    'h3': '<h3.*?>(.*?)</h3>',
    'h4': '<h4.*?>(.*?)</h4>',
    'h5': '<h5.*?>(.*?)</h5>',
    'h6': '<h6.*?>(.*?)</h6>',
    'hr': '<hr/>',
    'blockquote': '<blockquote.*?>(.*?)</blockquote>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'block_code': '<pre.*?><code.*?>(.*?)</code></pre>',
    'p': '<p\s.*?>(.*?)</p>',
    'p_with_out_class': '<p>(.*?)</p>',
    'thead': '<thead.*?>(.*?)</thead>',
    'tr': '<tr>(.*?)</tr>',
    'article_start':'(<!--article detail-->)',
    'article_end':'(<!--/article detail-->)'
}

INLINE_ELEMENTS = {
    'td': '<td>(.*?)</td>',
    'tr': '<tr>(.*?)</tr>',
    'th': '<th>(.*?)</th>',
    'b': '<b>(.*?)\s+</b>',
    'i': '<i>(.*?)\s+</i>',
    'del': '<del>(.*?)</del>',
    'inline_p': '<p\s.*?>(.*?)</p>',
    'inline_p_with_out_class': '<p>(.*?)</p>',
    'code': '<code.*?>(.*?)</code>',
    'span': '<span.*?>(.*?)</span>',
    'ul': '<ul.*?>(.*?)</ul>',
    'ol': '<ol.*?>(.*?)</ol>',
    'li': '<li.*?>(.*?)</li>',
    #'img': '<img.*?src="(.*?)".*?>(.*?)</img>',
    'img': r'(.*)<img.*?src="(.*?)".*?/>(.*)',
    'a': '<a.*?href="(.*?)".*?>(.*?)</a>',
    'em': '<em.*?>(.*?)\s*</em>',
    'strong': '<strong.*?>(.*?)\s*</strong>',
    'article_start':'(<!--article detail-->)',
    'article_end':'(<!--/article detail-->)'
}

DELETE_ELEMENTS = ['<span.*?>', '</span>', '<div.*?>', '</div>']

def download_image(content,i,title):
    #content = '<img alt="" height="692" src="//nwzimg.wezhan.hk/contents/sitefiles3601/18008104/images/3827319.png" width="703" />'
    pattern = r'(.*)<img.*?src="(.*?)".*?/>(.*)'
    save_image=currpath+r'/images/'+title+'/image_'+str(i)+'.png'
    #new=re.sub(pattern, r'![image_'+str(i)+']({{ site.baseurl }}/assets/images/'+'image_'+str(i)+'.png', content)
    #print(new)
    IMAGE_URL=re.sub(pattern, r'http:\g<2>', content)
    print(IMAGE_URL)
    try:
        r = requests.get(IMAGE_URL,timeout=2)
        f = open(save_image,'wb')
        f.write(r.content) 
        f.close()
        i += 1
    except requests.exceptions.ConnectionError:
        print('image_unavailable') 
    
    return i

class Element:
    def __init__(self, start_pos, end_pos, content, tag, num_of_img, num_of_article, title, is_block=False):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.content = content
        self._elements = []
        self.is_block = is_block
        self.tag = tag
        self.num_of_img = num_of_img
        self.num_of_article = num_of_article
        self.title = title
        self._result = None
        if self.is_block:
            self.parse_inline()

    def __str__(self):
        wrapper = MARKDOWN.get(self.tag)
        self._result = '{}{}{}'.format(wrapper[0], self.content, wrapper[1])
        return self._result

    def parse_inline(self):
        for tag, pattern in INLINE_ELEMENTS.items():
            if tag == 'a':
                self.content = re.sub(pattern, '[\g<2>](\g<1>)', self.content)
            elif tag == 'img':
                #self.content = re.sub(pattern, '![\g<2>](\g<1>)', self.content)
                judge = re.search(pattern,self.content)
                temp = re.sub(pattern, '\g<1>'+r'![image_'+str(self.num_of_img)+']({{ site.baseurl }}/assets/images/'+self.title+'/image_'+str(self.num_of_img)+'.png)'+'\g<3>', self.content)
                if judge :
                    self.num_of_img=download_image(self.content,self.num_of_img,self.title)
                    self.content = temp
            elif self.tag == 'ul' and tag == 'li':
                self.content = re.sub(pattern, '- \g<1>', self.content)
            elif self.tag == 'ol' and tag == 'li':
                self.content = re.sub(pattern, '1. \g<1>', self.content)
            elif self.tag == 'thead' and tag == 'tr':
                self.content = re.sub(pattern, '\g<1>\n', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'th':
                self.content = re.sub(pattern, '|\g<1>', self.content.replace('\n', ''))
            elif self.tag == 'tr' and tag == 'td':
                self.content = re.sub(pattern, '|\g<1>', self.content.replace('\n', ''))
            else:
                wrapper = MARKDOWN.get(tag)
                self.content = re.sub(pattern, '{}\g<1>{}'.format(wrapper[0], wrapper[1]), self.content)



class Tomd:
    def __init__(self, html='', num_of_img = 1, num_of_article = 1 , title = 'article', options=None):
        self.html = html
        self.num_of_img = num_of_img
        self.num_of_article = num_of_article
        self.title = title
        self.options = options
        self._markdown = ''

    def convert(self, html, options=None):
        elements = []
        for tag, pattern in BlOCK_ELEMENTS.items():
            for m in re.finditer(pattern, html, re.I | re.S | re.M):
                element = Element(start_pos=m.start(),
                                  end_pos=m.end(),
                                  content=''.join(m.groups()),
                                  tag=tag,
                                  num_of_img = self.num_of_img,
                                  num_of_article = self.num_of_article,
                                  title = self.title,
                                  is_block=True)
                can_append = True
                for e in elements:
                    if e.start_pos < m.start() and e.end_pos > m.end():
                        can_append = False
                    elif e.start_pos > m.start() and e.end_pos < m.end():
                        elements.remove(e)
                if can_append:
                    elements.append(element)
                    self.num_of_img = element.num_of_img
        elements.sort(key=lambda element: element.start_pos)
    
        self._markdown = ''.join([str(e) for e in elements])

        for index, element in enumerate(DELETE_ELEMENTS):
            self._markdown = re.sub(element, '', self._markdown)
        return self._markdown

    @property
    def markdown(self):
    
    
        self.convert(self.html, self.options)
        return self._markdown


_inst = Tomd()
convert = _inst.convert

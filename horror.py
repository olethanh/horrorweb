import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('horror')
class Tag(object):
    name = 'html'

    def __init__(self, *args, **attr):
        self._children = []
        self.attr = attr
        self.sub = args
        self._dac.append_to_current(self)

    def __enter__(self):
        self._dac.set_current(self)
        logger.debug('enter')

    def __exit__(self, type, value, traceback):
        self._dac.pop_current(self)
        logger.debug('exit')

    @property
    def children(self):
        return ''.join([child.render() for child in self._children])

    def render_attributes(self):
        if not self.attr:
            return ''

        attrlist = [ '%s="%s"' % (k, v)for k,v in self.attr.items()]
        res = ' ' +  ' '.join(attrlist)
        return res

    def render_sub(self):
        return ''.join(self.sub)

    def render(self):
        logger.debug('render element : %s',  self.name)
        return "<%s%s>%s%s</%s>" % (self.name, self.render_attributes(), self.children, self.render_sub(), self.name)

    def __repr__(self):
        logger.debug(self.name)


class T(object):
    def __init__(self):
        self.__roots__ = []
        self.__current__ = None
        self.__previous__ = []

    def set_current(self, tag):
        if self.__current__:
            self.__previous__.append(self.__current__)
        self.__current__ = tag

    def pop_current(self, tag):
        if self.__previous__:
            self.__current__ = self.__previous__.pop()

    def append_to_current(self, tag):
        if self.__current__ :
            self.__current__._children.append(tag)
        else:
            self.__roots__.append(tag)

    def render(self):
        return '\n'.join(root.render() for root in self.__roots__)

    def __getattr__(self, attribute):
        logger.debug('getattr %s %s', attribute, self.__dict__.keys())
        return type(attribute, (Tag,), {'name': attribute, '_dac': self})

t = T()

projects = [
    ('projet1', 'url1'),
    ('projet2', 'url2'),

]
with t.html():
    with t.head():
        t.title('Ma page')
    with t.body():
        t.button('mon button', type='text')
        t.p('My projects')
        with t.ul():
            for title, url in projects:
                with t.li():
                    t.a(title, href=url)

print t.render()


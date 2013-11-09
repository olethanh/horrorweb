import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('horror')

class TagFactoryMeta(type):
    def __getattr__(cls, attribute):
        if attribute in cls.registred_tags:
            logger.debug('GettingExistingElement %s', attribute)
            klass = cls.registred_tags[attribute]
            return klass
        return type('AutoGenerated_'+ attribute, (Tag,), {'name': attribute})

class TagFactory(type):
    __metaclass__ = TagFactoryMeta
    registred_tags = {}

    def __new__(meta, classname, bases, classDict):
        klass = type.__new__(meta, classname, bases, classDict)
        logging.debug('Registred new tag type : %s', classname)
        meta.registred_tags[classname] = klass
        return klass

class Tag(object):
    name = None
    __metaclass__ = TagFactory

    def __init__(self, *args, **attr):
        self._children = []
        self.attr = attr
        self.sub = args
        self._dac.append_to_current(self)

    def __enter__(self):
        self._dac.set_current(self)
        logger.debug('enter' + `self`)

    def __exit__(self, type, value, traceback):
        self._dac.pop_current(self)
        logger.debug('exit' + `self`)

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
        logger.debug('render element : %s',  self.__class__)
        return "<%s%s>%s%s</%s>" % (self.name, self.render_attributes(), self.children, self.render_sub(), self.name)

    def __repr__(self):
        logger.debug(self.name)
        return self.name + ' ' + str(self.__class__)


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
        klass = getattr(TagFactory, attribute)
        klass._dac = self #FIXME : Will probably pose problem with multiple documents, since we modify class attribute
            #Maybe we should return a function so it can get called?
        return klass

class MyLink(TagFactory.a):
    def __init__(self, title, url=None):
        super(MyLink, self).__init__()
        self.sub = (title, )
        url = url if url else title
        self.attr = {'href':url}

class TagWithExtraRender(TagFactory.Tag):
    name = 'span'
    def render(self):
        r = super(TagWithExtraRender, self).render()
        return r + "<br/ >Added Text"


class MyCustomWidget(TagFactory.div):
    def __init__(self, name):
        super(MyCustomWidget, self).__init__()
        with self:
            self.attr['class'] = ' myclass'
            t.h2('My custom widget')
            t.div('Custom Text')
            t.MyLink(name, 'http://google.com')
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
        t.MyLink('http://perdu.com')
        t.MyCustomWidget('Hoho')
        t.h2('My projects')
        t.TagWithExtraRender('hello world')
        with t.ul():
            for title, url in projects:
                with t.li():
                    t.a(title, href=url)

print t.render()


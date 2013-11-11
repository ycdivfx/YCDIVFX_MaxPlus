'''
Created on 07/11/2013

@author: Daniel Santana
'''
import MaxPlus

mxs_eval = MaxPlus.Core.EvalMAXScript


class RenderElement(object):
    '''
    Single Render Element
    We could use the Animatable return by the GetRenderElement, but since we can't pass
    it to MAXScript, let's leave for now as is.
    '''
    _internal_index = -1
    __mxs_get_file = '((maxOps.GetCurRenderElementMgr()).GetRenderElementFilename %i) as string'
    __mxs_set_file = '(maxOps.GetCurRenderElementMgr()).SetRenderElementFilename %i "%s"'
    __mxs_get_element = 'el = (maxOps.GetCurRenderElementMgr()).GetRenderElement %i;'
    __mxs_fn1 = 'dsObjectPropertiesHelper._set_property %s #%s %s;'
    __mxs_fn2 = 'dsObjectPropertiesHelper._get_property %s #%s;'
    __mxs_fn3 = 'dsObjectPropertiesHelper != undefined'
    __mxs_fn4 = 'dsObjectPropertiesHelper._has_property %s #%s;'
    __mxs_fns = '''global dsObjectPropertiesHelper
-- Some parts are based on pen PresetManager for type checking
struct dsObjectPropertiesHelper
(
    fn isCompatable valueClass keyClass=
    (
        case of
        (
            (valueClass==keyClass): true
            (valueClass==float and keyClass==integer): true
            (valueClass==integer and keyClass==float): true
            (valueClass==filename and keyClass==string): true
            (valueClass==string and keyClass==filename): true
            default: false
        )
    ),
    fn _set_property obj k value =
    (
        local classString=((classOf obj) as string)
        if not hasProperty obj k do return False
        local keyClass=(classOf value)
        local valueClass=(classOf (getProperty obj k))
        if isCompatable valueClass keyClass then
            setProperty obj k value
        else
            format "Warning: Values are not compatable for \\"%\\"\\n\\tProperty \\"%\\" needs value class of % got %\\n" classString k valueClass keyClass
    ),
    fn _get_property obj k =
    (
        if not hasProperty obj k do return False
        r = getProperty obj k
        c = classof r
        if c == filename do return r as string
        if r == undefined do r = ""
        r
    ),
    fn _has_property obj k =
    (
        hasProperty obj k
    )
)
dsObjectPropertiesHelper = dsObjectPropertiesHelper()
True'''

    def __init__(self, n=-1, className=None):
        self._internal_index = n

    def __init_mxs_(self):
        if not mxs_eval(self.__mxs_fn3).Get():
            mxs_eval(self.__mxs_fns)

    def __getattr__(self, name):
        if name in ['_internal_index']:
            raise AttributeError
        if name == 'File':
            return self._get_filename()
        self.__init_mxs_()
        mx_element = self.__mxs_get_element % self._internal_index
        mx_script = mx_element + (self.__mxs_fn4 % ('el', name))
        if mxs_eval(mx_script).Get():
            mx_script = mx_element + (self.__mxs_fn2 % ('el', name))
            return mxs_eval(mx_script).Get()
        else:
            print "Element does't contain '%s'" % name
            raise AttributeError

    def __setattr__(self, name, value):
        if name in ['_internal_index']:
            object.__setattr__(self, name, value)
            return
        if name == 'File':
            self._set_filename(name)
            return
        self.__init_mxs_()
        mx_element = self.__mxs_get_element % self._internal_index
        mx_script = mx_element + (self.__mxs_fn4 % ('el', name))
        if mxs_eval(mx_script).Get():
            mx_script = mx_element + (self.__mxs_fn1 % ('el', name, value))
            mxs_eval(mx_script)
        else:
            print "Couldn't seet element property '%s' with value %s" % (name, value)
            raise AttributeError

    def _set_filename(self, name):
        mxs_eval(self.__mxs_set_file % (self._internal_index, name))

    def _get_filename(self):
        return mxs_eval(self.__mxs_get_file % self._internal_index).Get()


class RenderElementManager(object):
    '''
    Missing RenderElementManager class
    '''

    __mxs_re_count = '(maxOps.GetCurRenderElementMgr()).NumRenderElements()'
    __mxs_re_del = '(maxOps.GetCurRenderElementMgr()).RemoveAllElements()'
    __mxs_re_add = '''elm = %s()
    (maxOps.GetCurRenderElementMgr()).AddRenderElement elm'''
    __mxs_re_g_active = '(maxOps.GetCurRenderElementMgr()).GetElementsActive()'
    __mxs_re_s_active = '(maxOps.GetCurRenderElementMgr()).SetElementsActive %s'
    __mxs_re_g_display = '(maxOps.GetCurRenderElementMgr()).GetDisplayElements()'
    __mxs_re_s_display = '(maxOps.GetCurRenderElementMgr()).SetDisplayElements %s'

    def __init__(self):
        pass

    def __build_element(self, i):
        return RenderElement(i)

    def AddElement(self, className):
        '''
        Adds a new render element using the class name and
        returns it.
        @param className: Name of the element to add (MAXScript class name)
        @type className: str
        @return: Element
        @rtype: RenderElement
        '''
        if mxs_eval(self.__mxs_re_add % className).Get():
            return self.__build_element(len(self))
        return None

    #def RemoveElement(self, className):
    #    pass

    def RemoveAllElements(self):
        return mxs_eval(self.__mxs_re_del)

    def GetElements(self):
        return [self.__build_element(i) for i in xrange(len(self))]

    def __getitem__(self, i):
        return self.__build_element(i)

    def __len__(self):
        return mxs_eval(self.__mxs_re_count).Get()

    @property
    def Active(self):
        return mxs_eval(self.__mxs_re_g_active).Get()

    @Active.setter
    def Active(self, value):
        mxs_eval(self.__mxs_re_s_active % value)

    @property
    def Display(self):
        return mxs_eval(self.__mxs_re_g_display).Get()

    @Display.setter
    def Display(self, value):
        mxs_eval(self.__mxs_re_s_display % value)

    Elements = property(lambda self: (self[i] for i in xrange(len(self))))

# Adding a new class to MaxPlus
MaxPlus.RenderElementManager = RenderElementManager

if __name__ == '__main__':
    re = RenderElementManager()
    print 'Number of render elements %s' % len(re)
    for element in re.Elements:
        # NOTE: Please change this, since i was testing with VRay elements
        print 'Element %s is %s' % (element.ElementName, 'enabled' if element.VrayVFB else 'disabled')
        element.VrayVFB = False
        print 'Element %s is now %s' % (element.ElementName, 'enabled' if element.VrayVFB else 'disabled')
        print 'Filename=', element.File

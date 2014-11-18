


"""This class holds all the necessary properties required to perform docking. The reason for theis class is that instead of passing differenet parameter for different methods to Docking class we just pass this list of parameters and then reterive what we want."""

class MetaDockParams(type):
    _glideLigAdd = None
    _glideRecAdd = None
    _glidegridZipAdds = None

    def _get_glideLigAdd(self):
        return self._glideLigAdd

    def _set_glideLigAdd(self, value):
        #raise AttributeError("class 'Foo' attribute 'ro' is not writable!")
	self._glideLigAdd = value

    def _get_glideRecAdd(self):
        return self._glideRecAdd

    def _set_glideRecAdd(self, value):
        #raise AttributeError("class 'Foo' attribute 'ro' is not writable!")
	self._glideRecAdd = value

    def _get_glidegridZipAdds(self):
        return self._glidegridZipAdds

    def _set_glidegridZipAdds(self, value):
        self._glidegridZipAdds = value


    glideLigAdd = property(_get_glideLigAdd, _set_glideLigAdd)
    glideRecAdd = property(_get_glideRecAdd, _set_glideRecAdd)
    glidegridZipAdds = property(_get_glidegridZipAdds, _set_glidegridZipAdds)


class DockParams(object):
    __metaclass__=MetaDockParams

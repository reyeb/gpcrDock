


"""This class holds all the necessary properties required to perform docking. The reason for theis class is that instead of passing differenet parameter for different methods to Docking class we just pass this list of parameters and then reterive what we want."""

class MetaDockParams(type):

#######Glide Parameters
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

#######Gold Parameters [it can be merge with Glide in future !!!! if so remove this bit]
    _GoldLigAdd = None
    _GoldRecAdd = None
    _GoldgridZipAdds = None

    def _get_GoldLigAdd(self):
        return self._GoldLigAdd

    def _set_GoldLigAdd(self, value):
        #raise AttributeError("class 'Foo' attribute 'ro' is not writable!")
	self._GoldLigAdd = value

    def _get_GoldRecAdd(self):
        return self._GoldRecAdd

    def _set_GoldRecAdd(self, value):
        #raise AttributeError("class 'Foo' attribute 'ro' is not writable!")
	self._GoldRecAdd = value

    def _get_GoldgridZipAdds(self):
        return self._GoldgridZipAdds

    def _set_GoldgridZipAdds(self, value):
        self._GoldgridZipAdds = value


    GoldLigAdd = property(_get_GoldLigAdd, _set_GoldLigAdd)
    GoldRecAdd = property(_get_GoldRecAdd, _set_GoldRecAdd)
    GoldgridZipAdds = property(_get_GoldgridZipAdds, _set_GoldgridZipAdds)

#######Vina Parameters 
    _VinaLigAdd = None
    _VinaRecAdd = None
    _VinagridZipAdds = None

    def _get_VinaLigAdd(self):
        return self._VinaLigAdd

    def _set_VinaLigAdd(self, value):
        #raise AttributeError("class 'Foo' attribute 'ro' is not writable!")
	self._VinaLigAdd = value

    def _get_VinaRecAdd(self):
        return self._VinaRecAdd

    def _set_VinaRecAdd(self, value):
        #raise AttributeError("class 'Foo' attribute 'ro' is not writable!")
	self._VinaRecAdd = value

    def _get_VinagridZipAdds(self):
        return self._VinagridZipAdds

    def _set_VinagridZipAdds(self, value):
        self._VinagridZipAdds = value


    VinaLigAdd = property(_get_VinaLigAdd, _set_VinaLigAdd)
    VinaRecAdd = property(_get_VinaRecAdd, _set_VinaRecAdd)
    VinagridZipAdds = property(_get_VinagridZipAdds, _set_VinagridZipAdds)
class DockParams(object):
    __metaclass__=MetaDockParams

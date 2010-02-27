"""
The main DebugToolbar class that loads and renders the Toolbar.
"""
from django.template.loader import render_to_string
from debug_toolbar.config import config

class DebugToolbar(object):

    def __init__(self, request):
        self.request = request
        self.panels = []
        self.config = config
        self.template_context = {
            'BASE_URL': self.config.get_base_url(self.request), # for backwards compatibility
            'DEBUG_TOOLBAR_MEDIA_URL': self.config.get_media_url(self.request),
        }

        self.load_panels()

    def load_panels(self):
        """
        Populate debug panels
        """
        from django.core import exceptions

        for panel_path in self.default_panels:
            try:
                dot = panel_path.rindex('.')
            except ValueError:
                raise exceptions.ImproperlyConfigured, '%s isn\'t a debug panel module' % panel_path
            panel_module, panel_classname = panel_path[:dot], panel_path[dot+1:]
            try:
                mod = __import__(panel_module, {}, {}, [''])
            except ImportError, e:
                raise exceptions.ImproperlyConfigured, 'Error importing debug panel %s: "%s"' % (panel_module, e)
            try:
                panel_class = getattr(mod, panel_classname)
            except AttributeError:
                raise exceptions.ImproperlyConfigured, 'Toolbar Panel module "%s" does not define a "%s" class' % (panel_module, panel_classname)

            try:
                panel_instance = panel_class(context=self.template_context)
            except:
                raise # Bubble up problem loading panel

            self.panels.append(panel_instance)

    def render_toolbar(self):
        """
        Renders the overall Toolbar with panels inside.
        """
        context = self.template_context.copy()
        context.update({ 'panels': self.panels, })

        return render_to_string('debug_toolbar/base.html', context)
    
    def get_default_panels(self):
        return self.config['DEFAULT_PANELS']
    
    def set_default_panels(self, new_panels):
        self.config['DEFAULT_PANELS'] = new_panels
    
    ## for backwards compatibility
    default_panels = property(fget = get_default_panels, fset = set_default_panels)
    
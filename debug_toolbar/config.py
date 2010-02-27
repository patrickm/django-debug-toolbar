from django.conf import settings

class DebugToolbarConfig(dict):
    def __init__(self, settings):
        super(DebugToolbarConfig, self).__init__()
        self['INTERCEPT_REDIRECTS'] = True
        self['SHOW_TOOLBAR_CALLBACK'] = None
        self['EXTRA_SIGNALS'] = []
        self['HIDE_DJANGO_SQL'] = True
        self['SQL_WARNING_THRESHOLD'] = 500
        self['SHOW_TEMPLATE_CONTEXT'] = True
        self['MEDIA_ROOT'] = None
        self['MEDIA_URL_PREFIX'] = None
        self['ALLOWED_HTML_TYPES'] = ['text/html', 'application/xhtml+xml']
        self['TAG'] = u'body'
        self['DEFAULT_PANELS'] = [
            'debug_toolbar.panels.version.VersionDebugPanel',
            'debug_toolbar.panels.timer.TimerDebugPanel',
            'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
            'debug_toolbar.panels.headers.HeaderDebugPanel',
            'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
            'debug_toolbar.panels.sql.SQLDebugPanel',
            'debug_toolbar.panels.template.TemplateDebugPanel',
            #'debug_toolbar.panels.cache.CacheDebugPanel',
            'debug_toolbar.panels.signals.SignalDebugPanel',
            'debug_toolbar.panels.logger.LoggingPanel',
        ]

        dtconfig = getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {})
        self.update(dtconfig)
        
        dtpanels = getattr(settings, 'DEBUG_TOOLBAR_PANELS', False)
        if dtpanels:
            self['DEFAULT_PANELS'] = dtpanels
        
        ## for backwards compatibility
        debug_toolbar_media_root = getattr(settings, 'DEBUG_TOOLBAR_MEDIA_ROOT', None)
        if debug_toolbar_media_root:
            self['MEDIA_ROOT'] = debug_toolbar_media_root
    
    def get(self, k, d = None):
        val = super(DebugToolbarConfig, self).get(k)
        if val is None:
            return d
        return val

    def get_media_url(self, request):
        return u'%s/__debug__/m/' % self.get_base_url(request)
    
    def get_base_url(self, request):
        return request.META.get('SCRIPT_NAME', '') or self.get('MEDIA_URL_PREFIX', '')

config = DebugToolbarConfig(settings)

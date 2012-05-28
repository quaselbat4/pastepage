from tastypie import fields
from django.conf import settings
from tastypie.serializers import Serializer
from django.core.urlresolvers import reverse
from tastypie.resources import ModelResource
from django.conf.urls.defaults import url
from archive.models import Site, Update, Screenshot
# Diff throttle depending on env
if settings.PRODUCTION:
    from tastypie.throttle import CacheThrottle as Throttle
else:
    from tastypie.throttle import BaseThrottle as Throttle


class ScreenshotResource(ModelResource):
    update = fields.ToOneField('api.resources.UpdateResource', 'update')
    site = fields.ToOneField('api.resources.SiteResource', 'site')
    
    class Meta:
        resource_name = 'screenshots'
        queryset = Screenshot.objects.filter(site__status='active').select_related("update")
        excludes = ['has_html', 'html_archived', 'html_raw']
        allowed_methods = ['get',]
        throttle = Throttle(throttle_at=50)
        serializer = Serializer(formats=['json', 'jsonp'],
            content_types = {
                'json': 'text/javascript',
                'jsonp': 'text/javascript'
        })
        include_absolute_url = True


class SiteResource(ModelResource):
    
    class Meta:
        resource_name = 'sites'
        queryset = Site.objects.active()
        allowed_methods = ['get',]
        throttle = Throttle(throttle_at=50)
        serializer = Serializer(formats=['json', 'jsonp'],
            content_types = {
                'json': 'text/javascript',
                'jsonp': 'text/javascript'
        })
        include_absolute_url = True
        filtering = {
            "slug": ('exact',),
        }


class UpdateResource(ModelResource):
    screenshots = fields.ToManyField('api.resources.ScreenshotResource', 'screenshot_set')
    
    class Meta:
        resource_name = 'updates'
        queryset = Update.objects.all()
        allowed_methods = ['get',]
        throttle = Throttle(throttle_at=50)
        serializer = Serializer(formats=['json', 'jsonp'],
            content_types = {
                'json': 'text/javascript',
                'jsonp': 'text/javascript'
        })
        include_absolute_url = True

















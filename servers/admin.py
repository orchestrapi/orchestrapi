from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Server

class ServerAdmin(admin.ModelAdmin):
    
    list_display = ['name', '_daemon_url', 'hearthbeat']

    def _daemon_url(self, obj):
        return mark_safe(f'<a target="_new" href="{obj.get_daemon_url}">{obj.get_daemon_url}</a>')

    def hearthbeat(self, obj):
        script = """
            const url = '%s/'
            fetch(url, {mode: 'no-cors'})
                .then(function(response){
                    let elem = document.getElementById('server%s');
                    if(response.ok) {
                        elem.style.color = 'green';
                        elem.innerHTML = 'Ok';
                    }else {
                        elem.style.color = 'red';
                        elem.innerHTML = 'Not Running';
                    }
                });
        """ % (obj.get_daemon_url, obj.id)
        print(script)
        return mark_safe(f'<p id="server{obj.id}">Heathbeat</p><script>{script}</script>')


admin.site.register(Server, ServerAdmin)
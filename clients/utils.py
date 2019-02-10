
from files.models import ConfigFile
import re

def clean_volume(volumen, app):
    match = re.search(r'\$\{.*\}', volumen)
    if match:
        match = match.group(0)
        slug = match[2:-1]
        try:
            config_file = ConfigFile.objects.get(slug=slug, app=app)
            return volumen.replace(match, config_file.file.path)
        except Exception as e:
            raise e
    else:
        return volumen
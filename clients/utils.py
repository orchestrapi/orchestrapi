from files.models import ConfigFile
import re

def get_match_and_slug(text, pattern):
    match = re.search(pattern, volumen)
    if match:
        return match.group(0), match[2:-1]
    return None, None

def clean_volume(volumen, instance):
    match, slug = get_match_and_slug(volumen, r'\$\{.*\}')
    if not match:
        return volumen
    try:
        from apps.models import App
        if isinstance(instance, App):
            config_file = ConfigFile.objects.get(slug=slug, app=instance)
        else:
            config_file = ConfigFile.objects.get(slug=slug, service=instance)

        return volumen.replace(match, config_file.file.path)
    except Exception as e:
        raise e

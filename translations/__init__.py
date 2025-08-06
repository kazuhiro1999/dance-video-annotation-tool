from .ja import translations as ja
from .en import translations as en

all_translations = {
    "ja": ja,
    "en": en
}

def localize_config(config, lang):
    def localize(obj):
        if isinstance(obj, dict):
            if 'ja' in obj and 'en' in obj:
                return obj.get(lang, obj.get('ja'))
            return {k: localize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [localize(item) for item in obj]
        else:
            return obj
    return localize(config)
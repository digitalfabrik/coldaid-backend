from django import template

register = template.Library()


@register.filter
def request_translation_title(request, language):
    all_request_translations = request.translations
    request_translation = all_request_translations.filter(language__code=language.code)
    if request_translation.exists():
        return request_translation.first().title
    if all_request_translations.exists():
        request_translation = all_request_translations.first()
        return '{title} ({language})'.format(
            title=request_translation.title,
            language=request_translation.language
        )
    return ''


@register.filter
def request_translation_creator(request, language):
    all_request_translations = request.translations
    request_translation = all_request_translations.filter(language__code=language.code)
    if request_translation.exists():
        return request_translation.first().creator
    if all_request_translations.exists():
        request_translation = all_request_translations.first()
        return '{creator} ({language})'.format(
            creator=request_translation.creator,
            language=request_translation.language
        )
    return ''


@register.filter
def request_translation_last_updated(request, language):
    all_request_translations = request.translations
    request_translation = all_request_translations.filter(language__code=language.code)
    if request_translation.exists():
        return request_translation.first().last_updated
    if all_request_translations.exists():
        return all_request_translations.first().last_updated
    return ''


@register.filter
def request_translation_created_date(request, language):
    all_request_translations = request.translations
    request_translation = all_request_translations.filter(language__code=language.code)
    if request_translation.exists():
        return request_translation.first().created_date
    if all_request_translations.exists():
        return all_request_translations.first().created_date
    return ''

# -*- coding: utf-8 -*-
""" Python API for language and translation management. """

from collections import namedtuple

from django.conf import settings
from django.utils.translation import ugettext as _

from openedx.core.djangoapps.dark_lang.models import DarkLangConfig
from openedx.core.djangoapps.site_configuration.helpers import get_value


# Named tuples can be referenced using object-like variable
# deferencing, making the use of tuples more readable by
# eliminating the need to see the context of the tuple packing.
Language = namedtuple('Language', 'code name')


def header_language_selector_is_enabled():
    """Return true if the header language selector has been enabled via settings or site-specific configuration."""
    setting = get_value('SHOW_HEADER_LANGUAGE_SELECTOR', settings.FEATURES.get('SHOW_HEADER_LANGUAGE_SELECTOR', False))

    # The SHOW_LANGUAGE_SELECTOR setting is deprecated, but might still be in use on some installations.
    deprecated_setting = get_value('SHOW_LANGUAGE_SELECTOR', settings.FEATURES.get('SHOW_LANGUAGE_SELECTOR', False))

    return setting or deprecated_setting


def footer_language_selector_is_enabled():
    """Return true if the footer language selector has been enabled via settings or site-specific configuration."""
    return get_value('SHOW_FOOTER_LANGUAGE_SELECTOR', settings.FEATURES.get('SHOW_FOOTER_LANGUAGE_SELECTOR', False))


def released_languages():
    """Retrieve the list of released languages.

    Constructs a list of Language tuples by intersecting the
    list of valid language tuples with the list of released
    language codes.

    Returns:
       list of Language: Languages in which full translations are available.

    Example:

        >>> print released_languages()
        [Language(code='en', name=u'English'), Language(code='fr', name=u'Français')]

    """
    released_language_codes = DarkLangConfig.current().released_languages_list
    default_language_code = settings.LANGUAGE_CODE

    if default_language_code not in released_language_codes:
        released_language_codes.append(default_language_code)
        released_language_codes.sort()

    # Intersect the list of valid language tuples with the list
    # of released language codes
    return [
        Language(language_info[0], language_info[1])
        for language_info in settings.LANGUAGES
        if language_info[0] in released_language_codes
    ]


def all_languages():
    """Retrieve the list of all languages, translated and sorted.

    Returns:
        list of (language code (str), language name (str)): the language names
        are translated in the current activated language and the results sorted
        alphabetically.

    """
    languages = [(lang[0], _(lang[1])) for lang in settings.ALL_LANGUAGES]  # pylint: disable=translation-of-non-string
    return sorted(languages, key=lambda lang: lang[1])

from ..langid import AppStreamLang, PoLang
from . import bcp47


def convert(lang: PoLang) -> AppStreamLang:
    """
    Convert a PO file language to a BCP 47 language tag.

    The tag is composed and validated by :func:`metaglot.langmap.bcp47.convert`
    on behalf of :class:`AppStreamLang`.

    :param lang: The PO file language.
    :return: The BCP 47 language tag for the language.
    :raises ValueError: If the composed tag is not a valid BCP 47 tag.
    """
    return bcp47.convert(lang, AppStreamLang)

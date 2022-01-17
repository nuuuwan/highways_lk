import xml.dom.minidom as minidom
import xml.etree.ElementTree as ElementTree

FONT_FAMILY = 'Futura'
DEFAULT_ATTRIB_MAP = {
    'html': {
        'style': 'font-family: %s;' % FONT_FAMILY,
    },
    'svg': {
        'xmlns': 'http://www.w3.org/2000/svg',
    },
    'text': {
        'font-family': FONT_FAMILY,
        'text-anchor': 'middle',
        'fill': '#000000',
        'stroke': 'none',
    },
    'text-gray': {
        'font-family': FONT_FAMILY,
        'text-anchor': 'middle',
        'fill': '#c0c0c0',
        'stroke': 'none',
    },
}


def _(tag, child_element_list_or_other=None, attrib_custom={}):
    """XML Element."""
    tag_real = tag.split('-')[0]
    child_element_list_or_other = child_element_list_or_other or []

    attrib = DEFAULT_ATTRIB_MAP.get(tag, {})
    attrib.update(attrib_custom)
    attrib = dict(
        zip(
            list(map(lambda key: key.replace('_', '-'), attrib.keys())),
            list(map(str, attrib.values())),
        )
    )

    element = ElementTree.Element(tag_real)
    element.attrib = attrib

    if isinstance(child_element_list_or_other, list):
        for child_element in child_element_list_or_other:
            element.append(child_element)
    else:
        element.text = str(child_element_list_or_other)
    return element


def render_xml(element):
    """Render XML Element."""
    s = ElementTree.tostring(element, encoding='utf-8').decode()
    parsed_s = minidom.parseString(s)
    return parsed_s.toprettyxml(indent='  ')

#
# Copyright (c), 2018-2020, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
import re
from typing import cast, Tuple, Union

from elementpath.aliases import NamespacesType, NsmapType

# Regex patterns related to names and namespaces
NAMESPACE_URI_PATTERN = re.compile(r'{([^}]+)}')
EXPANDED_NAME_PATTERN = re.compile(
    r'^(?:{(?P<namespace>[^}]+)})?'
    r'(?P<local>[^\d\W][\w\-.\u00B7\u0300-\u036F\u0387\u06DD\u06DE\u203F\u2040]*)$',
)

# Namespaces
XML_NAMESPACE = "http://www.w3.org/XML/1998/namespace"
XMLNS_NAMESPACE = "http://www.w3.org/2000/xmlns/"  # Used in DOM for xmlns declarations
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"
XSI_NAMESPACE = "http://www.w3.org/2001/XMLSchema-instance"
XLINK_NAMESPACE = "http://www.w3.org/1999/xlink"

# XPath/XQuery namespaces
XPATH_FUNCTIONS_NAMESPACE = "http://www.w3.org/2005/xpath-functions"
XQT_ERRORS_NAMESPACE = "http://www.w3.org/2005/xqt-errors"
XPATH_MATH_FUNCTIONS_NAMESPACE = "http://www.w3.org/2005/xpath-functions/math"
XPATH_MAP_FUNCTIONS_NAMESPACE = "http://www.w3.org/2005/xpath-functions/map"
XPATH_ARRAY_FUNCTIONS_NAMESPACE = "http://www.w3.org/2005/xpath-functions/array"
XSLT_XQUERY_SERIALIZATION_NAMESPACE = "http://www.w3.org/2010/xslt-xquery-serialization"

# XML namespace attributes
XML_BASE = '{%s}base' % XML_NAMESPACE
XML_LANG = '{%s}lang' % XML_NAMESPACE
XML_SPACE = '{%s}space' % XML_NAMESPACE
XML_ID = '{%s}id' % XML_NAMESPACE

# XML Schema Instance namespace attributes
XSI_TYPE = '{%s}type' % XSI_NAMESPACE
XSI_NIL = '{%s}nil' % XSI_NAMESPACE
XSI_SCHEMA_LOCATION = '{%s}schemaLocation' % XSI_NAMESPACE
XSI_NONS_SCHEMA_LOCATION = '{%s}schemaLocation' % XSI_NAMESPACE

# XML Schema tags (schema and types)
XSD_SCHEMA = '{%s}schema' % XSD_NAMESPACE
XSD_ANY_TYPE = '{%s}anyType' % XSD_NAMESPACE
XSD_ANY_SIMPLE_TYPE = '{%s}anySimpleType' % XSD_NAMESPACE
XSD_ANY_ATOMIC_TYPE = '{%s}anyAtomicType' % XSD_NAMESPACE
XSD_NOTATION = '{%s}NOTATION' % XSD_NAMESPACE
XSD_ID = '{%s}ID' % XSD_NAMESPACE
XSD_IDREF = '{%s}IDREF' % XSD_NAMESPACE
XSD_IDREFS = '{%s}IDREFS' % XSD_NAMESPACE

XSD_STRING = '{%s}string' % XSD_NAMESPACE
XSD_FLOAT = '{%s}float' % XSD_NAMESPACE
XSD_DOUBLE = '{%s}double' % XSD_NAMESPACE
XSD_DECIMAL = '{%s}decimal' % XSD_NAMESPACE

# XPath type labels defined in XSD namespace that are not XSD builtin types
XSD_UNTYPED = '{%s}untyped' % XSD_NAMESPACE
XSD_UNTYPED_ATOMIC = '{%s}untypedAtomic' % XSD_NAMESPACE
XSD_ERROR = '{%s}error' % XSD_NAMESPACE
XSD_NUMERIC = '{%s}numeric' % XSD_NAMESPACE


def get_namespace(name: str) -> str:
    try:
        return NAMESPACE_URI_PATTERN.match(name).group(1)  # type: ignore[union-attr]
    except AttributeError:
        return ''


def split_expanded_name(name: str) -> Tuple[str, str]:
    match = EXPANDED_NAME_PATTERN.match(name)
    if match is None:
        raise ValueError(f"{name!r} is not an expanded QName")
    namespace, local_name = match.groups()
    return namespace or '', local_name


def get_prefixed_name(name: str, namespaces: Union[NamespacesType, NsmapType]) -> str:
    """
    Get the prefixed form of a QName, using a namespace map.

    :param name: an extended QName or a local name or a prefixed QName.
    :param namespaces: a dictionary with a map from prefixes to namespace URIs.
    """
    try:
        if not name.startswith(('{', 'Q{')):
            return name
        elif name[0] == '{':
            ns_uri, local_name = name[1:].split('}')
        else:
            ns_uri, local_name = name[2:].split('}')
    except (ValueError, TypeError):
        raise ValueError(f"{name!r} is not a QName")

    for prefix, uri in sorted(namespaces.items(), reverse=True,
                              key=lambda x: x if x[0] is not None else ('', x[1])):
        if uri == ns_uri:
            return f'{prefix}:{local_name}' if prefix else local_name
    else:
        if ns_uri == XML_NAMESPACE:
            return f'xml:{local_name}'
        return name


def get_expanded_name(name: str, namespaces: Union[NamespacesType, NsmapType]) -> str:
    """
    Get the expanded form of a QName, using a namespace map.
    Local names are mapped to the default namespace.

    :param name: a prefixed QName or a local name or an extended QName.
    :param namespaces: a dictionary with a map from prefixes to namespace URIs.
    :return: the expanded format of a QName or a local name.
    """
    if not name or name.startswith('{'):
        return name
    elif name.startswith('Q{'):
        return name[1:]

    try:
        prefix, local_name = name.split(':')
    except ValueError:
        if ':' in name:
            raise ValueError(f"wrong format for prefixed QName {name!r}")
        elif '' in namespaces:
            uri = namespaces['']
        elif None in namespaces:
            uri = cast(NsmapType, namespaces)[None]  # lxml nsmap
        else:
            return name

        return f'{{{uri}}}{name}' if uri else name
    else:
        if not prefix or not local_name:
            raise ValueError(f"wrong format for reference name {name!r}")
        elif prefix == 'xml':
            return f'{{{XML_NAMESPACE}}}{local_name}'

        uri = namespaces[prefix]
        if not uri:
            raise ValueError(f"prefix {prefix!r} is mapped to an empty URI")
        return f'{{{uri}}}{local_name}'

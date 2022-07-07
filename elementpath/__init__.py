#
# Copyright (c), 2018-2022, SISSA (International School for Advanced Studies).
# All rights reserved.
# This file is distributed under the terms of the MIT License.
# See the file 'LICENSE' in the root directory of the present
# distribution, or http://opensource.org/licenses/MIT.
#
# @author Davide Brunato <brunato@sissa.it>
#
__version__ = '3.0.0b2'
__author__ = "Davide Brunato"
__contact__ = "brunato@sissa.it"
__copyright__ = "Copyright 2018-2022, SISSA"
__license__ = "MIT"
__status__ = "Production/Stable"


from . import datatypes
from . import protocols  # only for type annotations
from . import tdop

# Expose only exceptions that are not derived from builtins or from other libraries
from .exceptions import ElementPathError, MissingContextError, ElementPathParseError

from .xpath_context import XPathContext, XPathSchemaContext
from .xpath_nodes import XPathNode, DocumentNode, ElementNode, AttributeNode, \
    NamespaceNode,  CommentNode, ProcessingInstructionNode, TextNode, SchemaNode
from .tree_builders import get_node_tree, build_node_tree, build_lxml_node_tree, \
    build_schema_node_tree
from .xpath_token import XPathToken, XPathFunction
from .xpath1 import XPath1Parser
from .xpath2 import XPath2Parser
from .xpath_selectors import select, iter_select, Selector
from .schema_proxy import AbstractSchemaProxy
from .regex import RegexError, translate_pattern

TypedElement = ElementNode  # for backward compatibility with xmlschema<=1.10.0

__all__ = ['datatypes', 'protocols', 'tdop',
           'ElementPathError', 'MissingContextError', 'ElementPathParseError',
           'XPathContext', 'XPathSchemaContext',
           'XPathNode', 'DocumentNode', 'ElementNode', 'AttributeNode',
           'NamespaceNode', 'CommentNode', 'ProcessingInstructionNode',
           'TextNode', 'SchemaNode', 'TypedElement', 'get_node_tree',
           'build_node_tree', 'build_lxml_node_tree', 'build_schema_node_tree',
           'XPathToken', 'XPathFunction', 'XPath1Parser', 'XPath2Parser',
           'select', 'iter_select', 'Selector', 'AbstractSchemaProxy',
           'RegexError', 'translate_pattern']

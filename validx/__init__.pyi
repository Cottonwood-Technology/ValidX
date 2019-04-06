import typing as t
from . import py, cy

__impl__: str
__version__: str
__author__: str
__license__: str

Validator: t.Union[t.Type[py.Validator], t.Type[cy.Validator]]
Int: t.Union[t.Type[py.Int], t.Type[cy.Int]]
Float: t.Union[t.Type[py.Float], t.Type[cy.Float]]
Str: t.Union[t.Type[py.Str], t.Type[cy.Str]]
Bytes: t.Union[t.Type[py.Bytes], t.Type[cy.Bytes]]
Date: t.Union[t.Type[py.Date], t.Type[cy.Date]]
Time: t.Union[t.Type[py.Time], t.Type[cy.Time]]
Datetime: t.Union[t.Type[py.Datetime], t.Type[cy.Datetime]]
Bool: t.Union[t.Type[py.Bool], t.Type[cy.Bool]]
List: t.Union[t.Type[py.List], t.Type[cy.List]]
Tuple: t.Union[t.Type[py.Tuple], t.Type[cy.Tuple]]
Dict: t.Union[t.Type[py.Dict], t.Type[cy.Dict]]
AllOf: t.Union[t.Type[py.AllOf], t.Type[cy.AllOf]]
OneOf: t.Union[t.Type[py.OneOf], t.Type[cy.OneOf]]
LazyRef: t.Union[t.Type[py.LazyRef], t.Type[cy.LazyRef]]
Type: t.Union[t.Type[py.Type], t.Type[cy.Type]]
Const: t.Union[t.Type[py.Const], t.Type[cy.Const]]
Any: t.Union[t.Type[py.Any], t.Type[cy.Any]]

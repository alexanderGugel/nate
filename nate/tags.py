from abc import abstractmethod
from dataclasses import dataclass
from html import escape
from typing import Dict, Generator, Union, Iterable


class BaseTag:
    """
    In HTML5 there are six different kinds of elements: void elements, the
    template element, raw text elements, escapable raw text elements, foreign
    elements, and normal elements. Tags are used to delimit the start and end
    of elements in the markup.
    To simplify the serialization code we _only_ distinguish between tags that
    need an end tag and those that don't.
    See https://html.spec.whatwg.org/multipage/syntax.html#elements-2.
    """

    @abstractmethod
    def _to_html(self) -> Generator[str, None, None]:
        pass

    def to_html(self) -> str:
        return "".join(self._to_html())


Class = Union[str, Iterable[str]]
Attr = Dict[str, Union[str, None]]


@dataclass
class SelfClosingTag(BaseTag):
    """
    The start and end tags of certain normal elements can be omitted. Those
    that cannot be omitted must not be omitted. Void elements only have a start
    tag; end tags must not be specified for void elements. Foreign elements
    must either have a start tag and an end tag, or a start tag that is marked
    as self-closing, in which case they must not have an end tag.
    This class implements the serialization of tags that do _not_ have an end
    tag ("self-closing"). As such, SelfClosingTag instances do _not_ have
    children.
    See https://html.spec.whatwg.org/multipage/syntax.html#elements-2.
    """

    tag: str
    attr: Attr
    class_: Class

    def _to_html(self) -> Generator[str, None, None]:
        yield "<"
        yield self.tag
        yield from class_to_html(self.class_)
        yield from attr_to_html(self.attr)
        yield "/>"


Children = Union[
    BaseTag,
    str,
    Iterable[Union[BaseTag, str]],
]


@dataclass
class FullTag(BaseTag):
    """
    Raw text, escapable raw text, and normal elements have a start tag to
    indicate where they begin, and an end tag to indicate where they end.
    This class implements the serialization of tags that require an end tag.
    FullTags are allowed to have children. During serialization, those child
    tags are serialized in a recursive fashion. Raw text is not represented
    using a separate tag, but can be listed as a child.
    See https://html.spec.whatwg.org/multipage/syntax.html#elements-2.
    """

    tag: str
    children: Children
    class_: Class
    attr: Attr

    def _to_html(self) -> Generator[str, None, None]:
        yield "<"
        yield self.tag
        yield from class_to_html(self.class_)
        yield from attr_to_html(self.attr)
        yield ">"
        yield from children_to_html(self.children)
        yield "</"
        yield self.tag
        yield ">"


@dataclass
class FullTagWithPrefix(FullTag):
    """
    Supports adding a custom prefix to a full tag. This is useful for the html
    element, which typically has to be prefixed with a corresponding doctype.
    """

    prefix: str

    def _to_html(self) -> Generator[str, None, None]:
        yield self.prefix
        yield from super()._to_html()


@dataclass
class DangerousHtml(BaseTag):
    """
    By default, all strings are escaped to prevent cross-site scripting (XSS)
    attacks. DangerousHtml can be used to inject unescaped HTML. This should be
    used sparingly. It is useful as an escape hatch.
    """

    html: str

    def _to_html(self) -> Generator[str, None, None]:
        yield self.html


@dataclass
class Fragment(BaseTag):
    """
    Tags accept lists of children. Sometimes it is desirable to serialize those
    children without wrapping the resulting HTML into start and end tags.
    """

    children: Children

    def _to_html(self) -> Generator[str, None, None]:
        yield from children_to_html(self.children)


def children_to_html(children: Children) -> Generator[str, None, None]:
    if isinstance(children, BaseTag):
        yield from children.to_html()
    elif isinstance(children, str):
        yield escape(children)
    elif isinstance(children, Iterable):
        for child in children:
            if isinstance(child, BaseTag):
                yield from child.to_html()
            elif isinstance(child, str):
                yield escape(child)


def class_to_html(class_: Class) -> Generator[str, None, None]:
    """
    Helper function used for serializing a list of class names to a
    corresponding HTML attribute. Technically this could be avoided by
    converting the class names to attributes prior to constructing the node,
    but this would incur additional overhead as we'd then have to reconstruct
    the attribute (and thus go over it twice). Given how common this use case
    is, it has been special cased.
    """

    final = class_ if isinstance(class_, str) else " ".join(class_)
    if final == "":
        return
    yield ' class="'
    yield final
    yield '"'


def attr_to_html(attr: Attr) -> Generator[str, None, None]:
    """
    Attributes for an element are expressed inside the element's start tag.
    Attributes can be specified in four different ways:
    1. Empty attribute syntax
    2. Unquoted attribute value syntax
    3. Single-quoted attribute value syntax
    4. Double-quoted attribute value syntax
    Only 1. and 4. are supported. Empty attributes can be expressed by using
    the None value.
    See https://html.spec.whatwg.org/multipage/syntax.html#attributes-2.
    """

    if len(attr) == 0:
        return
    for k in attr:
        yield " "
        yield k
        v = attr[k]
        if isinstance(v, str):
            yield '="'
            yield escape(v, quote=True)
            yield '"'


# The following functions might seem a bit verbose, but is easier to type.
# Currently Python does not support typing higher-order function that return
# Callables with optional arguments.

# Void elements
# See https://html.spec.whatwg.org/multipage/syntax.html#elements-2.


def Area(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="area", class_=class_, attr=attr)


def Base(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="base", class_=class_, attr=attr)


def Br(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="br", class_=class_, attr=attr)


def Col(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="col", class_=class_, attr=attr)


def Embed(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="embed", class_=class_, attr=attr)


def Hr(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="hr", class_=class_, attr=attr)


def Img(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="img", class_=class_, attr=attr)


def Input(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="input", class_=class_, attr=attr)


def Link(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="link", class_=class_, attr=attr)


def Meta(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="meta", class_=class_, attr=attr)


def Param(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="param", class_=class_, attr=attr)


def Source(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="source", class_=class_, attr=attr)


def Track(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="track", class_=class_, attr=attr)


def Wbr(class_: Class = [], **attr: Union[str, None]) -> SelfClosingTag:
    return SelfClosingTag(tag="wbr", class_=class_, attr=attr)


# All other elements
# The spec maintained by WHATWG misses an exhaustive list of all permissible
# elements. Thus we're referring to W3C in this case.
# See https://www.w3.org/TR/2011/WD-html-markup-20110113/elements.html.


def A(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="a", children=children, class_=class_, attr=attr)


def Abbr(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="abbr", children=children, class_=class_, attr=attr)


def Address(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="address", children=children, class_=class_, attr=attr)


def Article(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="article", children=children, class_=class_, attr=attr)


def Aside(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="aside", children=children, class_=class_, attr=attr)


def Audio(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="audio", children=children, class_=class_, attr=attr)


def B(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="b", children=children, class_=class_, attr=attr)


def Bdi(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="bdi", children=children, class_=class_, attr=attr)


def Bdo(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="bdo", children=children, class_=class_, attr=attr)


def Blockquote(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(
        tag="blockquote",
        children=children,
        class_=class_,
        attr=attr,
    )


def Body(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="body", children=children, class_=class_, attr=attr)


def Button(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="button", children=children, class_=class_, attr=attr)


def Canvas(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="canvas", children=children, class_=class_, attr=attr)


def Caption(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="caption", children=children, class_=class_, attr=attr)


def Cite(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="cite", children=children, class_=class_, attr=attr)


def Code(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="code", children=children, class_=class_, attr=attr)


def Colgroup(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="colgroup", children=children, class_=class_, attr=attr)


def Command(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="command", children=children, class_=class_, attr=attr)


def Datalist(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="datalist", children=children, class_=class_, attr=attr)


def Dd(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="dd", children=children, class_=class_, attr=attr)


def Del(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="del", children=children, class_=class_, attr=attr)


def Details(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="details", children=children, class_=class_, attr=attr)


def Dfn(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="dfn", children=children, class_=class_, attr=attr)


def Div(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="div", children=children, class_=class_, attr=attr)


def Dl(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="dl", children=children, class_=class_, attr=attr)


def Dt(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="dt", children=children, class_=class_, attr=attr)


def Em(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="em", children=children, class_=class_, attr=attr)


def Fieldset(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="fieldset", children=children, class_=class_, attr=attr)


def Figcaption(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(
        tag="figcaption",
        children=children,
        class_=class_,
        attr=attr,
    )


def Figure(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="figure", children=children, class_=class_, attr=attr)


def Footer(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="footer", children=children, class_=class_, attr=attr)


def Form(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="form", children=children, class_=class_, attr=attr)


def H1(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="h1", children=children, class_=class_, attr=attr)


def H2(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="h2", children=children, class_=class_, attr=attr)


def H3(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="h3", children=children, class_=class_, attr=attr)


def H4(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="h4", children=children, class_=class_, attr=attr)


def H5(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="h5", children=children, class_=class_, attr=attr)


def H6(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="h6", children=children, class_=class_, attr=attr)


def Head(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="head", children=children, class_=class_, attr=attr)


def Header(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="header", children=children, class_=class_, attr=attr)


def Hgroup(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="hgroup", children=children, class_=class_, attr=attr)


def Html(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTagWithPrefix(
        prefix="<!DOCTYPE html>",
        tag="html",
        children=children,
        class_=class_,
        attr=attr,
    )


def I(  # noqa: E741, E743
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="i", children=children, class_=class_, attr=attr)


def Iframe(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="iframe", children=children, class_=class_, attr=attr)


def Ins(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="ins", children=children, class_=class_, attr=attr)


def Kbd(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="kbd", children=children, class_=class_, attr=attr)


def Keygen(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="keygen", children=children, class_=class_, attr=attr)


def Label(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="label", children=children, class_=class_, attr=attr)


def Legend(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="legend", children=children, class_=class_, attr=attr)


def Li(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="li", children=children, class_=class_, attr=attr)


def Map(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="map", children=children, class_=class_, attr=attr)


def Mark(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="mark", children=children, class_=class_, attr=attr)


def Menu(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="menu", children=children, class_=class_, attr=attr)


def Meter(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="meter", children=children, class_=class_, attr=attr)


def Nav(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="nav", children=children, class_=class_, attr=attr)


def Noscript(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="noscript", children=children, class_=class_, attr=attr)


def Object(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="object", children=children, class_=class_, attr=attr)


def Ol(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="ol", children=children, class_=class_, attr=attr)


def Optgroup(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="optgroup", children=children, class_=class_, attr=attr)


def Option(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="option", children=children, class_=class_, attr=attr)


def Output(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="output", children=children, class_=class_, attr=attr)


def P(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="p", children=children, class_=class_, attr=attr)


def Pre(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="pre", children=children, class_=class_, attr=attr)


def Progress(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="progress", children=children, class_=class_, attr=attr)


def Q(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="q", children=children, class_=class_, attr=attr)


def Rp(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="rp", children=children, class_=class_, attr=attr)


def Rt(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="rt", children=children, class_=class_, attr=attr)


def Ruby(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="ruby", children=children, class_=class_, attr=attr)


def S(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="s", children=children, class_=class_, attr=attr)


def Samp(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="samp", children=children, class_=class_, attr=attr)


def Script(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="script", children=children, class_=class_, attr=attr)


def Section(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="section", children=children, class_=class_, attr=attr)


def Select(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="select", children=children, class_=class_, attr=attr)


def Small(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="small", children=children, class_=class_, attr=attr)


def Span(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="span", children=children, class_=class_, attr=attr)


def Strong(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="strong", children=children, class_=class_, attr=attr)


def Style(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="style", children=children, class_=class_, attr=attr)


def Sub(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="sub", children=children, class_=class_, attr=attr)


def Summary(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="summary", children=children, class_=class_, attr=attr)


def Sup(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="sup", children=children, class_=class_, attr=attr)


def Table(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="table", children=children, class_=class_, attr=attr)


def Tbody(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="tbody", children=children, class_=class_, attr=attr)


def Td(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="td", children=children, class_=class_, attr=attr)


def Textarea(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="textarea", children=children, class_=class_, attr=attr)


def Tfoot(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="tfoot", children=children, class_=class_, attr=attr)


def Th(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="th", children=children, class_=class_, attr=attr)


def Thead(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="thead", children=children, class_=class_, attr=attr)


def Time(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="time", children=children, class_=class_, attr=attr)


def Title(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="title", children=children, class_=class_, attr=attr)


def Tr(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="tr", children=children, class_=class_, attr=attr)


def Ul(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="ul", children=children, class_=class_, attr=attr)


def Var(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="var", children=children, class_=class_, attr=attr)


def Video(
    children: Children = [],
    class_: Class = [],
    **attr: Union[str, None],
) -> FullTag:
    return FullTag(tag="video", children=children, class_=class_, attr=attr)

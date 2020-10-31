![Library](https://github.com/alexanderGugel/nate/raw/master/assets/alfons-morales-YLSwjSy7stw-unsplash.jpg)

# nate

[![PyPI](https://img.shields.io/pypi/v/nate)](https://pypi.org/project/nate/) [![PyPI - License](https://img.shields.io/pypi/l/nate)](https://pypi.org/project/nate/) [![Build Status](https://travis-ci.com/alexanderGugel/nate.svg?branch=master)](https://travis-ci.com/alexanderGugel/nate)

**nate** makes generating HTML fun. Rather than forcing you to adopt an entirely different templating language that comes with its own set of quirks, nate is built around a simple, but powerful Python DSL that enables you to easily compose trees of elements that can be translated to well-formed HTML - no more forgotten angle brackets, unbalanced tags, or unescaped user input.

Think of nate as an alternative to [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) or [Django templates](https://docs.djangoproject.com/en/3.1/ref/templates/language/).

## Features

- **Mostly typed** - The API has been designed with type safety in mind: All
  function boundaries have type hints to ensure correctness, ease
  documentation, and make auto-completion in the IDE of your choice a piece of
  cake.
- **No dependencies** - nate does not depend on any third-party libraries.
- **Stable API** - The API itself is stable. No breaking changes are planned.
- **Tiny** - The core library is approximately 500 eLOC, which is tiny and
  can be manually audited on a single afternoon.

## Install

With [pip](https://pip.pypa.io/en/stable/installing/) installed, run

```
$ pip install nate
```

## Usage

Import the elements you need.

```python
from nate import Table, Thead, Th, Tr, Tbody, Td
```

Construct your tree.

```python
politicians = [
    {"first_name": "Theodor", "last_name": "Heuss", "party": "FDP"},
    {"first_name": "Heinrich", "last_name": "Lübke", "party": "CDU"},
    {"first_name": "Gustav", "last_name": "Heinemann", "party": "SPD"},
    # ...
]

table = Table(
    [
        Thead(Th([Tr("First Name"), Tr("Last Name"), Tr("Party")])),
        Tbody(map(
            lambda politician: Tr(
                [
                    Td(politician["first_name"]),
                    Td(politician["last_name"]),
                    Td(politician["party"]),
                ]
            ),
            politicians,
        )),
    ]
)
```

Call `.to_html()` on your root node to serialize your tree to a string of HTML.

```python
table.to_html()  #=> <table><thead>....
```

Raw text nodes are escaped by default, thus making it difficult to introduce [XSS vulnerabilities](https://en.wikipedia.org/wiki/Cross-site_scripting).

```python
p = P("<script>alert('XSS');</script>")
p.to_html()  #=> <p>&lt;script&gt;alert(&#x27;XSS&#x27;);&lt;/script&gt;</p>
```

### Components

Templating languages tend to come with their own abstractions for building re-usable components. There is no need for those in nate, given that component hierarchies can easily be composed using plain Python functions.

```python
from nate import Div, H1, P, BaseTag


def MyComponent(title: str, description: str) -> BaseTag:
    return Div(
        children=[
            H1(title),
            P(description),
        ],
        class_="my-component",
    )

component = MyComponent(
    title="My title",
    description="My description",
)

component.to_html()  #=> <div class="my-component>...
```

### Examples

<table>
<thead>
<tr>
<th>
nate
</th>
<th>
HTML
</th>
</tr>
</thead>
<tbody>
<tr>
<td>

```python
Title("Hello World!").to_html()
```

</td>
<td>

```html
<title>Hello World!</title>
```

</td>
</tr>
<tr>
<td>

```python
steaks = ["Rib Eye", "New York Strip", "Porterhouse"]
Ul(map(lambda steak: Li(steak), steaks)).to_html()
```

</td>
<td>

```html
<ul>
  <li>Rib Eye</li>
  <li>New York Strip</li>
  <li>Porterhouse</li>
</ul>
```

</td>
</tr>
<tr>
<td>

```python
Html(
    lang="en",
    children=[
        Head(
            children=[
                Meta(charset="utf-8"),
                Title(children="Welcome to nate!"),
            ]
        ),
        Body(
            children=[
                H1("Mission"),
                P(
                    "nate is not a template engine.",
                    class_="red",
                ),
            ],
        ),
    ],
).to_html()
```

</td>
<td>


```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8"/>
        <title>Welcome to nate!</title>
    </head>
    <body>
        <h1>Mission</h1>
        <p class="red">nate is not a template engine.</p>
    </body>
</html>
```

</td>
</tr>
</tbody>
</table>

## How to contribute

- Keep it simple, don't do anything too crazy. Even folks that don't know Python should be able to understand the code without any issues.
- Design APIs with type-safety in mind.
- If your code slows things down, it won't get merged.
- Avoid introducing new dependencies.
- If you don't want to follow those rules, forking is _encouraged_!
- Ensure new code is covered by corresponding tests.

## Prior works of art

- [lamernews](https://github.com/antirez/lamernews) - While written in Ruby, the [`page.rb`](https://github.com/antirez/lamernews/blob/master/page.rb) library inspired this project.
- [hyperscript](https://github.com/hyperhype/hyperscript) - Pure JavaScript alternative to JSX.
- [hyperpython](https://github.com/ejplatform/hyperpython) - Python interpretation of hyperscript.
- [XHPy](https://pypi.org/project/xhpy/) - Extends Python syntax such that XML document fragments become valid Python expressions. Based off XHP, a similar framework for PHP.

## License

MIT

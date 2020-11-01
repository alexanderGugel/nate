import unittest

from nate import (
    H1,
    Body,
    Br,
    DangerousHtml,
    Div,
    Head,
    Hr,
    Html,
    Input,
    Meta,
    P,
    Title,
    Table,
    Thead,
    Tbody,
    Th,
    Tr,
    Td,
)

from .common import article_1, article_2, html, section


class TagsTest(unittest.TestCase):
    def test_basic(self) -> None:
        basic = Html(
            lang="en",
            children=[
                Head(
                    children=[
                        Meta(charset="utf-8"),
                        Meta(
                            name="viewport",
                            content="width=device-width, initial-scale=1",
                        ),
                        Title(children="Basic"),
                    ]
                ),
                Body(
                    children=[
                        H1("Hello world"),
                        P(
                            children=[
                                "First line",
                                Br(),
                                "Second line",
                            ]
                        ),
                        Hr(),
                        P("The end."),
                    ],
                ),
            ],
        )
        basic_expected = """<!DOCTYPE html>\
<html lang="en">\
<head>\
<meta charset="utf-8"/>\
<meta name="viewport" content="width=device-width, initial-scale=1"/>\
<title>Basic</title>\
</head>\
<body>\
<h1>Hello world</h1>\
<p>First line<br/>Second line</p><hr/>\
<p>The end.</p>\
</body>\
</html>\
"""
        self.assertEqual(basic.to_html(), basic_expected)

    def test_iterables(self) -> None:
        politicians = [
            {"first_name": "Theodor", "last_name": "Heuss", "party": "FDP"},
            {"first_name": "Heinrich", "last_name": "Lübke", "party": "CDU"},
            {"first_name": "Gustav", "last_name": "Heinemann", "party": "SPD"},
            {"first_name": "Walter", "last_name": "Scheel", "party": "FDP"},
            {"first_name": "Karl", "last_name": "Carstens", "party": "CDU"},
            {
                "first_name": "Richard",
                "last_name": "von Weizsäcker",
                "party": "CDU",
            },
            {"first_name": "Roman", "last_name": "Herzog", "party": "CDU"},
            {"first_name": "Johannes", "last_name": "Rau", "party": "SPD"},
        ]
        table = Table(
            [
                Thead(Th([Tr("First Name"), Tr("Last Name"), Tr("Party")])),
                Tbody(
                    map(
                        lambda politician: Tr(
                            [
                                Td(politician["first_name"]),
                                Td(politician["last_name"]),
                                Td(politician["party"]),
                            ]
                        ),
                        politicians,
                    ),
                ),
            ]
        )
        table_expected = """<table>\
<thead><th><tr>First Name</tr><tr>Last Name</tr><tr>Party</tr></th></thead>\
<tbody>\
<tr><td>Theodor</td><td>Heuss</td><td>FDP</td></tr>\
<tr><td>Heinrich</td><td>Lübke</td><td>CDU</td></tr>\
<tr><td>Gustav</td><td>Heinemann</td><td>SPD</td></tr>\
<tr><td>Walter</td><td>Scheel</td><td>FDP</td></tr>\
<tr><td>Karl</td><td>Carstens</td><td>CDU</td></tr>\
<tr><td>Richard</td><td>von Weizsäcker</td><td>CDU</td></tr>\
<tr><td>Roman</td><td>Herzog</td><td>CDU</td></tr>\
<tr><td>Johannes</td><td>Rau</td><td>SPD</td></tr>\
</tbody>\
</table>\
"""
        self.assertEqual(table.to_html(), table_expected)

        p = P("Test", class_=iter(["bg-red", "blue"]))
        p_expected = '<p class="bg-red blue">Test</p>'
        self.assertEqual(p.to_html(), p_expected)

    def test_xss(self) -> None:
        p = P("<script>alert('XSS');</script>")
        p_expected =\
            "<p>&lt;script&gt;alert(&#x27;XSS&#x27;);&lt;/script&gt;</p>"
        self.assertEqual(p.to_html(), p_expected)

        div = Div([DangerousHtml("<script>alert('XSS');</script>")])
        div_expected = "<div><script>alert('XSS');</script></div>"
        self.assertEqual(div.to_html(), div_expected)

        text_input = Input(value="<script>alert('XSS');</script>")
        text_input_expected =\
            '<input value="&lt;script&gt;alert(&#x27;XSS&#x27;);&lt;/\
script&gt;"/>'
        self.assertEqual(text_input.to_html(), text_input_expected)

    def test_article(self) -> None:
        article_1_expected = """\
<article class="pv4 bt bb b--black-10 ph3 ph0-l">\
<div class="flex flex-column flex-row-ns">\
<div class="w-100 w-60-ns pr3-ns order-2 order-1-ns">\
<h1 class="f3 athelas mt0 lh-title">\
Tech Giant Invests Huge Money to Build a Computer Out of Science Fiction</h1>\
<p class="f5 f4-l lh-copy athelas">\
The tech giant says it is ready to begin planning a quantum computer, a \
powerful cpu machine that relies on subatomic particles instead of \
transistors.\
</p>\
</div>\
<div class="pl3-ns order-1 order-2-ns mb4 mb0-ns w-100 w-40-ns">\
<img class="db" src="https://mrmrs.github.io/photos/cpu.jpg" alt="Photo of a \
dimly lit room with a computer interface terminal."/>\
</div>\
</div>\
<p class="f6 lh-copy gray mv0">By <span class="ttu">Robin Darnell</span></p>\
<time class="f6 db gray">Nov. 21, 2016</time>\
</article>"""

        article_2_expected = """<article class="pv4 bt bb b--black-10 ph3 ph0-l">\
<div class="flex flex-column flex-row-ns">\
<div class="w-100 w-60-ns pr3-ns order-2 order-1-ns">\
<h1 class="f3 athelas mt0 lh-title">\
A whale takes up residence in a large body of water\
</h1>\
<p class="f5 f4-l lh-copy athelas">\
This giant of a whale says it is ready to begin planning a new swim later \
this afternoon. A powerful mammal that relies on fish and plankton instead of \
hamburgers.\
</p>\
</div>\
<div class="pl3-ns order-1 order-2-ns mb4 mb0-ns w-100 w-40-ns">\
<img class="db" src="http://mrmrs.github.io/photos/whale.jpg" alt="Photo of a \
whale&#x27;s tale coming crashing out of the water."/>\
</div>\
</div>\
<p class="f6 lh-copy gray mv0">By <span class="ttu">Katherine Grant</span></p>\
<time class="f6 db gray">Nov. 19, 2016</time>\
</article>"""
        self.assertEqual(article_1.to_html(), article_1_expected)
        self.assertEqual(article_2.to_html(), article_2_expected)

    def test_section(self) -> None:
        expected = """<section class="mw7 center">\
<h2 class="athelas ph3 ph0-l">News</h2>\
<article class="pv4 bt bb b--black-10 ph3 ph0-l">\
<div class="flex flex-column flex-row-ns">\
<div class="w-100 w-60-ns pr3-ns order-2 order-1-ns">\
<h1 class="f3 athelas mt0 lh-title">\
Tech Giant Invests Huge Money to Build a Computer Out of Science Fiction</h1>\
<p class="f5 f4-l lh-copy athelas">\
The tech giant says it is ready to begin planning a quantum computer, a \
powerful cpu machine that relies on subatomic particles instead of \
transistors.\
</p>\
</div>\
<div class="pl3-ns order-1 order-2-ns mb4 mb0-ns w-100 w-40-ns">\
<img class="db" src="https://mrmrs.github.io/photos/cpu.jpg" alt="Photo of a \
dimly lit room with a computer interface terminal."/>\
</div>\
</div>\
<p class="f6 lh-copy gray mv0">By <span class="ttu">Robin Darnell</span></p>\
<time class="f6 db gray">Nov. 21, 2016</time>\
</article>\
<article class="pv4 bt bb b--black-10 ph3 ph0-l">\
<div class="flex flex-column flex-row-ns">\
<div class="w-100 w-60-ns pr3-ns order-2 order-1-ns">\
<h1 class="f3 athelas mt0 lh-title">\
A whale takes up residence in a large body of water\
</h1>\
<p class="f5 f4-l lh-copy athelas">\
This giant of a whale says it is ready to begin planning a new swim later \
this afternoon. A powerful mammal that relies on fish and plankton instead of \
hamburgers.\
</p>\
</div>\
<div class="pl3-ns order-1 order-2-ns mb4 mb0-ns w-100 w-40-ns">\
<img class="db" src="http://mrmrs.github.io/photos/whale.jpg" alt="Photo of a \
whale&#x27;s tale coming crashing out of the water."/>\
</div>\
</div>\
<p class="f6 lh-copy gray mv0">By <span class="ttu">Katherine Grant</span></p>\
<time class="f6 db gray">Nov. 19, 2016</time>\
</article>\
</section>"""
        self.assertEqual(section.to_html(), expected)

    def test_html(self) -> None:
        actual = html.to_html()
        expected = """<!DOCTYPE html>\
<html lang="en">\
<head>\
<meta charset="utf-8"/>\
<meta name="viewport" content="width=device-width, initial-scale=1"/>\
<title>Example Title</title>\
<link rel="stylesheet" href="https://unpkg.com/tachyons@4.12.0/css/tachyons.\
min.css"/>\
</head>\
<body class="sans-serif">\
<section class="mw7 center">\
<h2 class="athelas ph3 ph0-l">News</h2>\
<article class="pv4 bt bb b--black-10 ph3 ph0-l">\
<div class="flex flex-column flex-row-ns">\
<div class="w-100 w-60-ns pr3-ns order-2 order-1-ns">\
<h1 class="f3 athelas mt0 lh-title">\
Tech Giant Invests Huge Money to Build a Computer Out of Science Fiction</h1>\
<p class="f5 f4-l lh-copy athelas">\
The tech giant says it is ready to begin planning a quantum computer, a \
powerful cpu machine that relies on subatomic particles instead of \
transistors.\
</p>\
</div>\
<div class="pl3-ns order-1 order-2-ns mb4 mb0-ns w-100 w-40-ns">\
<img class="db" src="https://mrmrs.github.io/photos/cpu.jpg" alt="Photo of a \
dimly lit room with a computer interface terminal."/>\
</div>\
</div>\
<p class="f6 lh-copy gray mv0">By <span class="ttu">Robin Darnell</span></p>\
<time class="f6 db gray">Nov. 21, 2016</time>\
</article>\
<article class="pv4 bt bb b--black-10 ph3 ph0-l">\
<div class="flex flex-column flex-row-ns">\
<div class="w-100 w-60-ns pr3-ns order-2 order-1-ns">\
<h1 class="f3 athelas mt0 lh-title">\
A whale takes up residence in a large body of water</h1>\
<p class="f5 f4-l lh-copy athelas">\
This giant of a whale says it is ready to begin planning a new swim later \
this afternoon. A powerful mammal that relies on fish and plankton instead of \
hamburgers.\
</p>\
</div>\
<div class="pl3-ns order-1 order-2-ns mb4 mb0-ns w-100 w-40-ns">\
<img class="db" src="http://mrmrs.github.io/photos/whale.jpg" alt="Photo of a \
whale&#x27;s tale coming crashing out of the water."/>\
</div>\
</div>\
<p class="f6 lh-copy gray mv0">By <span class="ttu">Katherine Grant</span></p>\
<time class="f6 db gray">Nov. 19, 2016</time>\
</article>\
</section>\
</body>\
</html>\
"""
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

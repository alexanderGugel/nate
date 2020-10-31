"""
Content and markup taken from http://tachyons.io/components/.
"""

from nate import (
    H1,
    H2,
    Article,
    BaseTag,
    Body,
    Div,
    Head,
    Html,
    Img,
    Link,
    Meta,
    P,
    Section,
    Span,
    Time,
    Title,
)


def make_article(
    title: str,
    description: str,
    img_src: str,
    img_alt: str,
    author: str,
    time: str,
) -> BaseTag:
    return Article(
        class_="pv4 bt bb b--black-10 ph3 ph0-l",
        children=[
            Div(
                class_="flex flex-column flex-row-ns",
                children=[
                    Div(
                        class_="w-100 w-60-ns pr3-ns order-2 order-1-ns",
                        children=[
                            H1(
                                class_="f3 athelas mt0 lh-title",
                                children=title,
                            ),
                            P(
                                class_="f5 f4-l lh-copy athelas",
                                children=description,
                            ),
                        ],
                    ),
                    Div(
                        class_="""pl3-ns order-1 order-2-ns mb4 mb0-ns w-100 \
w-40-ns""",
                        children=[Img(src=img_src, class_="db", alt=img_alt)],
                    ),
                ],
            ),
            P(
                class_="f6 lh-copy gray mv0",
                children=["By ", Span(class_="ttu", children=author)],
            ),
            Time(class_="f6 db gray", children=time),
        ],
    )


article_1 = make_article(
    title="""Tech Giant Invests Huge Money to Build a Computer Out of \
Science Fiction""",
    description="""The tech giant says it is ready to begin planning a \
quantum computer, a powerful cpu machine that relies on subatomic particles \
instead of transistors.""",
    img_src="https://mrmrs.github.io/photos/cpu.jpg",
    img_alt="Photo of a dimly lit room with a computer interface terminal.",
    author="Robin Darnell",
    time="Nov. 21, 2016",
)

article_2 = make_article(
    title="A whale takes up residence in a large body of water",
    description="""This giant of a whale says it is ready to begin planning a \
new swim later this afternoon. A powerful mammal that relies on fish and \
plankton instead of hamburgers.""",
    img_src="http://mrmrs.github.io/photos/whale.jpg",
    img_alt="Photo of a whale's tale coming crashing out of the water.",
    author="Katherine Grant",
    time="Nov. 19, 2016",
)

tachyon_css = "https://unpkg.com/tachyons@4.12.0/css/tachyons.min.css"

section = Section(
    class_="mw7 center",
    children=[
        H2(class_="athelas ph3 ph0-l", children="News"),
        article_1,
        article_2,
    ],
)

head = Head(
    children=[
        Meta(charset="utf-8"),
        Meta(
            name="viewport",
            content="width=device-width, initial-scale=1",
        ),
        Title(children="Example Title"),
        Link(rel="stylesheet", href=tachyon_css),
    ]
)
html = Html(
    lang="en",
    children=[head, Body(class_="sans-serif", children=[section])],
)

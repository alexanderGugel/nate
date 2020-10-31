from .common import html


def bench() -> str:
    return html.to_html()


if __name__ == "__main__":
    import timeit

    print(timeit.timeit("bench()", setup="from __main__ import bench"))

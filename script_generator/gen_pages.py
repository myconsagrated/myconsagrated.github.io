from script_generator.generate_html import generate_html_page


# main loop:
# create index
# create newsletters pages (for now it will stay in the index)

def main():

    # generate index.html
    html = generate_html_page("./html_source/banner_index.html")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


    # for post in newsletter html_source
    


def test():

    import os
    from fnmatch import fnmatch

    root = './'
    pattern = "*.html"

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                print(os.path.join(path, name))


if __name__ == "__main__":
    test()
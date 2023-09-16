from script_generator.generate_html import generate_html_page


# main loop:
# create index
# create newsletters pages (for now it will stay in the index)

def main():

    # generate index.html
    html = generate_html_page("./html_source/index.html")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)


    # for post in newsletter html_source
    file_list = get_file_path_in_source_folder()
    for file in file_list:
        new_path = str(file).replace("html_source/", "")
        html = generate_html_page(str(file))

        with open(new_path, "w", encoding="utf-8") as f:
            f.write(html)
    

def get_file_path_in_source_folder():

    import os
    from fnmatch import fnmatch

    root = './html_source'
    pattern = "*.html"
    list_paths = []
    for path, subdirs, files in os.walk(root):
        if "experiments" in path:
            continue
        for name in files:
            if fnmatch(name, pattern):
                # print(os.path.join(path, name))
                list_paths.append(os.path.join(path, name))

    return list_paths

if __name__ == "__main__":
    main()
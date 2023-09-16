### Main template

def generate_html_page(file_post_path):
    """
    <head>
    <body>
    """

    html = """
    <!DOCTYPE HTML>
    <html>
    """

    html += return_head()
    html += return_body(file_post_path)

    html += """</html>"""

    return html


def return_head():
    return """
    	<head>
            <title>Jardim do MyConsagrated</title>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
            <link rel="stylesheet" href="/assets/css/main.css" />
	    </head>
    """


def return_body(file_post_path):
    """
    <wrapper>
    <scripts>
    """
    html = """<body class="is-preload">"""
    html += return_wrapper(file_post_path)
    html += return_scripts()
    html += """</body>"""
    return html



def return_wrapper(file_post_path):
    html = """<div id="wrapper">"""
    html += return_main_content(file_post_path)
    html += generate_sidebar()

    html += """</div>"""
    return html

def return_main_content(file_post_path):
    """
    header
    banner
    section
    """
    html = """
    <!-- Main -->
    <div id="main">
        <div class="inner"> 
    """

    html += return_main_header()

    with open(file_post_path, "r", encoding='utf-8') as f:
        html_file = f.read()

    html += html_file

    html += """</div></div>"""

    return html

def return_main_header():
    return """
    <header id="header">
        <a href="/index.html" class="logo"><strong>Jardim Digital</strong> do MyConsgrated</a>
        <ul class="icons">
            <li><a href="https://github.com/myconsagrated" class="icon brands fa-github"><span class="label">Github</span></a></li>
            <li><a href="https://www.youtube.com/channel/UCvcKENipTzsesA44hROpsLQ" class="icon brands fa-youtube"><span class="label">YouTube</span></a></li>
        </ul>
    </header>
    """

def generate_sidebar():
    """
    Por hora acho que tem tudo que eu preciso, depois adiciono mais coisas
    """
    return """
    <!-- Sidebar -->
    <div id="sidebar">
        <div class="inner">

        <!-- Menu -->
        <nav id="menu">
            <header class="major">
                <h2>Menu</h2>
            </header>
            <ul>
                <li><a href="/index.html">Entrada do Jardim</a></li>
                <li><a href="/newsletters.html">Newsletters</a></li>
            </ul>
        </nav>
        </div>
    </div>

    """


def return_scripts():
    return """
    <script src="/assets/js/jquery.min.js"></script>
	<script src="/assets/js/browser.min.js"></script>
	<script src="/assets/js/breakpoints.min.js"></script>
	<script src="/assets/js/util.js"></script>
	<script src="/assets/js/main.js"></script>
    """

    
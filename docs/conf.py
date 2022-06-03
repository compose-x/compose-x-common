#!/usr/bin/env python
import os
import sys

try:
    import sphinx_material

    UNSAFE = False
except ImportError:
    UNSAFE = True


sys.path.insert(0, os.path.abspath(".."))

import compose_x_common

extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
templates_path = ["_templates"]

# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "Compose-X Commons Lib"
copyright = f"2021-2022, @{compose_x_common.__author__}"
author = compose_x_common.__author__

version = compose_x_common.__version__
# The full version, including alpha/beta/rc tags.
release = compose_x_common.__version__
language = None

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".idea"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

extensions += [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
]

sitemap_locales = ["en"]
autosummary_generate = True
autoclass_content = "class"

html_baseurl = "https://docs.common.compose-x.io"

if not UNSAFE:
    extensions.append("sphinx_material")
    html_theme_path = sphinx_material.html_theme_path()
    html_context = sphinx_material.get_html_context()
    html_theme = "sphinx_material"
    html_theme_options = {
        # Set the name of the project to appear in the navigation.
        "nav_title": "Compose-X Commons Lib",
        "base_url": "https://docs.common.compose-x.io",
        "html_minify": False,
        "html_prettify": True,
        "css_minify": True,
        "color_primary": "blue",
        "color_accent": "light-blue",
        # Set the repo location to get a badge with stats
        "repo_url": "https://github.com/compose-x/compose_x_common/",
        "repo_name": "compose-x/compose_x_common",
        "repo_type": "github",
        "globaltoc_depth": 2,
        "globaltoc_collapse": True,
        "globaltoc_includehidden": False,
    }

    html_sidebars = {
        "**": ["logo-text.html", "globaltoc.html", "localtoc.html", "searchbox.html"]
    }

else:
    extensions.append("sphinx_rtd_theme")
    html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]
html_show_sourcelink = True

# -- Options for HTMLHelp output ---------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "compose_x_commondoc"


# -- Options for LaTeX output ------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "compose_x_common.tex",
        "Compose-X Commons Lib Documentation",
        "John Preston",
        "manual",
    ),
]

# -- Options for manual page output ------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "compose_x_common",
        "Compose-X Commons Lib Documentation",
        [author],
        1,
    )
]

# -- Options for Texinfo output ----------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "compose_x_common",
        "Compose-X Commons Lib Documentation",
        author,
        "compose_x_common",
    ),
]

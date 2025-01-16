# -- Project information

project = 'EnAcuity coding challenge'
copyright = '2024, Solene'
author = 'Solene'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'myst_parser',
    'autodoc2',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

myst_enable_extensions = [
    "linkify",           # Automatically turn URLs into links
    "replacements",      # Enable text replacements
    "heading_anchors",   # Add anchors to headers
    "smartquotes",       # Convert quotes to typographic quotes
    "html_admonition",   # Render admonitions in Markdown
    "html_image",        # Render HTML-style images
]

autodoc2_packages = [
    "components/custom_slider.py"
]
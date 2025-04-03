# SSG

A **S**imple **S**tatic **S**ite generator written in Python.

## Overview

This project is a lightweight static site generator that converts Markdown content into fully functional HTML pages. It uses a custom templating system and supports inline and block-level Markdown syntax. The generated site includes a blog, contact page, and other content, styled with a custom CSS theme.

## Features

- Converts Markdown files to HTML using a custom parser.
- Supports inline Markdown elements like bold, italic, links, and images.
- Handles block-level Markdown elements such as headings, lists, blockquotes, and code blocks.
- Recursively processes directories to generate nested HTML structures.
- Copies static assets (CSS, images, etc.) to the output directory.
- Fully customizable HTML templates.
- Includes unit tests for core functionality.

## Project Structure

- `content/`: Contains the Markdown files for the site content.
- `docs/`: The output directory where the generated HTML files and static assets are stored.
- `src/`: The source code for the static site generator, including Markdown parsing, HTML generation, and file handling.
- `static/`: Static assets like CSS and images.
- `template.html`: The HTML template used for rendering pages.

## Usage

1. Place your Markdown files in the `content/` directory.
2. Customize the `template.html` file to change the layout and design.
3. Run the following command to generate the site:

   ```sh
   python3 src/main.py
   ```

4. The generated site will be available in the `docs/` directory.
5. To preview the site locally, run:

    ```sh
    cd docs && python3 -m http.server 8888
    ```

    Then open `http://localhost:8888` in your browser.

## Development

To run the tests, use:

```sh
python3 -m unittest discover -s src
```

## Dependencies

This project uses only Python's standard library, so no additional dependencies are required.
#!/usr/bin/python3
"""
A script that converts Markdown to HTML.
"""

import sys
import os
import re
import hashlib


def convert_markdown_to_html(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file_1:
        html_content = []
        md_content = [line.rstrip() for line in file_1]

        in_unordered_list = False
        in_ordered_list = False
        in_paragraph = False

        for line in md_content:
            # Convert headings
            heading_match = re.match(r'^(#{1,6}) (.*)', line)
            if heading_match:
                if in_unordered_list:
                    html_content.append('</ul>')
                    in_unordered_list = False
                if in_ordered_list:
                    html_content.append('</ol>')
                    in_ordered_list = False
                if in_paragraph:
                    html_content.append('</p>')
                    in_paragraph = False
                h_level = len(heading_match.group(1))
                html_content.append(
                        f'<h{h_level}>{heading_match.group(2)}</h{h_level}>')
            # Convert unordered lists
            elif line.startswith('- '):
                if in_ordered_list:
                    html_content.append('</ol>')
                    in_ordered_list = False
                if not in_unordered_list:
                    html_content.append('<ul>')
                    in_unordered_list = True
                item = line[2:]  # Remove '- ' from the start
                html_content.append(f'<li>{item}</li>')
            # Convert ordered lists
            elif line.startswith('* '):
                if in_unordered_list:
                    html_content.append('</ul>')
                    in_unordered_list = False
                if not in_ordered_list:
                    html_content.append('<ol>')
                    in_ordered_list = True
                item = line[2:]  # Remove '* ' from the start
                html_content.append(f'<li>{item}</li>')
            else:
                if in_unordered_list:
                    html_content.append('</ul>')
                    in_unordered_list = False
                if in_ordered_list:
                    html_content.append('</ol>')
                    in_ordered_list = False

                # Handle special cases
                line = re.sub(r'\[\[(.+?)\]\]',
                              lambda match: hashlib.md5(
                                  match.group(1).encode()).hexdigest(), line)
                line = re.sub(r'\(\((.+?)\)\)',
                              lambda match: match.group(1).replace('c', '')
                              .replace('C', ''), line)

                # Convert paragraphs
                if line:
                    if not in_paragraph:
                        html_content.append('<p>')
                        in_paragraph = True
                    # Handle bold and emphasized text within paragraphs
                    line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
                    line = re.sub(r'__(.+?)__', r'<em>\1</em>', line)
                    if html_content[-1] != '<p>':
                        html_content.append('<br/>')
                    html_content.append(line)
                else:
                    if in_paragraph:
                        html_content.append('</p>')
                        in_paragraph = False

        # Close any remaining open tags
        if in_unordered_list:
            html_content.append('</ul>')
        if in_ordered_list:
            html_content.append('</ol>')
        if in_paragraph:
            html_content.append('</p>')

    with open(output_file, 'w', encoding='utf-8') as file_2:
        file_2.write('\n'.join(html_content) + '\n')


if __name__ == '__main__':
    # Check that the number of arguments passed is 2
    if len(sys.argv) != 3:
        print('Usage: ./markdown2html.py README.md README.html',
              file=sys.stderr)
        sys.exit(1)

    # Store the arguments into variables
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check that the markdown file exists and is a file
    if not (os.path.exists(input_file) and os.path.isfile(input_file)):
        print(f'Missing {input_file}', file=sys.stderr)
        sys.exit(1)

    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)

from textnode import *
import os
import shutil
from convert_functions import *
import sys
def clear_directory_contents(path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

def copy_source(path, dest):
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        print(item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            shutil.copy(item_path, dest)
        elif os.path.isdir(item_path):
            dir_path = f"{dest}{item}/" 
            os.mkdir(dir_path)
            new_path = item_path + "/"
            copy_source(new_path, dir_path)

# def generate_page(from_path, template_path, dest_path):
#     print(f"Generating page from {from_path} to {dest_path} using {template_path}")
#     try:
#         with open(from_path, 'r') as file:
#             md = file.read()
#     except FileNotFoundError:
#         print(f"Error: The file '{from_path}' was not found.")

#     title = extract_title(md)

#     try:
#         with open(template_path, 'r') as file:
#             template = file.read()
#             print(template)
#     except FileNotFoundError:
#         print(f"Error: The file '{template_path}' was not found.")

#     node = markdown_to_html_node(md)
#     html_string = node.to_html()


#     print("DEBUG: ", title)
#     print("HTML: ", string)

#     try:
#         with open(dest_path, 'w', encoding='utf-8') as file:
#             with open(template_path, 'r') as temp_file:
#                 template = temp_file.read()
#                 template = template.replace("{{ Title }}", title)
#                 template = template.replace("{{ Content }}", html_string)
            
#                 file.write(template)
#     except FileNotFoundError:
#         print(f"Error: The file '{template_path}' was not found.")


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read Markdown content
    try:
        with open(from_path, 'r', encoding='utf-8') as file:
            md = file.read()
    except FileNotFoundError:
        print(f"❌ Error: Markdown file '{from_path}' not found.")
        return

    # Extract title and convert to HTML
    title = extract_title(md)
    node = markdown_to_html_node(md)
    html_string = node.to_html()

    print("DEBUG — Title:", title)
    print("DEBUG — HTML preview:", html_string[:100], "...")  # print first 100 chars only

    # Read and apply template
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template = file.read()
    except FileNotFoundError:
        print(f"❌ Error: Template file '{template_path}' not found.")
        return

    filled_template = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", html_string)
        .replace('href="/', f'href="{base_path}')
        .replace('src="/', f'src="{base_path}')
    )
    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write final HTML
    try:
        with open(dest_path, 'w', encoding='utf-8') as file:
            file.write(filled_template)
        print(f"✅ Page generated at {dest_path}")
    except Exception as e:
        print(f"❌ Error writing to '{dest_path}': {e}")


# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
#     for item in os.listdir(dir_path_content):
#         item_path = os.path.join(dir_path_content, item)
#         if os.path.isfile(item_path) and item_path[-3:] == ".md":
#             generate_page(item_path, template_path, dest_dir_path)
#         elif os.path.isdir(item_path):
#             dir_path = f"{dest_dir_path}/{item}/" 
#             os.mkdir(dir_path)
#             generate_pages_recursive(item_path, template_path, dir_path)
#         else:
#             continue
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        print(f"Current item path: {item_path}")

        if os.path.isfile(item_path) and item_path.endswith(".md"):
            generate_page(item_path, template_path, dest_dir_path + "/index.html", base_path)

        elif os.path.isdir(item_path):
            dir_path = os.path.join(dest_dir_path, item)
            os.makedirs(dir_path, exist_ok=True)

            generate_pages_recursive(item_path, template_path, dir_path, base_path)

# def generate_pages_recursive(src_dir, template_path, dest_dir):
#     for item in os.listdir(src_dir):
#         item_path = os.path.join(src_dir, item)
#         dest_path = os.path.join(dest_dir, item)

#         if os.path.isdir(item_path):
#             os.makedirs(dest_path, exist_ok=True)
#             generate_pages_recursive(item_path, template_path, dest_path)
#         elif os.path.isfile(item_path) and item_path[-3:] == ".md" :
#             generate_page(item_path, template_path, dest_dir)


def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    clear_directory_contents("docs/")

    copy_source("static/", "docs/")

    generate_pages_recursive("content", "template.html", "docs", basepath)

main()

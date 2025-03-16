import os
import markdown
import glob
import shutil

def convert_md_to_html():
    # Create docs directory if it doesn't exist
    if not os.path.exists('docs'):
        os.makedirs('docs')

    # First, copy all root markdown files to docs if they don't exist there
    root_md_files = glob.glob('*.md')
    for md_file in root_md_files:
        docs_path = os.path.join('docs', md_file)
        if not os.path.exists(docs_path):
            shutil.copy2(md_file, docs_path)
            print(f'Copied {md_file} to docs directory')

    # Also copy job markdown files if they exist
    if os.path.exists('jobs'):
        if not os.path.exists('docs/jobs'):
            os.makedirs('docs/jobs')
        job_md_files = glob.glob('jobs/*.md')
        for md_file in job_md_files:
            docs_path = os.path.join('docs', md_file)
            os.makedirs(os.path.dirname(docs_path), exist_ok=True)
            shutil.copy2(md_file, docs_path)
            print(f'Copied {md_file} to docs directory')

    # HTML template for main docs
    main_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 1rem;
            text-align: center;
        }}
        .nav {{
            background: #34495e;
            padding: 1rem;
            text-align: center;
        }}
        .nav a {{
            color: white;
            text-decoration: none;
            margin: 0 1rem;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: background 0.3s;
        }}
        .nav a:hover {{
            background: #2c3e50;
        }}
        .content {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
            transition: color 0.3s;
        }}
        a:hover {{
            color: #2980b9;
        }}
        pre {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }}
        code {{
            background: #f8f9fa;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
        }}
        .breadcrumbs {{
            padding: 1rem;
            background: #f8f9fa;
            margin-bottom: 1rem;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
    </div>
    
    <div class="nav">
        <a href="/ai-dc/index.html">Home</a>
        <a href="/ai-dc/documentation.html">Documentation</a>
        <a href="/ai-dc/components.html">Components</a>
    </div>

    <div class="content">
        <div class="breadcrumbs">
            <a href="/ai-dc/index.html">Home</a> / {breadcrumbs}
        </div>
        {content}
    </div>
</body>
</html>'''

    # Convert all markdown files in docs directory and subdirectories
    for root, dirs, files in os.walk('docs'):
        for md_file in files:
            if md_file.endswith('.md'):
                full_path = os.path.join(root, md_file)
                
                # Read markdown content
                with open(full_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()

                # Convert to HTML
                html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
                
                # Get title from filename
                title = os.path.basename(md_file).replace('.md', '').replace('_', ' ')
                
                # Create breadcrumbs
                rel_path = os.path.relpath(full_path, 'docs')
                path_parts = os.path.dirname(rel_path).split(os.sep)
                breadcrumbs = ' / '.join(path_parts + [title]) if path_parts[0] != '.' else title
                
                # Create HTML file
                html_file = full_path.replace('.md', '.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(main_template.format(
                        title=title,
                        breadcrumbs=breadcrumbs,
                        content=html_content
                    ))
                
                print(f'Converted {full_path} to {html_file}')

    # Update main HTML files to use absolute paths
    main_files = ['index.html', 'documentation.html', 'components.html']
    for file in main_files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update links to use /ai-dc prefix
            content = content.replace('href="docs/', 'href="/ai-dc/docs/')
            content = content.replace('href="index.html"', 'href="/ai-dc/index.html"')
            content = content.replace('href="documentation.html"', 'href="/ai-dc/documentation.html"')
            content = content.replace('href="components.html"', 'href="/ai-dc/components.html"')
            
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Updated links in {file}')

if __name__ == '__main__':
    convert_md_to_html() 
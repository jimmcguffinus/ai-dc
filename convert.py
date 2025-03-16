import os
import markdown
import glob

def convert_md_to_html():
    # Create docs directory if it doesn't exist
    if not os.path.exists('docs'):
        os.makedirs('docs')

    # Get all markdown files
    md_files = glob.glob('docs/*.md')

    # HTML template
    template = '''<!DOCTYPE html>
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
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
    </div>
    
    <div class="nav">
        <a href="../index.html">Home</a>
        <a href="../documentation.html">Documentation</a>
        <a href="../components.html">Components</a>
    </div>

    <div class="content">
        {content}
    </div>
</body>
</html>'''

    # Convert each markdown file
    for md_file in md_files:
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # Get title from filename
        title = os.path.basename(md_file).replace('.md', '').replace('_', ' ')
        
        # Create HTML file
        html_file = md_file.replace('.md', '.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(template.format(title=title, content=html_content))
        
        print(f'Converted {md_file} to {html_file}')

if __name__ == '__main__':
    convert_md_to_html() 
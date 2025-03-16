import os
import markdown
import glob
import shutil
import logging
from markdown.extensions import fenced_code, tables, toc

# Set up logging
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info(f'Created directory: {path}')

def copy_markdown_files(source_dir, target_dir):
    """Copy markdown files from source to target directory"""
    ensure_directory(target_dir)
    
    # Get all markdown files in the source directory (non-recursive)
    for file in os.listdir(source_dir):
        if file.endswith('.md'):
            source_path = os.path.join(source_dir, file)
            target_file = os.path.join(target_dir, file)
            
            # Copy file if it doesn't exist or is different
            if not os.path.exists(target_file) or \
               os.path.getmtime(source_path) > os.path.getmtime(target_file):
                shutil.copy2(source_path, target_file)
                logging.info(f'Copied {source_path} to {target_file}')

def convert_md_to_html():
    """Convert all markdown files to HTML with proper structure"""
    # Create docs directory
    ensure_directory('docs')
    
    # Copy markdown files from root directory
    copy_markdown_files('.', 'docs')

    # HTML template with enhanced styling
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
            background: #f5f6fa;
        }}
        .header {{
            background: #2c3e50;
            color: white;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .nav {{
            background: #34495e;
            padding: 1rem;
            text-align: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
        .main-content {{
            background: white;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
            border: 1px solid #e9ecef;
        }}
        code {{
            background: #f8f9fa;
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        }}
        .breadcrumbs {{
            padding: 1rem;
            background: white;
            margin-bottom: 1rem;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        th, td {{
            padding: 0.75rem;
            border: 1px solid #e9ecef;
        }}
        th {{
            background: #f8f9fa;
        }}
        tr:nth-child(even) {{
            background: #f8f9fa;
        }}
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }}
        h1 {{
            border-bottom: 2px solid #3498db;
            padding-bottom: 0.5rem;
        }}
        ul, ol {{
            padding-left: 1.5rem;
        }}
        li {{
            margin: 0.5rem 0;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 1rem 0;
            padding: 1rem;
            background: #f8f9fa;
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
        <div class="main-content">
            {content}
        </div>
    </div>
</body>
</html>'''

    # Convert all markdown files in docs directory
    for file in os.listdir('docs'):
        if file.endswith('.md'):
            try:
                full_path = os.path.join('docs', file)
                
                # Read markdown content
                with open(full_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()

                # Convert to HTML with extended features
                html_content = markdown.markdown(
                    md_content,
                    extensions=[
                        'tables',
                        'fenced_code',
                        'toc',
                        'attr_list',
                        'def_list',
                        'footnotes'
                    ]
                )
                
                # Get title from filename
                title = os.path.basename(file).replace('.md', '').replace('_', ' ')
                
                # Create breadcrumbs
                breadcrumbs = title
                
                # Create HTML file
                html_file = full_path.replace('.md', '.html')
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(main_template.format(
                        title=title,
                        breadcrumbs=breadcrumbs,
                        content=html_content
                    ))
                
                logging.info(f'Converted {full_path} to {html_file}')
            except Exception as e:
                logging.error(f'Error converting {file}: {str(e)}')

    # Update main HTML files to use absolute paths
    main_files = ['index.html', 'documentation.html', 'components.html']
    for file in main_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update links to use /ai-dc prefix
                content = content.replace('href="', 'href="/ai-dc/')
                content = content.replace('href="/ai-dc/http', 'href="http')  # Fix external links
                content = content.replace('href="/ai-dc/https', 'href="https')  # Fix external links
                content = content.replace('href="/ai-dc/#', 'href="#')  # Fix anchor links
                
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
                logging.info(f'Updated links in {file}')
            except Exception as e:
                logging.error(f'Error updating {file}: {str(e)}')

if __name__ == '__main__':
    try:
        # Clean up docs directory if it exists
        if os.path.exists('docs'):
            shutil.rmtree('docs')
            logging.info('Cleaned up docs directory')
            
        convert_md_to_html()
        logging.info('Conversion completed successfully')
    except Exception as e:
        logging.error(f'Conversion failed: {str(e)}') 
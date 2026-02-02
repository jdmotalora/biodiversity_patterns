import os
import re

content_dir = "content"

def fix_frontmatter(content, filename):
    """Convierte frontmatter de Obsidian a formato Quartz"""
    
    # Si tiene frontmatter de Obsidian
    if content.startswith('---'):
        # Extraer el frontmatter existente
        parts = content.split('---', 2)
        if len(parts) >= 3:
            old_frontmatter = parts[1]
            body = parts[2]
            
            # Crear título desde el nombre del archivo
            title = filename.replace('.md', '').replace('..', '.')
            
            # Nuevo frontmatter para Quartz
            new_frontmatter = f"---\ntitle: {title}\n---"
            
            return new_frontmatter + body
    
    # Si no tiene frontmatter, agregarlo
    title = filename.replace('.md', '').replace('..', '.')
    return f"---\ntitle: {title}\n---\n\n{content}"

def fix_image_syntax(content):
    """Convierte ![[imagen.png]] a formato Markdown estándar"""
    # Patrón: ![[nombre.extension]]
    pattern = r'!\[\[([^\]]+\.(png|jpg|jpeg|gif|webp|svg))\]\]'
    replacement = r'![imagen](/Images/\1)'
    return re.sub(pattern, replacement, content, flags=re.IGNORECASE)

def fix_html_centering(content):
    """Elimina tags HTML de centrado que pueden causar problemas"""
    content = re.sub(r'<p align="center">(.*?)</p>', r'\n\n**\1**\n\n', content)
    return content

def process_file(filepath, filename):
    """Procesa un archivo completo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Aplicar correcciones
        content = fix_frontmatter(content, filename)
        content = fix_image_syntax(content)
        content = fix_html_centering(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Corregido: {filename}")
        return True
    except Exception as e:
        print(f"✗ Error en {filename}: {str(e)}")
        return False

# Procesar todos los archivos
print("Iniciando corrección de archivos...\n")
fixed = 0
errors = 0

for filename in os.listdir(content_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(content_dir, filename)
        if process_file(filepath, filename):
            fixed += 1
        else:
            errors += 1

print(f"\n{'='*50}")
print(f"✓ Archivos corregidos: {fixed}")
print(f"✗ Errores: {errors}")
print(f"{'='*50}")
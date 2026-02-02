import os
import re

content_dir = "content"

def fix_image_links(content):
    """Convierte referencias de imágenes de Obsidian a formato correcto para Quartz"""
    
    # Patrón 1: ![[imagen.extension]]
    # Lo convierte a: ![](Images/imagen.extension)
    pattern1 = r'!\[\[([^\]]+\.(png|jpg|jpeg|gif|webp|svg|PNG|JPG|JPEG))\]\]'
    content = re.sub(pattern1, r'![](\1)', content, flags=re.IGNORECASE)
    
    # Patrón 2: Asegurar que apunte a la carpeta Images/
    # Si la imagen no tiene ruta, agregar Images/
    pattern2 = r'!\[\]\((?!Images/)([^/)]+\.(png|jpg|jpeg|gif|webp|svg|PNG|JPG|JPEG))\)'
    content = re.sub(pattern2, r'![](Images/\1)', content, flags=re.IGNORECASE)
    
    return content

def process_file(filepath, filename):
    """Procesa un archivo y corrige las referencias de imágenes"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        content = fix_image_links(content)
        
        # Solo guardar si hubo cambios
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Corregido: {filename}")
            return True
        else:
            print(f"○ Sin cambios: {filename}")
            return False
    except Exception as e:
        print(f"✗ Error en {filename}: {str(e)}")
        return False

# Procesar todos los archivos .md
print("Corrigiendo enlaces de imágenes...\n")
fixed = 0

for filename in os.listdir(content_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(content_dir, filename)
        if process_file(filepath, filename):
            fixed += 1

print(f"\n{'='*50}")
print(f"✓ Archivos modificados: {fixed}")
print(f"{'='*50}")
print("\nAhora ejecuta:")
print("git add content/")
print('git commit -m "fix: corregir enlaces de imágenes"')
print("git push origin main")
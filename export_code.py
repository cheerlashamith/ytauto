import os
from pathlib import Path

# Files to include based on extension
EXTENSIONS = {'.py', '.js', '.html', '.css', '.json', '.bat', '.txt', '.md'}

# Directories to exclude
EXCLUDE_DIRS = {'__pycache__', '.git', 'node_modules', '.venv', 'outputs', 'venv', 'env'}

def export_code(root_dir: str, output_file: str):
    root_path = Path(root_dir).resolve()
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"=== FULL CODEBASE EXPORT ===\n")
        outfile.write(f"Root Directory: {root_path.name}\n\n")
        
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Exclude unwanted directories in-place
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            
            for file in filenames:
                path = Path(dirpath) / file
                
                # Skip the output file itself
                if path.resolve() == Path(output_file).resolve():
                    continue
                    
                # Skip if not a text/code file
                if path.suffix.lower() not in EXTENSIONS:
                    continue
                    
                # Ignore very large files (e.g. over 5MB)
                if path.stat().st_size > 5 * 1024 * 1024:
                    continue
                    
                # Write file header and content
                rel_path = path.relative_to(root_path)
                outfile.write("\n" + "="*80 + "\n")
                outfile.write(f"FILE: {rel_path}\n")
                outfile.write("="*80 + "\n\n")
                
                try:
                    content = path.read_text(encoding='utf-8')
                    outfile.write(content)
                    outfile.write("\n")
                except Exception as e:
                    outfile.write(f"[Error reading file: {e}]\n")

if __name__ == '__main__':
    root = r"c:\Users\shami\OneDrive\Desktop\DOWNLOAD_ME_AutoCourse_Final_Master"
    output = os.path.join(root, "FULL_CODEBASE_FOR_AI.txt")
    export_code(root, output)
    print(f"Successfully exported all code to {output}")

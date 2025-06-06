# Manages file creation, iteration saving, and Git commit

import os
import re
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='file_writer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def parse_code_blocks(content):
    """Extract code blocks from markdown content."""
    code_blocks = []
    pattern = r"```(?:(\w+)\n)?(.*?)```"
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        language = match.group(1) or 'text'
        code = match.group(2).strip()
        code_blocks.append({
            'language': language,
            'code': code,
            'timestamp': datetime.now().isoformat()
        })
    
    return code_blocks

def determine_file_path(code_block, content):
    """Determine the appropriate file path for the code block."""
    # Look for file path hints in the content
    file_hints = re.findall(r"file:\s*([^\n]+)", content)
    if file_hints:
        return file_hints[0].strip()
    
    # Default file paths based on language
    language_to_extension = {
        'python': '.py',
        'javascript': '.js',
        'html': '.html',
        'css': '.css',
        'json': '.json'
    }
    
    extension = language_to_extension.get(code_block['language'], '.txt')
    return f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"

def write_changes():
    """
    Reads ai_3_out.txt and applies the generated changes to the codebase.
    """
    try:
        # 1. Read ai_3_out.txt
        with open("ai_3_out.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 2. Parse implementation
        code_blocks = parse_code_blocks(content)
        
        # 3. Apply changes to files
        for block in code_blocks:
            file_path = determine_file_path(block, content)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
            
            # Write the code to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(block['code'])
            
            # 4. Log changes
            logging.info(f"Created/Updated file: {file_path}")
            logging.info(f"Language: {block['language']}")
            logging.info(f"Timestamp: {block['timestamp']}")
            
            print(f"📝 Written to {file_path}")
        
        return True, f"Successfully processed {len(code_blocks)} code blocks"
        
    except Exception as e:
        error_msg = f"Error in write_changes: {str(e)}"
        logging.error(error_msg)
        return False, error_msg

if __name__ == "__main__":
    success, message = write_changes()
    print(message)

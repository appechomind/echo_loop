#!/usr/bin/env python3
"""
Project reorganization script for EchoLoop automation system
"""

import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create the optimized directory structure."""
    directories = [
        'core',           # Core system files
        'agents',         # AI agent modules
        'automation',     # Automation components
        'web',           # Web interface files
        'config',        # Configuration files
        'scripts',       # Batch/shell scripts
        'logs',          # Log files
        'tests',         # Test files
        'data',          # Data files (txt outputs)
        'backup',        # Backup/legacy files
        'utils'          # Utility modules
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created/verified directory: {directory}")

def get_file_mappings():
    """Define where each file should be moved."""
    return {
        # Core system files
        'core': [
            'echo_loop.py',
            'task_queue.py',
            'main_ai_output.py'
        ],
        
        # AI Agents
        'agents': [
            'gemini_agent.py',
            'chatgpt_agent.py', 
            'cursor_agent.py',
            'llama3_agent.py'
        ],
        
        # Automation components
        'automation': [
            'browser_controller.py',
            'chatgpt_typer.py',
            'screen_reader.py',
            'file_writer.py',
            'hotkey_handler.py',
            'cursor_loop_manager.py'
        ],
        
        # Web interface
        'web': [
            'web_monitor.py',
            'echomind_flask_server.py',
            'autoloop_gui.py',
            'server.js',
            'package.json',
            'package-lock.json'
        ],
        
        # Configuration
        'config': [
            '.env',
            'requirements.txt',
            '.gitignore',
            'setup.py'
        ],
        
        # Scripts
        'scripts': [
            'start_system.bat',
            'create_env.bat',
            'create_env.py',
            'fix_env.py',
            'launch_agents.bat',
            'run_echo_loop.bat',
            'run_dual_ai_loop.bat',
            'run_loop.bat'
        ],
        
        # Logs
        'logs': [
            'loop.log',
            'log.txt',
            'evolution_log.txt'
        ],
        
        # Tests
        'tests': [
            'test_system.py',
            'test_env.py',
            'test_gemini.py',
            'test_automation.py'
        ],
        
        # Data files
        'data': [
            'ai_1_out.txt',
            'ai_2_out.txt', 
            'ai_3_out.txt',
            'cursor_prompt.txt',
            'instructions.txt',
            'next_task.txt',
            'prd_text.txt',
            'llama3_response.txt'
        ],
        
        # Backup/legacy
        'backup': [
            'echo_loop_build.zip',
            'index.html',
            'index.html.html',
            'works.html',
            'styles.css'
        ],
        
        # Keep static and templates as they are (web assets)
        # Move js content to web/js
        # Move static content to web/static  
        # Move templates to web/templates
    }

def move_files():
    """Move files to their optimized locations."""
    file_mappings = get_file_mappings()
    moved_count = 0
    
    for target_dir, files in file_mappings.items():
        for filename in files:
            if os.path.exists(filename):
                try:
                    target_path = os.path.join(target_dir, filename)
                    shutil.move(filename, target_path)
                    print(f"✅ Moved {filename} → {target_path}")
                    moved_count += 1
                except Exception as e:
                    print(f"❌ Error moving {filename}: {e}")
            else:
                print(f"⚠️  File not found: {filename}")
    
    # Handle special directories
    special_moves = [
        ('static', 'web/static'),
        ('templates', 'web/templates'),
        ('js', 'web/js'),
        ('agent_backup', 'backup/agent_backup'),
        ('backup_agents', 'backup/backup_agents')
    ]
    
    for source, target in special_moves:
        if os.path.exists(source):
            try:
                if os.path.exists(target):
                    shutil.rmtree(target)
                shutil.move(source, target)
                print(f"✅ Moved directory {source} → {target}")
                moved_count += 1
            except Exception as e:
                print(f"❌ Error moving directory {source}: {e}")
    
    return moved_count

def create_init_files():
    """Create __init__.py files for Python packages."""
    python_dirs = ['core', 'agents', 'automation', 'web', 'utils', 'tests']
    
    for directory in python_dirs:
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write(f'"""\n{directory.title()} module for EchoLoop automation system\n"""\n')
            print(f"✅ Created {init_file}")

def update_imports():
    """Update import statements to reflect new structure."""
    print("\n📝 Import updates needed:")
    print("   - Update echo_loop.py imports to use agents.* and automation.*")
    print("   - Update web_monitor.py to import from core.*")
    print("   - Update test files to import from appropriate modules")
    print("   - Consider creating a main entry point in root directory")

def create_project_summary():
    """Create a project structure summary."""
    summary = """
# EchoLoop Project Structure

## 📁 Directory Organization

- **core/** - Core system components (main loop, task queue)
- **agents/** - AI agent implementations (Gemini, ChatGPT, etc.)
- **automation/** - Browser automation and I/O components
- **web/** - Web interface, Flask server, and frontend assets
- **config/** - Configuration files (.env, requirements.txt)
- **scripts/** - Batch files and setup scripts
- **logs/** - Log files and execution history
- **tests/** - Test scripts and validation tools
- **data/** - Input/output text files and prompts
- **backup/** - Legacy files and backups
- **utils/** - Utility functions and helpers

## 🚀 Entry Points

- `python -m core.echo_loop` - Start main automation loop
- `python -m web.web_monitor` - Start web monitoring interface
- `python -m scripts.start_system` - Complete system startup

## 📦 Package Structure

Each directory is a Python package with proper __init__.py files for clean imports.
"""
    
    with open('PROJECT_STRUCTURE.md', 'w') as f:
        f.write(summary)
    print("✅ Created PROJECT_STRUCTURE.md")

def main():
    """Main reorganization function."""
    print("🔧 Starting EchoLoop project reorganization...")
    print("=" * 50)
    
    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    # Move files
    print("\n📦 Moving files to optimized locations...")
    moved_count = move_files()
    
    # Create Python package files
    print("\n🐍 Creating Python package structure...")
    create_init_files()
    
    # Provide import update guidance
    update_imports()
    
    # Create project summary
    print("\n📋 Creating project documentation...")
    create_project_summary()
    
    print("\n" + "=" * 50)
    print(f"✅ Reorganization complete! Moved {moved_count} files")
    print("🎯 Project is now optimally organized for development")
    print("\n📝 Next steps:")
    print("   1. Update import statements in core files")
    print("   2. Test that all components still work")
    print("   3. Update documentation and README")
    print("   4. Commit changes to version control")

if __name__ == "__main__":
    main() 
# EchoLoop Project Structure

## 📁 Optimized Directory Organization

```
echo_loop_control/
├── 📁 core/                    # Core system components
│   ├── echo_loop.py           # Main automation loop
│   ├── task_queue.py          # Task queue system with retry logic
│   ├── main_ai_output.py      # AI output processing
│   └── __init__.py
│
├── 📁 agents/                  # AI agent implementations
│   ├── gemini_agent.py        # Gemini API integration
│   ├── chatgpt_agent.py       # ChatGPT agent simulation
│   ├── cursor_agent.py        # Cursor AI agent
│   ├── llama3_agent.py        # LLaMA3 agent (legacy)
│   └── __init__.py
│
├── 📁 automation/              # Browser automation & I/O
│   ├── browser_controller.py  # Selenium ChatGPT automation
│   ├── chatgpt_typer.py       # Human-like keyboard simulation
│   ├── screen_reader.py       # OCR screen capture
│   ├── file_writer.py         # Code parsing & file operations
│   ├── hotkey_handler.py      # Hotkey management
│   ├── cursor_loop_manager.py # Cursor automation
│   └── __init__.py
│
├── 📁 web/                     # Web interface & monitoring
│   ├── web_monitor.py         # Flask monitoring dashboard
│   ├── autoloop_gui.py        # PyQt GUI interface
│   ├── echomind_flask_server.py # Alternative Flask server
│   ├── server.js              # Node.js server
│   ├── package.json           # Node.js dependencies
│   ├── package-lock.json      # Node.js lock file
│   ├── 📁 templates/          # HTML templates
│   │   └── ui.html           # Main dashboard UI
│   ├── 📁 static/             # CSS/JS assets
│   │   └── style.css         # Dashboard styling
│   ├── 📁 js/                 # JavaScript modules
│   │   └── echomind-commands.js
│   └── __init__.py
│
├── 📁 config/                  # Configuration files
│   ├── .env                   # Environment variables & API keys
│   ├── requirements.txt       # Python dependencies
│   └── .gitignore            # Git ignore rules
│
├── 📁 scripts/                 # Batch files & setup scripts
│   ├── launch_agents.bat      # Launch AI agents
│   ├── run_echo_loop.bat      # Run main loop
│   ├── run_dual_ai_loop.bat   # Dual AI mode
│   └── run_loop.bat           # General loop runner
│
├── 📁 logs/                    # Log files & execution history
│   ├── loop.log              # Main automation log
│   ├── log.txt               # General log
│   └── evolution_log.txt     # System evolution tracking
│
├── 📁 tests/                   # Test scripts & validation
│   └── __init__.py
│
├── 📁 data/                    # Input/output text files
│   ├── ai_1_out.txt          # Initial prompt input
│   ├── ai_2_out.txt          # ChatGPT response
│   ├── ai_3_out.txt          # Gemini final output
│   ├── cursor_prompt.txt     # Cursor-specific prompts
│   ├── instructions.txt      # System instructions
│   ├── prd_text.txt          # Product requirements
│   ├── next_task.txt         # Next task queue
│   └── llama3_response.txt   # LLaMA3 responses
│
├── 📁 backup/                  # Legacy files & backups
│   ├── echo_loop_build.zip   # Project archive
│   ├── index.html            # Legacy HTML files
│   ├── styles.css            # Legacy CSS
│   ├── 📁 agent_backup/      # Agent backups
│   └── 📁 backup_agents/     # Additional agent backups
│
├── 📁 utils/                   # Utility functions & helpers
│   └── __init__.py
│
├── README.md                   # Project documentation
├── SECURITY.md                # Security guidelines
└── PROJECT_STRUCTURE.md       # This file
```

## 🚀 Entry Points & Usage

### Main System Components
```bash
# Start main automation loop
python -m core.echo_loop

# Start web monitoring dashboard
python -m web.web_monitor

# Run Gemini agent standalone
python -m agents.gemini_agent

# Test browser automation
python -m automation.browser_controller
```

### Web Interface
- **Dashboard**: http://localhost:5000
- **Real-time monitoring** with start/stop/pause controls
- **Log viewing** and system status
- **File content** viewing for AI outputs

### Batch Scripts (Windows)
```cmd
# Complete system startup
scripts\launch_agents.bat

# Run main echo loop
scripts\run_echo_loop.bat

# Dual AI mode
scripts\run_dual_ai_loop.bat
```

## 📦 Package Structure

Each directory is a proper Python package with `__init__.py` files for clean imports:

```python
# Import examples with new structure
from core.echo_loop import main
from agents.gemini_agent import GeminiAgent
from automation.browser_controller import BrowserController
from web.web_monitor import app
```

## 🔧 Configuration

### Environment Variables (config/.env)
```env
# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Browser Settings
BROWSER_HEADLESS=False
BROWSER_TIMEOUT=30

# Automation Settings
MAX_RETRIES=3
RETRY_DELAY=5
ITERATION_DELAY=1

# Git Settings
GIT_REPO_URL=https://github.com/appechomind/echo_loop_control.git
GIT_BRANCH=main

# Logging Settings
LOG_LEVEL=INFO
```

### Dependencies (config/requirements.txt)
- `google-generativeai` - Gemini API
- `selenium` - Browser automation
- `flask` - Web interface
- `pyautogui` - Screen automation
- `pytesseract` - OCR functionality
- `opencv-python` - Image processing
- `python-dotenv` - Environment management
- `gitpython` - Git integration

## 🎯 Benefits of New Structure

1. **Clear Separation of Concerns**
   - Core logic isolated from automation
   - AI agents grouped together
   - Web interface self-contained

2. **Improved Maintainability**
   - Easy to locate specific functionality
   - Reduced import complexity
   - Better code organization

3. **Scalability**
   - Easy to add new agents or automation components
   - Modular architecture supports extensions
   - Clean package structure

4. **Development Workflow**
   - Faster debugging with organized logs
   - Clear entry points for testing
   - Simplified deployment

## 🔄 Migration Notes

### Import Updates Required
- Update any existing scripts to use new import paths
- Web monitor now imports from `core.task_queue`
- Agents import from `agents.*` namespace
- Automation components use `automation.*` namespace

### File Paths
- All data files moved to `data/` directory
- Configuration centralized in `config/`
- Logs organized in `logs/` directory
- Web assets properly structured under `web/`

This optimized structure provides a solid foundation for continued development and maintenance of the EchoLoop automation system. 
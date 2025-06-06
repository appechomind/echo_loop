# Echo Loop Automation System

A robust automation system for seamless prompt-to-production workflow, featuring task queue management, web monitoring, and error handling.

## Features

- Task queue system with retry logic and dependency management
- Web-based monitoring interface
- Real-time progress tracking
- Error handling and recovery
- Git integration for version control
- Browser automation with Selenium
- OCR capabilities with Tesseract
- GUI interface for local control

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR
- Git
- Chrome/Chromium browser
- API keys for OpenAI and Gemini

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd echo_loop
```

2. Run the setup script:
```bash
python setup.py
```

3. Install Tesseract OCR:
   - Windows: Download and install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

4. Configure the environment:
   - Edit the `.env` file with your API keys and settings
   - Configure Git repository URL if needed

## Usage

### Starting the Automation

1. Start the web monitor:
```bash
python web_monitor.py
```

2. Run the main automation:
```bash
python echo_loop.py
```

3. Access the web interface at `http://localhost:5000`

### GUI Interface

For local control, use the GUI interface:
```bash
python autoloop_gui.py
```

## Components

- `echo_loop.py`: Main automation loop
- `task_queue.py`: Task queue management system
- `web_monitor.py`: Web-based monitoring interface
- `autoloop_gui.py`: Local GUI interface
- `browser_controller.py`: Browser automation
- `screen_reader.py`: Screen capture and OCR
- `chatgpt_typer.py`: ChatGPT interaction
- `file_writer.py`: File operations

## Error Handling

The system includes comprehensive error handling:
- Automatic retries for failed tasks
- Dependency management
- Detailed logging
- Error recovery mechanisms

## Monitoring

Monitor the automation through:
- Web interface (`http://localhost:5000`)
- GUI interface
- Log files in the `logs` directory

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and feature requests, please create an issue in the repository.
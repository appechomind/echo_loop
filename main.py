#!/usr/bin/env python3
"""
Main entry point for EchoLoop automation system
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main entry point with command line argument parsing."""
    parser = argparse.ArgumentParser(description='EchoLoop Automation System')
    parser.add_argument('component', choices=['loop', 'web', 'gemini', 'test'], 
                       help='Component to run')
    parser.add_argument('--headless', action='store_true', 
                       help='Run browser in headless mode')
    parser.add_argument('--port', type=int, default=5000,
                       help='Port for web interface (default: 5000)')
    
    args = parser.parse_args()
    
    if args.component == 'loop':
        print("🔄 Starting EchoLoop main automation...")
        from core.echo_loop import main as echo_main
        echo_main()
        
    elif args.component == 'web':
        print(f"🌐 Starting web monitoring interface on port {args.port}...")
        from web.web_monitor import app
        app.run(host='0.0.0.0', port=args.port, debug=True, threaded=True)
        
    elif args.component == 'gemini':
        print("🧠 Running Gemini agent...")
        from agents.gemini_agent import run_gemini_agent
        success = run_gemini_agent()
        sys.exit(0 if success else 1)
        
    elif args.component == 'test':
        print("🧪 Running system tests...")
        from automation.browser_controller import test_browser_controller
        test_browser_controller()

if __name__ == "__main__":
    main() 
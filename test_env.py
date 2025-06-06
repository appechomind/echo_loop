#!/usr/bin/env python3
"""
Test script to verify .env file configuration for EchoLoop system
"""

def test_env_file():
    """Test .env file configuration."""
    print("🔑 Testing .env configuration...")
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
            print("📋 .env file contents:")
            print(content)
            print("=" * 50)
            
            # Check for Gemini API key
            if 'GEMINI_API_KEY=' in content:
                # Extract the API key line
                lines = content.strip().split('\n')
                api_key_line = None
                for line in lines:
                    if line.startswith('GEMINI_API_KEY='):
                        api_key_line = line
                        break
                
                if api_key_line:
                    api_key = api_key_line.split('=')[1].strip()
                    if api_key.startswith('AIzaSy') and len(api_key) > 30:
                        print("✅ Gemini API key is properly configured!")
                        print(f"   Key starts with: {api_key[:10]}...")
                        return True
                    else:
                        print("❌ Gemini API key format is invalid")
                        print(f"   Found: {api_key}")
                        return False
                else:
                    print("❌ GEMINI_API_KEY line not found")
                    return False
            else:
                print("❌ GEMINI_API_KEY not found in .env file")
                return False
                
    except FileNotFoundError:
        print("❌ .env file not found")
        return False
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def main():
    """Run the .env test."""
    print("=" * 50)
    print("    EchoLoop .env Configuration Test")
    print("=" * 50)
    print()
    
    if test_env_file():
        print("\n🎉 .env file is correctly configured!")
        print("✅ The Gemini API key test should now pass.")
        return True
    else:
        print("\n⚠️ .env file configuration needs to be fixed.")
        print("❌ Please check the API key format.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 
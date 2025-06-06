from gemini_agent import run_gemini_agent

def test_gemini_integration():
    """
    Test the Gemini agent integration by running it with a sample input.
    """
    # Create a sample input file
    test_input = """Generate a simple web application that displays a counter.
    The counter should increment when a button is clicked.
    Include both frontend and backend components."""
    
    with open("ai_2_out.txt", "w", encoding="utf-8") as f:
        f.write(test_input)
    
    # Run the Gemini agent
    run_gemini_agent()
    
    # Read and print the output
    try:
        with open("ai_3_out.txt", "r", encoding="utf-8") as f:
            output = f.read()
            print("\n=== Gemini Agent Output ===")
            print(output)
            print("==========================\n")
    except FileNotFoundError:
        print("Error: ai_3_out.txt not found")

if __name__ == "__main__":
    test_gemini_integration() 
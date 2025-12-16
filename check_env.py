import sys
import pkg_resources

print(f"Python version: {sys.version}")

try:
    import google.genai
    print("google.genai imported successfully")
    print(f"google.genai version: {getattr(google.genai, '__version__', 'unknown')}")
except ImportError as e:
    print(f"Failed to import google.genai: {e}")

try:
    import google.generativeai
    print("google.generativeai imported successfully")
    print(f"google.generativeai version: {getattr(google.generativeai, '__version__', 'unknown')}")
except ImportError as e:
    print(f"Failed to import google.generativeai: {e}")

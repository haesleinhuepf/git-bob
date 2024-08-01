import os
import sys

print("Hello")
# Read the environment variable "ANTHROPIC_API_KEY"
api_key = os.environ.get("ANTHROPIC_API_KEY")

# Check if the environment variable is not None
print("Hello")
if api_key is not None:
    print("world!")

# Print out all arguments passed to the script
print("Script arguments:")
for arg in sys.argv[1:]:
    print(arg)

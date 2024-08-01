import os
import sys

from github_utilities import comment_on_issue, get_conversation_on_issue

print("Hello")
# Read the environment variable "ANTHROPIC_API_KEY"
api_key = os.environ.get("ANTHROPIC_API_KEY")

# Check if the environment variable is not None
print("Hello")
if api_key is not None:
    print("world!")
if api_key[0] == '"':
    print("nej!")

# Print out all arguments passed to the script
print("Script arguments:")
for arg in sys.argv[1:]:
    print(arg)

task = sys.argv[1]
repository = sys.argv[2] if len(sys.argv) > 2 else None
issue = int(sys.argv[3]) if len(sys.argv) > 3 else None

if task == "response-pull-request":

    comment_on_issue(repository, issue, "Hellooo world!")

print("Conversation:")
print(get_conversation_on_issue(repository, issue))

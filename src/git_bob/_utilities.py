# This module provides utility functions for text processing, including functions to remove indentation and outer markdown from text.
from functools import lru_cache


def remove_indentation(text):
    text = text.replace("\n    ", "\n")

    return text.strip()


def remove_outer_markdown(text):
    code = text \
        .replace("```python", "```") \
        .replace("```Python", "```") \
        .replace("```nextflow", "```") \
        .replace("```java", "```") \
        .replace("```javascript", "```") \
        .replace("```macro", "```") \
        .replace("```groovy", "```") \
        .replace("```jython", "```") \
        .replace("```md", "```") \
        .replace("```markdown", "```") \
        .replace("```txt", "```") \
        .replace("```csv", "```") \
        .replace("```yml", "```") \
        .replace("```yaml", "```") \
        .replace("```json", "```") \
        .replace("```py", "```")

    parts = code.split("```")
    if len(parts) == 1:
        code = None
    else:
        code = ""
        for t, c in zip(parts[::2], parts[1::2]):
            code = code + c
        code = code.strip("\n")

    return code

@lru_cache(maxsize=1)
def get_llm_name():
    import os
    return os.environ.get("GIT_BOB_LLM_NAME", "gpt-4o-2024-05-13")

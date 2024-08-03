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

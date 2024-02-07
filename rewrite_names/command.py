import sys
import re

from devchat.llm import chat
from devchat.ide.vscode_services import selected_lines, visible_lines, diff_apply

def get_selected_code():
    selected_data = selected_lines()

    miss_selected_error = "Please select some text."
    if selected_data["selectedText"] == "":
        print(miss_selected_error, file=sys.stderr, flush=True)
        sys.exit(-1)
    
    return selected_data

def get_visible_code():
    visible_data = visible_lines()
    return visible_data


RENAME_PROMPT = """
Following is my selected code to refactor:
{selected_text}

Following is my visible code in editor:
{visible_text}

Your task: refine internal variable and function names within the code to achieve concise and meaningful identifiers that comply with English naming conventions.

Please modify only the selected portion of the code.
Please ensure that the revised code segment maintains the same indentation as the 
selected code to seamlessly integrate with the existing code structure and maintain 
correct syntax. Just refactor the selected code. Keep all other information as it is. 
"""
@chat(prompt=RENAME_PROMPT, stream_out=True)
def refine_names(selected_text, visible_text):
    pass


def extract_markdown_block(text):
    """
    Extracts the first Markdown code block from the given text without the language specifier.

    :param text: A string containing Markdown text
    :return: The content of the first Markdown code block, or None if not found
    """
    pattern = r"```(?:\w+)?\s*\n(.*?)\n```"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        block_content = match.group(1)
        return block_content
    else:
        return text

print("hello world")
print("response from AI:\n\n")

selected_text = get_selected_code()
visible_text = get_visible_code()
response = refine_names(selected_text=selected_text, visible_text=visible_text)
new_code = extract_markdown_block(response)
diff_apply("", new_code)

sys.exit(0)
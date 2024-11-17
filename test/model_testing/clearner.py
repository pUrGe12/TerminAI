import re

a = '''
@@@json
{
  "operation": "open",
  "path": "/path/to/file",
  "mode": "read-only"
}
@@@

$$$summary
Opened file in read-only mode at /path/to/file.
$$$

'''

# Use a capturing group to get the text between $$$summary and $$$
match = re.search(r"\$\$\$summary\s*(.*?)\s*\$\$\$", a, re.DOTALL)
if match:
    result = match.group(1).strip()
    print(result)

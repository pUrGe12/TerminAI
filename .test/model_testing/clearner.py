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

print(re.findall("\$\$\$.*\$\$\$", a, re.DOTALL)[0].strip())

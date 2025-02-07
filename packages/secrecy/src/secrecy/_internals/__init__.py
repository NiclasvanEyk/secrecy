"""# DO NOT IMPORT DIRECTLY FROM THIS MODULE.

It is intended for **internal** organization and won't be covered by backwards compatibility.
Files and functions will be renamed, moved, or even deleted without regards for semver versions!

Instead, import from one of the top-level modules not beginning in an underscore:

```python
# ❌ bad
from secrecy._internals.sync import Secret

# ✅ good
from secrecy import Secret
```
"""

# TODO: Incomplete / Placeholder Functions

Summary: I scanned the codebase for common placeholder markers (`pass`, `TODO`, `NotImplementedError`, `Ellipsis`). Findings are conservative: only explicit placeholders are listed below. If you want a deeper AST-based scan for functions that return `None` or have trivial bodies, I can run that next.

## Findings

- **`app/forms/comment/update_comment_form.py`**: `UpdateCommentForm` contains only a `pass` (it inherits `CreateCommentForm`).
  - Why: class currently has no override or additional fields/validation.
  - Suggested action: implement any update-specific form behavior (e.g., limit editable fields), or remove this subclass if unnecessary.

## Notes

- No occurrences of `raise NotImplementedError` or `TODO` comments were found during the scan.
- Many files contain full implementations; no other obvious placeholder functions detected.

## Next steps (optional)

- Run an AST-based scan to find functions whose bodies are empty or consist only of trivial returns (e.g., `return None`).
- Manually review services and business-logic layers (`app/services/`) for unimplemented behaviors.


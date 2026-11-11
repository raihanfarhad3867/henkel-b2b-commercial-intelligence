# GitHub publication checklist

- [ ] Review all source URLs, report periods and published financial figures before claiming they are verified.
- [ ] Confirm company/team acronym and reporting scope; FSC reporting line is not publicly verified in this project.
- [ ] Ensure `DISCLAIMER.md` and synthetic labels remain visible in all screenshots and social posts.
- [ ] Never upload a recruiter email, interview recording, internal Henkel material, private customer list, passwords, or CRM exports.
- [ ] Open the final `.xlsx` and deck; check no hidden notes, real contact details or unsupported claims.
- [ ] Publish original code and analysis, **not** complete source PDFs or company logos without permission.
- [ ] If you later build a `.pbix`, confirm source file paths work after publication and add a dashboard screenshot.
- [ ] Run `python scripts/reproduce_all.py` and `python -m unittest discover -s tests -v` before each release.

## Create your public repository
1. On GitHub: **New repository** → `henkel-b2b-commercial-intelligence` → Public; leave generated README/License unchecked (provided here).
2. Unzip locally, open a terminal in the repository folder.
3. Run:

```bash
git init
git add .
git commit -m "Initial release: independent commercial intelligence portfolio"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/henkel-b2b-commercial-intelligence.git
git push -u origin main
```

Replace `YOUR-USERNAME`. This archive has not been pushed to any remote repository.

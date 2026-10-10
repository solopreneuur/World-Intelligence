#!/usr/bin/env python3
"""Send a markdown file as an HTML email via Gmail.
Usage: python3 send_email.py "Subject line" path/to/file.md
       python3 send_email.py "Subject line" path/to/file.md --preview out.html
If the file has an "If you read nothing else" summary blockquote, the subject
becomes "World Intel · <Day Mon D> · <first label>" and the summary labels
become the inbox preview text. Otherwise the subject passed in is used as is.
--preview writes the HTML to a file and prints the subject instead of sending.
"""
import os, re, smtplib, sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape
from pathlib import Path

import markdown

BODY_STYLE = (
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;"
    "font-size:15px;line-height:1.55;color:#1f1f1f;max-width:680px;margin:0 auto;"
    "padding:16px;overflow-wrap:break-word;word-wrap:break-word"
)
STYLES = {
    "h1": "font-size:22px;line-height:1.3;margin:0 0 12px",
    "h2": "font-size:19px;line-height:1.3;margin:28px 0 14px;padding-bottom:6px;"
          "border-bottom:1px solid #e2e2e2",
    "h3": "font-size:12px;line-height:1.4;font-weight:600;letter-spacing:0.08em;"
          "text-transform:uppercase;color:#6b6b6b;margin:32px 0 12px;padding-top:18px;"
          "border-top:1px solid #e2e2e2",
    "p": "margin:0 0 14px",
    "blockquote": "margin:0 0 20px;padding:12px 16px;background:#f4f4f4;"
                  "border-left:4px solid #c8c8c8;border-radius:4px",
    "ol": "margin:0;padding-left:22px",
    "ul": "margin:0 0 14px;padding-left:22px",
    "li": "margin:0 0 8px",
    "a": "color:#3b6894;text-decoration:none",
    "hr": "border:0;border-top:1px solid #e2e2e2;margin:24px 0",
}
TAG = re.compile(r"<(%s)\b([^>]*?)(\s*/?)>" % "|".join(STYLES))


def summary_labels(text):
    """Bold labels from the 'If you read nothing else' blockquote, if present."""
    block = re.search(r"^>.*If you read nothing else.*?(?=^(?!>)|\Z)", text, re.M | re.S | re.I)
    if not block:
        return []
    return re.findall(r"^>\s*\d+\.\s+\*\*(.+?)\*\*", block.group(0), re.M)[:3]


def to_html(body, labels):
    html = markdown.markdown(body, extensions=["nl2br", "sane_lists"])
    html = TAG.sub(lambda m: f'<{m[1]}{m[2]} style="{STYLES[m[1]]}"{m[3]}>', html)
    preheader = ""
    if labels:
        padding = "&#847;&zwnj;&nbsp;" * 100  # keeps body text out of the inbox preview
        preheader = (
            '<div style="display:none;font-size:1px;line-height:1px;max-height:0;max-width:0;'
            'opacity:0;overflow:hidden;mso-hide:all;color:transparent">'
            f'{escape(" · ".join(labels))}{padding}</div>'
        )
    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"></head>'
        f'<body style="margin:0;padding:0;background:#ffffff">{preheader}'
        f'<div style="{BODY_STYLE}">{html}</div></body></html>'
    )


env = dict(os.environ)  # GitHub Actions secrets arrive here
env_file = Path(__file__).parent / ".env"  # optional, local testing only
for line in (env_file.read_text().splitlines() if env_file.exists() else []):
    if "=" in line and not line.strip().startswith("#"):
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()

subject, path = sys.argv[1], Path(sys.argv[2])
preview = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--preview" else None
body = path.read_text(errors="replace")[-200000:]

labels = summary_labels(body)
if labels:
    now = datetime.now()
    subject = f"World Intel · {now:%a %b} {now.day} · {labels[0]}"
html = to_html(body, labels)

if preview:
    Path(preview).write_text(html)
    print(f"subject: {subject}")
    print(f"preheader: {' · '.join(labels) or '(none)'}")
    print(f"wrote: {preview}")
    sys.exit()

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = env["GMAIL_USER"]
msg["To"] = env["EMAIL_TO"]
msg.attach(MIMEText(body, "plain"))
msg.attach(MIMEText(html, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(env["GMAIL_USER"], env["GMAIL_APP_PASSWORD"])
    server.send_message(msg)
print(f"sent: {subject}")

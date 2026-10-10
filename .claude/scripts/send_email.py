#!/usr/bin/env python3
"""Send a markdown file as an HTML email via Gmail.
Usage: python3 send_email.py "Subject line" path/to/file.md
"""
import os, smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import markdown

env = dict(os.environ)  # GitHub Actions secrets arrive here
env_file = Path(__file__).parent / ".env"  # optional, local testing only
for line in (env_file.read_text().splitlines() if env_file.exists() else []):
    if "=" in line and not line.strip().startswith("#"):
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip()

subject, path = sys.argv[1], Path(sys.argv[2])
body = path.read_text(errors="replace")[-200000:]

msg = MIMEMultipart("alternative")
msg["Subject"] = subject
msg["From"] = env["GMAIL_USER"]
msg["To"] = env["EMAIL_TO"]
msg.attach(MIMEText(body, "plain"))
style = "font-family:-apple-system,Helvetica,sans-serif;font-size:15px;line-height:1.5;max-width:680px"
msg.attach(MIMEText(f'<div style="{style}">{markdown.markdown(body)}</div>', "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(env["GMAIL_USER"], env["GMAIL_APP_PASSWORD"])
    server.send_message(msg)
print(f"sent: {subject}")

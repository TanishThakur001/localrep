import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import psutil
import time
from flask import Flask, render_template

app = Flask(__name__)

EMAIL_ADDRESS = "tanishthakur131@gmail.com"
EMAIL_PASSWORD = "zqbj dhcb gehl imzy"
RECEIVER_EMAIL = "tanishthakur131@gmail.com"

def send_alert(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email alert sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)

boot_time = time.time() - psutil.boot_time()

@app.route("/")
def index():

    cpu_percent = psutil.cpu_percent(interval=1)

    mem = psutil.virtual_memory()
    mem_percent = mem.percent

    disk = psutil.disk_usage('/')
    disk_percent = disk.percent

    swap = psutil.swap_memory()
    swap_percent = swap.percent

    processes = len(psutil.pids())

    net = psutil.net_io_counters()

    bytes_sent = round(net.bytes_sent / (1024 * 1024), 2)
    bytes_recv = round(net.bytes_recv / (1024 * 1024), 2)

    uptime = round((time.time() - psutil.boot_time()) / 3600, 2)

    Message = None

    print("Reached alert check")

    if cpu_percent > 1 or mem_percent > 1:
        print("Calling send_alert()")

        Message = "High resource utilization detected. Scale UP"

        send_alert(
        "⚠ Azure VM Alert",
        f"""
CPU Usage: {cpu_percent}%

Memory Usage: {mem_percent}%

Disk Usage: {disk_percent}%

The VM has crossed the configured threshold.
"""
    )

    return render_template(
        "index.html",
        cpu_metric=cpu_percent,
        mem_metric=mem_percent,
        disk_metric=disk_percent,
        swap_metric=swap_percent,
        processes=processes,
        sent=bytes_sent,
        recv=bytes_recv,
        uptime=uptime,
        message=Message
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
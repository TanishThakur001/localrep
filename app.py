import psutil
import time
from flask import Flask, render_template

app = Flask(__name__)

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

    if cpu_percent > 80 or mem_percent > 80:
        Message = "High resource utilization detected. Scale UP"

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
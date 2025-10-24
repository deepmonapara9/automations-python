import psutil
import time


def check_system_health():
    print("🔍 Checking system health...\n")
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    battery = psutil.sensors_battery()

    print(f"CPU Usage: {cpu}%")
    print(f"Memory Usage: {memory}%")
    print(f"Disk Usage: {disk}%")
    if battery:
        print(
            f"Battery: {battery.percent}% {'(Charging)' if battery.power_plugged else '(On Battery)'}"
        )

    # Simple alert
    if cpu > 80 or memory > 80 or disk > 85:
        print("⚠️ Warning: High resource usage detected!")


if __name__ == "__main__":
    while True:
        check_system_health()
        print("-" * 30)
        time.sleep(10)

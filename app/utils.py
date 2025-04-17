import time
import asyncio

async def write_log(message: str):
    print(f"--- Background Task Log Start ---")
    await asyncio.sleep(2)
    with open("log.txt", "a") as log_file:
        log_file.write(f"{time.ctime()}: {message}\n")
    print(f"Logged: {message}")

async def send_email(email: str, message: str):
    print(f"--- Background Task Email Start ---")
    await asyncio.sleep(2)
    print(f"Email sent to {email}, message: {message}")

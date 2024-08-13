import asyncio
import subprocess

async def run_file(file):
    process = await asyncio.create_subprocess_exec(
        'python', file,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if stdout:
        print(f'{file} output:\n{stdout.decode()}')
    if stderr:
        print(f'{file} error:\n{stderr.decode()}')

async def main():
    await asyncio.gather(
        run_file('web.py'),
        run_file('bot.py')
    )

asyncio.run(main())
import subprocess
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass


@dataclass(frozen=True)
class Result:
    status: int
    stdout: str
    stderr: str


def run(script: str) -> Result:
    process = subprocess.Popen(
        ["docker", "run", "-i", "--rm", "python:3.13-slim", "python", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        stdout, stderr = process.communicate(input=script.encode(), timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
    return Result(
        status=process.returncode,
        stdout=stdout.decode(),
        stderr=stderr.decode(),
    )


def run_batch(scripts: list[str]) -> list[Result]:
    with ProcessPoolExecutor() as executor:
        return [*executor.map(run, scripts)]

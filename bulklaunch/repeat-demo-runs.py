import os
import re
import json
import asyncio
import datetime
import time
import subprocess
import urllib.error

import conducto as co


def run_pipe(logsdir, cmd):
    os.mkdir(logsdir)

    proc = subprocess.run(cmd, capture_output=True)

    if proc.returncode:
        return

    contents = proc.stdout.decode("utf-8")
    # print(contents)

    # search for the view-at-conduc.to url
    m = re.search(r"http[:/.a-z0-9A-Z]+/([a-zA-Z0-9]{3}-[a-zA-Z0-9]{3})", contents)

    print("*** Pipeline Launched ***")
    print(m.group(0))

    pipeid = m.group(1)

    with open(os.path.join(logsdir, "pipeline.txt"), "w") as f1:
        f1.write(pipeid)

    pipedict = None
    with open(os.path.join(logsdir, "progress.txt"), "w") as f2:
        while True:
            time.sleep(15)

            try:
                pipedict = co.api.Pipeline().get(pipeid)
            except co.api.InvalidResponse as e:
                f2.write(f"Pipeline service error {str(e)}\n")
                f2.flush()
                continue
            except urllib.error.URLError as e:
                f2.write(f"Pipeline status check network error {str(e)}\n")
                f2.flush()
                continue

            f2.write(f"{datetime.datetime.utcnow()}:  {pipedict['meta']['state']}\n")
            f2.write(json.dumps(pipedict["meta"]["stateCounts"]))
            f2.write("\n")
            f2.flush()

            if pipedict["meta"]["state"] in ("error", "done"):
                break

    if pipedict and pipedict["meta"]["state"] == "error":
        cmd2 = [
            "python",
            f"{os.environ['CONDUCTO_SUPER']}/private/infra/utils/bin/logs.py",
            "-e",
            "test",
            "-s",
            "manager",
            "-p",
            pipeid,
            "--start",
            "30min",
        ]

        p2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        with open(os.path.join(logsdir, "manager.log"), "wb") as f3:
            f3.write(p2.stdout)

    slept = False

    # sleep an active pipeline *not* in standby mode via websocket connection
    async def chat_with_server():
        nonlocal slept, pipeid
        websocket = await co.api.connect_to_pipeline(pipeid)

        await websocket.send(json.dumps({"type": "CLOSE_PROGRAM", "payload": None}))
        async for msg in websocket:
            obj = json.loads(msg)
            if obj["type"] == "SLEEP":
                slept = True

    print("putting the pipeline to sleep")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(chat_with_server())
    finally:
        pass

    print(f"all done with {pipeid}")

    return slept


def main():
    mydir = os.path.dirname(os.path.normpath(__file__))

    while True:
        initial = datetime.datetime.utcnow()

        print("Running cicd demo")
        looplogs = os.path.join(
            mydir, "log-cicd-full", str(datetime.datetime.utcnow()).replace(" ", "T")
        )
        cmd = [
            "python",
            "demo/cicd/full_demo.py",
            "--cloud",
            "--run",
        ]
        run_pipe(looplogs, cmd)

        final = datetime.datetime.utcnow()
        nexttime = initial + datetime.timedelta(minutes=30)
        pause = nexttime - final

        if pause.total_seconds() > 0:
            time.sleep(pause.total_seconds())


if __name__ == "__main__":
    main()

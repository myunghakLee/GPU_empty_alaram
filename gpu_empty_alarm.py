# -*- coding: utf-8 -*-
# +
from email.mime.text import MIMEText
import subprocess
import argparse
import smtplib
import time
import json

    
parser = argparse.ArgumentParser()
parser.add_argument('--sleep_time', type=int, default=900, help = "GPU Usage Measurement Cycle")
parser.add_argument('--gpu_id', default=[0], type=int, nargs='+', help = "Number of Used GPU")
parser.add_argument('--it', type=int, default=5, help = "Number of measurements")

parser.add_argument('--memory_usage', type=int, default=5, help = "The memory usage threshold for sending mail.")
parser.add_argument('--memory_utill', type=int, default=5, help = "The memory utill threshold for sending mail.")

parser.add_argument('--ID_s', type=str, required=True, help = "ID of the email to be sent")
parser.add_argument('--PW_s', type=str, required=True, help = "PW of the email to be sent")
parser.add_argument('--ID_r', type=str, required=True, help = "ID of the email to be sent")

gpu_num = len(args.gpu_id)

DEFAULT_ATTRIBUTES = (
    'index',
    'timestamp',
    'memory.total',
    'memory.free',
    'memory.used',
    'utilization.gpu',
    'utilization.memory',
    'temperature.gpu',
    'name'
)

def get_process()
    process = subprocess.check_output("ps -auxww $$",shell=True,executable="/bin/bash")
    process = str(process.decode())
    process_list = []
    for p in process.split("\n"):
        if 'python' in p and '.py ' in p:
            command = p[p.find("python"):]
            if "python /" in command:
                continue
            process_list.append(command)
    return process_list
    
def get_gpu_info(nvidia_smi_path='nvidia-smi', keys=DEFAULT_ATTRIBUTES, no_units=True):
    nu_opt = '' if not no_units else ',nounits'
    cmd = '%s --query-gpu=%s --format=csv,noheader%s' % (nvidia_smi_path, ','.join(keys), nu_opt)
    output = subprocess.check_output(cmd, shell=True)
    lines = output.decode().split('\n')
    lines = [ line.strip() for line in lines if line.strip() != '' ]
    info = [{k: v for k, v in zip(keys, line.split(', ')) } for line in lines]
    info = sorted(info, key=lambda a:int(a['index']))
    return info

def main(args):

    info = get_gpu_info()
    info = [A[i] for i in args.gpu_id]
    gpu_name = info[0]['name']

    while(True):
        try:
            print("GPU is Not Empty")
            memory_used, utilization, temperature = 0, 0, 0
            
            for _ in range(args.it):
                info = get_gpu_info()
                info = [info[i] for i in args.gpu_id]  # get gpu info that you selected

                memory_used += sum([float(d['memory.used']) for d in A]) / gpu_num
                utilization += sum([float(d['utilization.gpu']) for d in A]) / gpu_num
                temperature += sum([float(d['temperature.gpu']) for d in A]) / gpu_num
                time.sleep(3)  # get gpu info every 3 second.

            memory_used /= args.it
            utilization /= args.it
            temperature /= args.it

            print(f"memory_used : {memory_used}")
            print(f"utilization : {utilization}")
            print(f"temperature : {temperature}")

            if memory_used < args.memory_used and utilization < args.memory_utill:
                break

            time.sleep(args.sleep_time)

        except KeyboardInterrupt:
            break

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    print("login")
    s.login(args.ID_s, args.PW_s)

    title = f"The GPU device is empty. {gpu_name}"
    content = f'GPU name : {gpu_name}\n'
    content = f'GPU id : {args.gpu_id}\n'
    content += f'GPU memory_used : {[int(d["memory.used"]) for d in A]}\n'
    content += f'GPU utilization : {[int(d["utilization.gpu"]) for d in A]}\n'
    content += f'GPU temperature : {[int(d["temperature.gpu"]) for d in A]}\n'
    content += f'\n' * 3
    content += f'process\n'

    process_list = get_process()
    for p in process_list:
        content += f"{p}\n"

    msg = MIMEText(content)
    msg['Subject'] = title

    print("Send mail!!!")
    print("title : ", title)
    print("content : ", content)
    s.sendmail(args.ID_s, args.ID_r, msg.as_string())
    
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

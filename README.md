# GPU_empty_alaram

<p>This code is a code that sends mail when gpu usage falls below a certain level on a server (or personal computer).</p>

<p>It is expected to be useful for machine learning developers to check whether their experiments have been completed.</p>
<br />
<br />

## MAKE ID

To send mail, you need to set up a gmail account.

You should set up "2-step verification" through the link below.
https://myaccount.google.com/security

After that, you need to create a password using "App password created".

<img width="876" alt="image" src="https://user-images.githubusercontent.com/12128784/216520898-1c915b4f-df49-4747-af8b-562de488b7db.png">
<br />
<br />

## usage
```
python gpu_empty_alarm.py --gpu_id 0 1 2 --memory_usage 5000 --memory_utill 50 \
--ID_s [Your E-mail address] --PW_s [Your E-mail PW] --ID_r [Your ID for receive mail]
```

<p>You have to change memory_usage and memory_utill</p>
<p><em>memory_usage</em> : GPU memory in use</p>
<p><em>memory_utill</em> : GPU Utilization</p>

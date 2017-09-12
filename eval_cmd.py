import subprocess
from os import path

import discord


chroot_dir = path.join(path.dirname(path.abspath(__file__)), 'chroot')
MB = 1024 * 1024

def eval_cmd(client, message, args):
	proc_args = ['nsjail', '-Mo', '--chroot', chroot_dir, '-E', 'LANG=en_US.UTF-8',
			'-R/usr', '-R/lib', '-R/lib64', '--user', 'nobody', '--group', 'nogroup',
			'--time_limit', '2', '--disable_proc', '--iface_no_lo',
			'--cgroup_mem_max', str(50 * MB), '--quiet', '--',
			'/usr/bin/python3', '-ISq', '-c', prep_input(args)]

	proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
			stderr=subprocess.PIPE, universal_newlines=True)
	stdout, stderr = proc.communicate()

	output = 'Unknown error'

	if proc.returncode == 0:
		output = stdout
	elif proc.returncode == 1:
		try:
			output = stderr.split('\n')[-2]
		except IndexError:
			output = ''
	elif proc.returncode == 109:
		output = 'Timed out or memory limit exceeded'

	return discord.embed(title='Result', description=output, color=3447003)
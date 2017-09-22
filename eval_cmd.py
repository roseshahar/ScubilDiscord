import subprocess
from os import path

import discord


chroot_dir = path.join(path.dirname(path.abspath(__file__)), 'chroot')
MB = 1024 * 1024


def prep_input(args):
	args = args.lstrip()
	if args.startswith('```') and args.endswith('```'):
		split = args[3:].split('\n', 1)
		if len(split) == 2:
			language, other_lines = args[3:].split('\n', 1)
			if language == 'python':
				return other_lines[:-3]
	return args.strip('`').strip()


def eval_cmd(client, message, args):
	#print(prep_input(args))
	proc_args = ['../nsjail/nsjail', '-Mo', '--chroot', chroot_dir, '-E', 'LANG=en_US.UTF-8',
			'-R/usr', '-R/lib', '-R/lib64', '--user', 'nobody',
			'--time_limit', '2', '--disable_proc', '--iface_no_lo',
			'--cgroup_mem_max', str(50 * MB), '--quiet', '--',
			'/usr/bin/python3', '-ISq']

	proc = subprocess.Popen(proc_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
			stderr=subprocess.PIPE, universal_newlines=True)
	stdout, stderr = proc.communicate(prep_input(args) + '\n')

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

	#print(output)

	return discord.Embed(title='Result', description=output[:200], color=3447003)
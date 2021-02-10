#!/usr/bin/python
#
# Tracing syscalls by using BPF_PERF_OUTPUT.

from bcc import BPF
import sys

def usage():
    print("Usage: {0} <syscall>".format(sys.argv[0]))
    print("e.g.: {0} mkdir\n".format(sys.argv[0]))
    exit(1)

if len(sys.argv) != 2:
    usage()
    exit(1)

# define BPF program
prog = """
#include <linux/sched.h>

// define output data structure in C
struct data_t {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
};
BPF_PERF_OUTPUT(events);

int hello(struct pt_regs *ctx) {
    struct data_t data = {};

    data.pid = bpf_get_current_pid_tgid();
    data.ts = bpf_ktime_get_ns();
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    events.perf_submit(ctx, &data, sizeof(data));

    return 0;
}
"""

system_call = sys.argv[1]

# load BPF program
b = BPF(text=prog)
b.attach_kprobe(event=b.get_syscall_fnname(system_call), fn_name="hello")

# header
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "MESSAGE"))

# process event
start = 0
def print_event(cpu, data, size):
    global start
    event = b["events"].event(data)
    if start == 0:
            start = event.ts
    time_s = (float(event.ts - start)) / 1000000000
    print("%-18.9f %-16s %-6d %s" % (time_s, event.comm, event.pid,
        system_call + " Syscall invoked"))

# loop with callback to print_event
b["events"].open_perf_buffer(print_event)
while 1:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
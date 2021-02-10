# Trace Syscall example

Usage: trace_syscall.py <syscall>
e.g.: trace_syscall.py mkdir

In this example we'll trace a particular syscall. The syscall name can be parameterized.

## Setup

We need to run a docker image.

```
docker run -it --rm --privileged -v /lib/modules:/lib/modules:ro -v /usr/src:/usr/src:ro -v /etc/localtime:/etc/localtime:ro --workdir /usr/share/bcc/tools zlim/bcc
```

Then we'll need to copy the needed files or mount a volume for consuming them.

```
docker cp trace_syscall.py  <container_name>:/usr/share/bcc/examples/
docker cp mkdir_script.sh  <container_name>:/usr/share/bcc/examples/
```

On the running docker container terminal run

```
root@77ec0687d623:/usr/share/bcc/examples# chmod +x trace_syscall.py
root@77ec0687d623:/usr/share/bcc/examples# python trace_syscall.py mkdir
```

You should see output like

```
0.000000000        systemd-journal  556    mkdir Syscall invoked
0.000059278        systemd-journal  556    mkdir Syscall invoked
0.362536467        systemd-journal  556    mkdir Syscall invoked
0.362550343        systemd-journal  556    mkdir Syscall invoked
0.363447059        systemd-journal  556    mkdir Syscall invoked
0.363456598        systemd-journal  556    mkdir Syscall invoked
0.465168666        systemd-journal  556    mkdir Syscall invoked
0.465181098        systemd-journal  556    mkdir Syscall invoked
0.466175321        systemd-journal  556    mkdir Syscall invoked
0.466185130        systemd-journal  556    mkdir Syscall invoked
3.423365697        systemd-journal  556    mkdir Syscall invoked
3.423387067        systemd-journal  556    mkdir Syscall invoked
3.424193432        systemd-journal  556    mkdir Syscall invoked
3.424201412        systemd-journal  556    mkdir Syscall invoked
6.459053161        systemd-journal  556    mkdir Syscall invoked
6.459065604        systemd-journal  556    mkdir Syscall invoked
6.459912664        systemd-journal  556    mkdir Syscall invoked
6.459921583        systemd-journal  556    mkdir Syscall invoked
```

On a different terminal run

```
docker exec -it <container_name> /bin/bash
root@77ec0687d623:/usr/share/bcc/examples# chmod +x mkdir_script.sh
root@77ec0687d623:/usr/share/bcc/examples# ./mkdir_script.sh
```

Get back to the original docker container terminal and you should see:

```
20.475619649       mkdir            24445  mkdir Syscall invoked
20.477075177       mkdir            24446  mkdir Syscall invoked
20.478946454       mkdir            24447  mkdir Syscall invoked
```

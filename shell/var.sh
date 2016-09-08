#!/bin/sh

echo "shell process ID is $$"
echo "exit status of last cmd is $?"
echo "all args are $@"

./sub.sh
echo "name of last cmd is $_"

echo "process ID of last cmd in background is $!"

echo "$IFS"

echo "$HOME $UID $USER"

echo "number of args is $#"

echo "$* || $-"

echo "$PWD"

cmd="$1"
shift

echo "cmd is $cmd , remaining args are $@" 
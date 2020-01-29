#!/usr/bin/env bash
# shellcheck disable=SC2046
echo "You'll need to enter pi password twice, it's normal"

ssh pi@frcvision.local ./rmvision.sh
scp -r $(pwd) pi@frcvision.local:~/vision


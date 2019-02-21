#!/usr/bin/env bash
git branch -r | awk -F/ '/\/pyup-update-/{print $2}' | xargs -I {} git push origin :{}

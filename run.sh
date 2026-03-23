#!/usr/bin/env bash
# Simple runner for the ETL
set -e
cd "$(dirname "$0")"
python3 -m etl.main

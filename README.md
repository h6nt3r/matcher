## Overview
This Python tool reads a list of URLs, finds specific query parameters by name, and replaces their values with a given replacement string.  
It is designed for situations like:
- Sanitizing sensitive data from recon dumps (API keys, tokens, session IDs).
- Preparing URLs for sharing in bug bounty or pentest reports.
- Filtering or inverting selection of URLs based on query parameter keys.

## Usage
output parameter also remove port numbers
```
match -f urls.txt -r "*" -R -m payloads.txt -o output.txt
```
stdio mode usage
```
cat urls.txt | match -r "FUZZ" -R -m payloads.txt -o output.txt
```
## installations
```
cd /opt/ && sudo git clone https://github.com/h6nt3r/matcher.git
cd
sudo chmod +x /opt/matcher/match.py
sudo ln -sf /opt/matcher/match.py /usr/local/bin/match
match -h
```
## Options
```
match -h
usage: match [-h] [-f FILE] -r REPLACEMENT [-R] [-i] [-m MATCHER_LIST] [-c] [-d] [-s] [-o OUTPUT]

Parameters Matcher. current version: 1.0.2

options:
  -h, --help            show this help message and exit
  -f, --file FILE       Input file containing URLs. Defaults to stdin.
  -r, --replacement REPLACEMENT
                        Replacement text for matched query parameter values.
  -R, --remove-ports    Remove port numbers from URLs.
  -i, --invert-match    Invert the match to exclude URLs containing the matcher keys.
  -m, --matcher-list MATCHER_LIST
                        File containing list of matchers, one per line.
  -c, --case-insensitive
                        Case-insensitive matching of parameter names.
  -d, --delete-after    Delete all query parameters after the matched parameter (requires -m).
  -s, --silent          Silent mode: print only URLs in terminal, even with output file.
  -o, --output OUTPUT   Output file to save matching URLs.
```

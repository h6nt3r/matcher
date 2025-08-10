## Overview
This Python tool reads a list of URLs, finds specific query parameters by name, and replaces their values with a given replacement string.  
It is designed for situations like:
- Sanitizing sensitive data from recon dumps (API keys, tokens, session IDs).
- Preparing URLs for sharing in bug bounty or pentest reports.
- Filtering or inverting selection of URLs based on query parameter keys.

It supports:
- Case-sensitive or case-insensitive parameter matching.
- Optional port number removal from URLs.
- Inverted matching (keep URLs that **don’t** match).
- Verbose output for debugging.
- Reading matchers and URLs from files or stdin.

---

## Features
- **Parameter Name Matching**: Replace the value of parameters whose name matches entries from a matcher file.
- **Case-Insensitive Matching**: Match parameter names regardless of letter case (`token`, `TOKEN`, `ToKeN` all match).
- **Invert Match**: Keep only URLs that do **not** contain the specified parameters.
- **Remove Ports**: Strip port numbers (e.g., `:8080`) from URLs.
- **File or Stdin Input**: Read URLs from a file or directly from standard input.
- **Output to File or Stdout**: Save processed URLs to a file or print them directly.
- **Verbose Mode**: Print detailed info about matching and replacements.

---

## Usage
output parameter also remove port numbers
```
match -f urls.txt -r "*" -R -m payloads.txt -o parameter_outputs.txt
```
stdio mode usage
```
cat urls.txt | match -r "FUZZ" -R -m payloads.txt -o parameter_outputs.txt
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
usage: match [-h] [-f FILE] [-o OUTPUT] -r REPLACEMENT [-R] [-i] [-m MATCHER_LIST] [-v] [-c]

Grep URLs with optional port removal, inverted matching, and verbose output.

options:
  -h, --help            show this help message and exit
  -f, --file FILE       Input file containing URLs. Defaults to stdin.
  -o, --output OUTPUT   Output file to save matching URLs.
  -r, --replacement REPLACEMENT
                        Replacement text for matched query parameter values.
  -R, --remove-ports    Remove port numbers from URLs.
  -i, --invert-match    Invert the match to exclude URLs containing the matcher keys.
  -m, --matcher-list MATCHER_LIST
                        File containing list of matchers, one per line.
  -v, --verbose         Enable verbose mode for more detailed output.
  -c, --case-insensitive
                        Case-insensitive matching of parameter names.
```

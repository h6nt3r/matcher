## Usage
output parameter also remove port numbers
```
match -f urls.txt -p "=" -r -v -o parameter_outputs.txt
```
stdio mode usage
```
cat urls.txt | match -p "=" -r -v -o parameter_outputs.txt
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
usage: match [-h] [-f FILE] [-o OUTPUT] -p PLACEHOLDER [-r] [-i] [-v]

Grep URLs with optional port removal, inverted matching, and verbose output.

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input file containing URLs. Defaults to stdin.
  -o OUTPUT, --output OUTPUT
                        Output file to save matching URLs.
  -p PLACEHOLDER, --placeholder PLACEHOLDER
                        Placeholder text to search for in the URLs.
  -r, --remove-ports    Remove port numbers from URLs.
  -i, --invert-match    Invert the match to exclude URLs containing the placeholder.
  -v, --verbose         Enable verbose mode for more detailed output.
```

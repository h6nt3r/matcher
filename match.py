#!/usr/bin/env python3
import argparse
import sys
import re

def remove_port(url):
    return re.sub(r':\d{1,5}', '', url)

def grep_urls(file, placeholder, output, remove_ports, invert_match, verbose):
    matching_urls = []
    for line in file:
        url = line.strip()
        contains_placeholder = placeholder in url

        if invert_match:
            condition = not contains_placeholder
        else:
            condition = contains_placeholder

        if condition:
            if remove_ports:
                url = remove_port(url)
            matching_urls.append(url)
            if verbose:
                print(f"Matched URL: {url}")

    if output:
        if verbose:
            print(f"Saving results to {output}")
        with open(output, 'w') as f:
            for url in matching_urls:
                f.write(url + '\n')
    else:
        for url in matching_urls:
            print(url)

def main():
    parser = argparse.ArgumentParser(description="Grep URLs with optional port removal, inverted matching, and verbose output.")
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), default=sys.stdin,
                        help="Input file containing URLs. Defaults to stdin.")
    parser.add_argument('-o', '--output', type=str, help="Output file to save matching URLs.")
    parser.add_argument('-p', '--placeholder', type=str, required=True,
                        help="Placeholder text to search for in the URLs.")
    parser.add_argument('-r', '--remove-ports', action='store_true',
                        help="Remove port numbers from URLs.")
    parser.add_argument('-i', '--invert-match', action='store_true',
                        help="Invert the match to exclude URLs containing the placeholder.")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Enable verbose mode for more detailed output.")
    
    args = parser.parse_args()

    grep_urls(args.file, args.placeholder, args.output, args.remove_ports, args.invert_match, args.verbose)

if __name__ == "__main__":
    main()

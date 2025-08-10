#!/usr/bin/env python3
import argparse
import sys
import re
from urllib.parse import urlparse, parse_qsl, urlunparse

def remove_port(url):
    return re.sub(r':\d{1,5}', '', url)

def grep_urls(file, replacement, matcher_file, output, remove_ports, invert_match, verbose, case_insensitive):
    # Load matchers from file
    matchers = []
    if matcher_file:
        matchers.extend([line.strip() for line in matcher_file if line.strip()])

    matching_urls = []
    for line in file:
        url = line.strip()

        parsed = urlparse(url)
        query_params = parse_qsl(parsed.query, keep_blank_values=True)

        matched = False
        new_params = []

        for key, value in query_params:
            if case_insensitive:
                key_match = any(m.lower() == key.lower() for m in matchers)
            else:
                key_match = key in matchers

            if key_match:
                matched = True
                new_params.append((key, replacement))  # Replace value
            else:
                new_params.append((key, value))

        # Decide keep or skip
        if invert_match:
            condition = not matched
        else:
            condition = matched

        if condition:
            # Rebuild query without URL encoding '*'
            new_query = "&".join([f"{k}={v}" for k, v in new_params])

            # Rebuild full URL
            new_url = urlunparse(parsed._replace(query=new_query))

            if remove_ports:
                new_url = remove_port(new_url)

            matching_urls.append(new_url)
            if verbose:
                print(f"Matched and replaced URL: {new_url}")

    # Output
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
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), default=sys.stdin, help="Input file containing URLs. Defaults to stdin.")
    parser.add_argument('-o', '--output', type=str, help="Output file to save matching URLs.")
    parser.add_argument('-r', '--replacement', type=str, required=True, help="Replacement text for matched query parameter values.")
    parser.add_argument('-R', '--remove-ports', action='store_true', help="Remove port numbers from URLs.")
    parser.add_argument('-i', '--invert-match', action='store_true', help="Invert the match to exclude URLs containing the matcher keys.")
    parser.add_argument('-m', '--matcher-list', type=argparse.FileType('r'), help="File containing list of matchers, one per line.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose mode for more detailed output.")
    parser.add_argument('-c', '--case-insensitive', action='store_true', help="Case-insensitive matching of parameter names.")
    
    args = parser.parse_args()

    grep_urls(args.file, args.replacement, args.matcher_list, args.output, args.remove_ports, args.invert_match, args.verbose, args.case_insensitive)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import argparse
import sys
import re
from urllib.parse import urlparse, parse_qsl, urlunparse

def remove_port(url):
    return re.sub(r':\d{1,5}', '', url)

def grep_urls(file, single_url, replacement, matcher_file, output, remove_ports, invert_match, case_insensitive, delete_after, silent_mode):
    # Check if -m is provided when -d is used
    if delete_after and not matcher_file:
        print("Error: -d flag requires -m flag to specify matchers.")
        sys.exit(1)

    # Check if both -f and -u are provided
    if file != sys.stdin and single_url:
        print("Error: Cannot use both -f and -u flags together.")
        sys.exit(1)

    # Load matchers from file
    matchers = []
    if matcher_file:
        try:
            matchers.extend([line.strip() for line in matcher_file if line.strip()])
        except UnicodeDecodeError:
            print("Error: Failed to decode matcher file. Ensure it is UTF-8 encoded.")
            sys.exit(1)

    # Prepare URLs list
    all_urls = []
    error_count = 0
    if single_url:
        all_urls = [single_url]
    else:
        try:
            for line in file:
                try:
                    cleaned_line = line.decode('utf-8', errors='ignore') if isinstance(line, bytes) else line
                    if cleaned_line.strip():
                        all_urls.append(cleaned_line.strip())
                except UnicodeDecodeError:
                    error_count += 1
        except Exception:
            error_count += 1

    total_urls = len(all_urls)

    matching_urls = []
    for index, url in enumerate(all_urls, 1):
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ValueError("Invalid URL")
            
            query_params = parse_qsl(parsed.query, keep_blank_values=True)

            matched = False
            new_params = []

            for i, (key, value) in enumerate(query_params):
                param_string = f"?{key}="
                if case_insensitive:
                    key_match = any(m.lower() == param_string.lower() for m in matchers)
                else:
                    key_match = param_string in matchers

                if key_match:
                    matched = True
                    new_params.append((key, replacement))
                    if delete_after:
                        break
                else:
                    new_params.append((key, value))

            if (invert_match and not matched) or (not invert_match and (matched or not matchers)):
                new_query = "&".join([f"{k}={v}" for k, v in new_params])
                new_url = urlunparse(parsed._replace(query=new_query))

                if remove_ports:
                    new_url = remove_port(new_url)

                matching_urls.append(new_url)
                if silent_mode:
                    print(new_url)
                else:
                    print(f"URL({index}/{total_urls}): {new_url}")

        except (ValueError, Exception):
            error_count += 1

    if not silent_mode:
        print(f"Total Url Matches: {len(matching_urls)}")
        print(f"Total Error: {error_count}")

    if output:
        with open(output, 'w', encoding='utf-8') as f:
            for url in matching_urls:
                f.write(url + '\n')

def main():
    parser = argparse.ArgumentParser(description="Parameters Matcher. current version: 1.0.3")
    parser.add_argument('-u', '--url', type=str, help="Single URL to scan.")
    parser.add_argument('-f', '--file', type=argparse.FileType('r', encoding='utf-8', errors='ignore'), default=sys.stdin, help="Input file containing URLs. Defaults to stdin.")
    parser.add_argument('-r', '--replacement', type=str, required=True, help="Replacement text for matched query parameter values.")
    parser.add_argument('-R', '--remove-ports', action='store_true', help="Remove port numbers from URLs.")
    parser.add_argument('-i', '--invert-match', action='store_true', help="Invert the match to exclude URLs containing the matcher keys.")
    parser.add_argument('-m', '--matcher-list', type=argparse.FileType('r', encoding='utf-8', errors='ignore'), help="File containing list of matchers, one per line.")
    parser.add_argument('-c', '--case-insensitive', action='store_true', help="Case-insensitive matching of parameter names.")
    parser.add_argument('-d', '--delete-after', action='store_true', help="Delete all query parameters after the matched parameter (requires -m).")
    parser.add_argument('-s', '--silent', action='store_true', help="Silent mode: print only URLs in terminal, even with output file.")
    parser.add_argument('-o', '--output', type=str, help="Output file to save matching URLs.")

    args = parser.parse_args()

    grep_urls(args.file, args.url, args.replacement, args.matcher_list, args.output, args.remove_ports, args.invert_match, args.case_insensitive, args.delete_after, args.silent)

if __name__ == "__main__":
    main()
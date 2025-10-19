#!/usr/bin/env python3
import argparse
import sys
import re
from urllib.parse import urlparse, parse_qsl, urlunparse

def remove_port(url):
    return re.sub(r':\d{1,5}', '', url)

def grep_urls(file, replacement, matcher_file, output, remove_ports, invert_match, case_insensitive, delete_after, silent_mode):
    # Check if -m is provided when -d is used
    if delete_after and not matcher_file:
        print("Error: -d flag requires -m flag to specify matchers.")
        sys.exit(1)

    # Load matchers from file
    matchers = []
    if matcher_file:
        try:
            matchers.extend([line.strip() for line in matcher_file if line.strip()])
        except UnicodeDecodeError:
            print("Error: Failed to decode matcher file. Ensure it is UTF-8 encoded.")
            sys.exit(1)

    # Read all URLs to count total, handling encoding errors
    all_urls = []
    error_count = 0
    try:
        for line in file:
            try:
                # Decode line with 'ignore' to skip invalid characters
                cleaned_line = line.decode('utf-8', errors='ignore') if isinstance(line, bytes) else line
                if cleaned_line.strip():
                    all_urls.append(cleaned_line.strip())
            except UnicodeDecodeError:
                error_count += 1  # Silently skip encoding errors
    except Exception:
        error_count += 1  # Silently skip any other errors

    total_urls = len(all_urls)

    matching_urls = []
    for index, url in enumerate(all_urls, 1):
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:  # Basic URL validation
                raise ValueError("Invalid URL")
            
            query_params = parse_qsl(parsed.query, keep_blank_values=True)

            matched = False
            new_params = []

            for i, (key, value) in enumerate(query_params):
                if case_insensitive:
                    key_match = any(m.lower() == key.lower() for m in matchers)
                else:
                    key_match = key in matchers

                if key_match:
                    matched = True
                    new_params.append((key, replacement))  # Replace value
                    # If -d flag is used, stop adding parameters after this match
                    if delete_after:
                        break
                else:
                    new_params.append((key, value))

            # Decide keep or skip
            if invert_match:
                condition = not matched
            else:
                condition = matched or not matchers  # If no matchers, process all URLs

            if condition:
                # Rebuild query without URL encoding '*'
                new_query = "&".join([f"{k}={v}" for k, v in new_params])

                # Rebuild full URL
                new_url = urlunparse(parsed._replace(query=new_query))

                if remove_ports:
                    new_url = remove_port(new_url)

                matching_urls.append(new_url)
                if silent_mode:
                    print(new_url)  # Print only URLs in silent mode
                else:
                    print(f"URL({index}/{total_urls}): {new_url}")  # Print verbose if not silent

        except (ValueError, Exception):
            error_count += 1  # Silently skip errors

    # Print summary in verbose mode
    if not silent_mode:
        print(f"Total Url Matches: {len(matching_urls)}")
        print(f"Total Error: {error_count}")

    # Output to file
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            for url in matching_urls:
                f.write(url + '\n')  # Always save only URLs to file

def main():
    parser = argparse.ArgumentParser(description="Parameters Matcher. current version: 1.0.2")
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

    grep_urls(args.file, args.replacement, args.matcher_list, args.output, args.remove_ports, args.invert_match, args.case_insensitive, args.delete_after, args.silent)

if __name__ == "__main__":
    main()
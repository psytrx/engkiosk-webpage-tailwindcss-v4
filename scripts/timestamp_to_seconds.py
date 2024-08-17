import argparse

if __name__ == "__main__":
    cli_parser = argparse.ArgumentParser(description='Find tags without descriptions. Without `-write-file`, the tags get printed to stdout.')
    cli_parser.add_argument('timestamp',
        metavar='timestamp',
        type=str,
        default='',
        nargs='?',
        help='Timestamo in the format "HH:MM:SS"')

    args = cli_parser.parse_args()
    timestamp = args.timestamp

    ts_parts = args.timestamp.split(":")
    if len(ts_parts) == 3:
        hours = int(ts_parts[0])
        minutes = int(ts_parts[1])
        seconds = int(ts_parts[2])

        total_seconds = hours * 3600 + minutes * 60 + seconds
        print(total_seconds)

    else:
        print("Invalid timestamp format. Please provide a timestamp in the format HH:MM:SS")
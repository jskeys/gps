#!/usr/bin/env python

import argparse
import gps
import serial

if __name__ == "__main__":

    # Argument parsing
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--port", "-p", type=str, default="COM4")
    args = arg_parser.parse_args()

    connection = serial.Serial(args.port)

    gps_parser = gps.GPSParser()
    sentences = gps_parser.parse(str(connection.read(400)))
    for sentence in sentences:
        print(sentence.type)

#!/usr/bin/env python

import re

from functools import reduce
from serial import Serial


class NMEASentence:
    def __init__(self, sentence: str):

        # The last three characters should be an asterisk followed by a hexadecimal checksum. If
        # not, raise an error.
        match = re.search(r"\*([\w]{2})$", sentence)
        if match is None:
            raise ValueError("Could not extract checksum.")

        self.checksum = int(match.group(1), 16)

        # Remove checksum from sentence
        sentence = sentence.replace(match.group(), "")

        # The rest of the sentence should be comma-delimited. The first element provides the talker
        # and type. These are common to all messages so they can always be extracted. The remaining
        # fields are type-specific, so they're stored in a generic `data_fields` attribute.
        data_fields = sentence.split(",")

        self.talker = data_fields[0][0:2]
        self.type = data_fields[0][2:5]
        self.data_fields = data_fields[1:]

    def _calculate_checksum(self, string: str):
        return reduce(lambda x, y: x ^ y, bytearray(string, "utf-8"))


class GPSParser:
    def __init__(self):
        self._buffer = ""

    def parse(self, data: str):
        self._buffer += data

        # Find the start of the first message in the buffer
        sentence_start = self._buffer.find("$")
        # If '$' is not found, then there is nothing useful in the buffer, so set it to any empty
        # string. Otherwise, remove everything up to but not including the first occurence.
        if sentence_start < 0:
            self._buffer = ""
        else:
            self._buffer = self._buffer[sentence_start:]

        buffer_pointer = 0
        sentences = []
        for sentence in re.finditer(r"\$(.*?)\\r\\n", self._buffer):
            sentences.append(NMEASentence(sentence.group(1)))
            buffer_pointer = sentence.end()

        self._buffer = self._buffer[buffer_pointer:]

        return sentences

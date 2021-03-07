#!/usr/bin/env python
"""

Comp Ling II - Homework 2 - Vikram D'Mello

A simple command-line tool to read a tagged corpus of sentences, requiring the user to provide the input corpus file, three output files, and a random number seed; which then splits the sentences into three groups: training 80%, development/tuning 10%, and validation/test 10%, and finally writes these three subsets of the corpus to the specified output files.

"""

# Dependencies
import argparse
from typing import Iterator, List
import random
import re


# Preamble: Text formatting codes as dictionary
font = {
    "PURPLE": "\033[95m",
    "CYAN": "\033[96m",
    "DARKCYAN": "\033[36m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}


# UDF to read & parse tagged corpus of sentences
# The `yield` keyword in Python works like a `return`, with the difference that nstead of returning a value, it gives back - or 'yields' - a 'generator object' to the caller.


def read_tags(inputPath: str) -> Iterator[List[List[str]]]:

    print(f"\n\nReading source corpus...")

    with open(inputPath, "r") as sourceCorpus:
        sentences = []
        for eachWord in sourceCorpus:
            eachWord = eachWord.rstrip()
            if eachWord:  # Line has contents - ie, there is a word
                sentences.append(eachWord.split())
            else:  # Line is blank - ie, end-of-sentence
                yield sentences.copy()  # Save one sentence list item
                sentences.clear()  # Ready for next sentence
    # Just in case someone forgets to put a blank line at the end...
    if sentences:
        yield sentences


def main(args):

    print(
        f'\n\n{font["CYAN"]}{font["BOLD"]}*** Welcome to Corpus Splitter ***{font["END"]}'
    )
    argsDisp = str(args)
    argsDisp = re.sub("Namespace", "", argsDisp)
    print(
        f'\n\n{font["UNDERLINE"]}Your provided arguments are:{font["END"]}\n{argsDisp}'
    )

    # Note how we must use a `list()` constructor here to iterate through the contents of the `yield` generator object.
    corpus = list(read_tags(args.input))

    lenCorpus = len(corpus)
    print(
        f'\n{font["GREEN"]}Successfully read {lenCorpus:,} sentences from corpus file {font["UNDERLINE"]}{args.input}{font["END"]}\n\n'
    )

    # Seed & shuffle
    random.seed(args.seed)
    random.shuffle(corpus)

    # Identify list indices for 80% train and 90% dev
    indexSplitTrain = int(lenCorpus * 0.8)
    indexSplitDev = int(lenCorpus * 0.9)

    # Slice list sentences accordingly into three lists
    splitTrain = corpus[:indexSplitTrain]
    splitDev = corpus[indexSplitTrain:indexSplitDev]
    splitTest = corpus[indexSplitDev : len(corpus)]

    # Finally, write split lists to files

    print(f"\nWriting splits to output files...")

    # Match each output file to its list, to loop through
    splitListFiles = {
        args.train: splitTrain,
        args.dev: splitDev,
        args.test: splitTest,
    }
    cntSentSplitsAll = 0

    # Loop through each output file, matched to its list
    for key in splitListFiles:
        cntSentSplitCurr = len(splitListFiles[key])
        cntSentSplitsAll = cntSentSplitsAll + cntSentSplitCurr
        cntTokensSplitCurr = sum(len(x) for x in splitListFiles[key])
        
        with open(key, "w") as output:
            for eachLine in splitListFiles[key]:
                output.write("%s\n" % eachLine)
            print(
                f'\n{font["GREEN"]}Successfully saved {cntSentSplitCurr:,} sentences with {cntTokensSplitCurr:,} tagged words/tokens to file {font["UNDERLINE"]}{key}{font["END"]}'
            )

    print(
        f'\n{font["GREEN"]}{font["BOLD"]}...for a total of {cntSentSplitsAll:,} sentences {font["END"]}'
    )

    print(
        f'\n\n{font["CYAN"]}{font["BOLD"]}*** All done!  Thanks for using Corpus Splitter ***{font["END"]}\n'
    )


if __name__ == "__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(description="Text Corpus Splitter")

    # Define all five arguments

    parser.add_argument(
        "--seed", type=int, required=True, help="Random number generator seed"
    )

    parser.add_argument("input", help="Source corpus file name & path")

    parser.add_argument(
        "train", help="Destination training split file name & path"
    )

    parser.add_argument(
        "dev", help="Destination development/tuning split file name & path"
    )

    parser.add_argument(
        "test", help="Destination test/validation split file name & path"
    )

    # Parse arguments
    args = parser.parse_args()

    # Pass to `main()`
    main(args)

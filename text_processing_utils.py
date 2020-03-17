import string

WHITESPACE_AND_PUNCTUATION = set(string.whitespace + string.punctuation)


def get_spans_and_words(text):
    start = 0
    end = -1
    spans_and_words = []
    substring_empty = True
    for i, c in enumerate(text):
        end = i
        if c in WHITESPACE_AND_PUNCTUATION and not substring_empty:
            spans_and_words.append([(start, end), text[start:end]])
            substring_empty = True
            start = i + 1
        elif c in WHITESPACE_AND_PUNCTUATION:
            start = i + 1
        elif substring_empty:
            substring_empty = False

    return spans_and_words


if __name__ == "__main__":
    text = 'Abstract\n\nThe World Health Organization (WHO) has declared the 2019 novel coronavirus (2019-nCoV) infection outbreak a global health emergency. Currently, there is no effective anti-2019-nCoV medication. The sequence identity of the 3CL proteases of 2019-nCoV and SARS is 96%, which provides a sound foundation for structural-based drug repositioning (SBDR). Based on a SARS 3CL protease X-ray crystal structure, we construct a 3D homology structure of 2019-nCoV 3CL protease. Based on this structure and existing experimental datasets for SARS 3CL protease inhibitors, we develop an SBDR model based on machine learning and mathematics to screen 1465 drugs in the DrugBank that have been approved by the U.S. Food and Drug Administration (FDA). We found that many FDA approved drugs are potentially highly potent to 2019-nCoV.\n\n'
    print(get_spans_and_words(text))

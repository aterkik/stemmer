#!/usr/bin/env python

""" Porter's Stemming Algorithm
    ---------------------------
    The implementation of Martin Porter's stemming (reducing words to
    their roots) algorithm [1].

    Some improvements marked 'DEPARTURE' differ from the rules
    described in the published paper.  However, these departures are
    improvements and without them testing on the word samples [2]
    would fail.

    This implementation stems only lower case strings; Words should be
    forced to lower case before trying to stem them.

    [1] http://www.tartarus.org/~martin/PorterStemmer
    [2] Input: http://www.tartarus.org/~martin/voc.txt
        Corresponding output: http://www.tartarus.org/~martin/output.txt
"""

import re
class Stemmer(object):
    """ Test to count the number of VC counts where:
        V - One more consecutive vowels
        C - One or more consecutive consonants
        Note: Y is considered a consonant if it's not preceded by a vowel.
    """
    vc_count = re.compile(r'[y]?[^aeiouy]*[aeiouy][aeiou]*[^aeiou]'
                        '[^aeiouy]*').findall
    # Test for a vowel in a word
    contains_v = re.compile(r'[aeiouy]').search
    # Test for a double consonant ending
    double_c = re.compile(r'[^aeiou]{2,}$').search
    # Checks for a CVC (i.e. Consonant Vowel Consonant) ending
    ends_cvc = re.compile(r'[^aeiou][aeiouy][^aeiouwxy]$').search

    # Suffices and their corresponding replacement for step 2.
    # Indexed by the suffix's penultimate character for faster
    # checking as described in the paper.
    step2_suffix_tbl = {'a' : (
                                ('ational', 'ate'),
                                ('tional', 'tion')
                                ),
                        'c' : (
                                ('enci', 'ence'),
                                ('anci', 'ance'),
                                ),
                        'e' : (
                                ('izer', 'ize'),
                                ),
                        'l' : (
                                ('bli', 'ble'),
                                # DEPARTURE
                                # To match the published algorithm, replace the above tuple with:
                                # ('abli', 'able'),
                                ('alli', 'al'),
                                ('entli', 'ent'),
                                ('eli', 'e'),
                                ('ousli', 'ous')
                                ),
                        'o' : (
                                ('ization', 'ize'),
                                ('ation', 'ate'),
                                ('ator', 'ate')
                                ),
                        's' : (
                                ('alism', 'al'),
                                ('iveness', 'ive'),
                                ('fulness', 'ful'),
                                ('ousness', 'ous')
                                ),
                        't' : (
                                ('aliti', 'al'),
                                ('iviti', 'ive'),
                                ('biliti', 'ble')
                                ),
                        # DEPARTURE
                        # To match the published algorithm, delete the next tuple.
                        'g' : (
                                ('logi', 'log'),
                                )
                       }
	# Suffices and their corresponding replacement for step 3.
    step3_suffix_tbl = {
                        't' : (
                                ('icate', 'ic'),
                                ('iciti', 'ic')
                              ),
                        'v' : (
                                ('ative', ''),
                              ),
                        'z' : (
                                ('alize', 'al'),
                              ),
                        'a' : (
                                ('ical', 'ic'),
                              ),
                        'u' : (
                                ('ful', ''),
                              ),
                        's' : (
                                ('ness', ''),
                              )
                       }
	# Suffices and their corresponding replacement for step 4.
    step4_suffix_tbl = {
                        'a' : (
                                ('al', ''),
                              ),
                        'c' : (
                                ('ance', ''),
                                ('ence', ''),
                              ),
                        'e' : (
                                ('er', ''),
                              ),
                        'i' : (
                                ('ic', ''),
                              ),
                        'l' : (
                                ('able', ''),
                                ('ible', '')
                              ),
                        'n' : (
                                ('ant', ''),
                                ('ement', ''),
                                ('ment', ''),
                                ('ent', '')
                              ),
                        'o' : (
                                ('ou', ''),
                              ),
                        's' : (
                                ('ism', ''),
                              ),
                        't' : (
                                ('ate', ''),
                                ('iti', '')
                              ),
                        'u' : (
                                ('ous', ''),
                              ),
                        'v' : (
                                ('ive', ''),
                              ),
                        'z' : (
                                ('ize', ''),
                              )
                        }

    def __init__(self):
        """Does some basic initialization."""
        self.original_word, self.stemmed = '', ''
        self.step1b_second_rule, self.step1b_third_rule = False, False

    def m(self, word):
        """Calculates and returns the given word's
        VC measure.
        """
        return len(self.vc_count(word))

    def stem_m(self, suffix = ''):
        """Calculates and returns the stem's VC measure.  If suffix is
        given, it calculates the measure after the suffix is stripped
        from the stem.
        """
        if suffix:
            return self.m(self.rep_end(self.stemmed, suffix))
        return self.m(self.stemmed)

    def rep_end(self, word, suffix, rep = ''):
        """Given a word, replaces its ending to rep if
        the word ends with the given suffix."""
        if word.endswith(suffix):
            return word[:len(word) - len(suffix)] + rep
        return word

    def replace_end(self, suffix, rep, cond = True):
        """Replaces the stem's end to rep if the stem ends with
        suffix.
        """

        applied = False
        if cond and self.stemmed.endswith(suffix):
            self.stemmed = self.rep_end(self.stemmed, suffix, rep)
            applied = True
        return applied

    def longest_match(self, word, tbl):
        """Finds and returns the word's longest matching suffix and its
        corresponding replacement from a suffix table 'tbl'.
        """

        longest_match = ('', '')
        # The suffices are grouped according to their next-to-last
        # character for faster searching.
        try:
            penultimate_ch = word[-2]
        except IndexError:
            return longest_match

        if tbl.has_key(penultimate_ch):
            tbl = tbl[penultimate_ch]
        else:
            return longest_match
        # Now find the longest matching suffix from a single group.
        for suffix, rep in tbl:
            if word.endswith(suffix) and len(suffix) > len(longest_match[0]):
                longest_match = (suffix, rep)
        return longest_match

    def replace_ends_if(self, suffix_tbl, cond = True, m_thresh = 1):
        """Strips out the suffix of the stem according to the table given
        if cond is True and the resulting stem has a greater VC measure
        than m_thresh.
        """
        if not cond:
            return self.stemmed
        longest_match = self.longest_match(self.stemmed, suffix_tbl)
        if longest_match[0] and self.stem_m(longest_match[0]) > m_thresh:
            self.stemmed = self.rep_end(self.stemmed, longest_match[0],
                                        longest_match[1])
        return self.stemmed

    def v_in_stem(self, word, suffix = '', rep = ''):
        """Whether or not word conatins a vowel."""
        return self.contains_v(self.rep_end(word, suffix, rep))

    def stem_ends_with_dbl_cons(self):
        """Whether or not the stem ends with double consonant. """
        return self.double_c(self.stemmed)

    def stem_ends_with_cvc(self, suffix = '', rep = ''):
        """Whether or not the stem ends with doubCVC pattern.  If suffix
        is given, the check is made after suffix is replaced by rep.
        """
        new_stem = self.stemmed
        if suffix and new_stem.endswith(suffix):
            new_stem = self.rep_end(new_stem, suffix, rep)
        return self.ends_cvc(new_stem)

    def str_ends_with_char(self, word, char_list=None):
        """Checks if word ends with a character from any of those
        in char_list."""

        if char_list and len(word):
            if word[-1] in char_list:
                return True
        return False

    def remove_dbl_last_char(self, cond = True):
        """Removes doubled last charcter if there is one
        and cond is True.
        """
        if cond and self.stemmed[-2] == self.stemmed[-1]:
            self.stemmed = self.stemmed[:-1]

    def step1ab(self):
        """ Strips plurals and -ed or -ing.
        Examples:
           caresses  ->  caress
           ponies    ->  poni
           agreed    ->  agree
           disabled  ->  disable

           matting   ->  mat
           mating    ->  mate
           meetings  ->  meet
        """
        # Step 1a
        self.replace_end('sses', 'ss')
        self.replace_end('ies', 'i')
        self.replace_end('ss', 'ss')
        self.replace_end('s', '', not self.stemmed.endswith('ss') )
        # Step 1b
        if self.stemmed.endswith('eed'):
            self.replace_end('eed', 'ee', self.stem_m('eed') > 0)
        elif self.stemmed.endswith('ed'):
            self.step1b_second_rule = self.replace_end('ed', '',
                                        self.v_in_stem(self.stemmed, 'ed'))
        else:
            self.step1b_third_rule = self.replace_end('ing', '',
                                        self.v_in_stem(self.stemmed, 'ing'))

    def step1b1(self):
        """The rule to map to a single letter causes the removal of one of the
        double letter pair. This rule puts the -E back on -AT, -BL and -IZ, so
        that the suffixes -ATE, -BLE and -IZE can be recognised later. This E
        may be removed in step 4. (This rule is applied only if the second or
        third rule of step1b was satisfied.)
        """
        self.replace_end('at', 'ate')
        self.replace_end('bl', 'ble')
        self.replace_end('iz', 'ize')
        if self.stem_m () == 1 and self.stem_ends_with_cvc():
            self.stemmed += 'e'
        self.remove_dbl_last_char(self.stem_ends_with_dbl_cons()
                    and not self.str_ends_with_char(self.stemmed,
                                                    ['l', 's', 'z']))

    def step1c(self):
        """Replaces 'y' by 'i' if the stem will have a vowel after y is
        removed."""
        self.replace_end('y', 'i', self.v_in_stem(self.stemmed, 'y'))

    def step2and3(self):
        """ Step 2 and step 3 map double suffices to single ones."""
        # Step 2
        self.replace_ends_if(self.step2_suffix_tbl,
                self.stem_m() > 0,
                m_thresh = 0)
        # Step 3
        self.stemmed = self.replace_ends_if(self.step3_suffix_tbl,
                                            self.stem_m() > 0,
                                            m_thresh = 0)

    def step4(self):
        """step4() removes -ant, -ence etc for stem measures greater than 1."""
        longest_match = self.longest_match(self.stemmed, self.step4_suffix_tbl)
        if self.stemmed.endswith('ion') and len(longest_match[0]) < len('ion'):
            if self.str_ends_with_char(self.rep_end(self.stemmed, 'ion'),
                                        ['s', 't']):
                longest_match = ('ion', '')
        if self.stem_m(longest_match[0]) > 1:
            self.stemmed = self.rep_end(self.stemmed, longest_match[0],
                                        longest_match[1])

    def step5(self):
        """step5() removes a last -e if stem measure > 1, and changes -ll to -l
        if stem measure > 1. """
        stem_m = self.stem_m('e')
        if stem_m > 1:
            self.replace_end('e', '')
        elif stem_m == 1 and not self.stem_ends_with_cvc('e'):
            self.replace_end('e', '')
        self.remove_dbl_last_char(self.stem_ends_with_dbl_cons()
            and self.stem_m() > 1
            and self.str_ends_with_char(self.stemmed, ['l']))

    def stem(self, word):
        """Returns the stemmed word."""
        self.original_word, self.stemmed = word, word
        self.step1b_second_rule, self.step1b_third_rule = False, False
        # Departure
        # Strings with length less than 3 don't get stemmed.
        if len(self.original_word) < 3:
            return self.stemmed
        self.step1ab()
        if self.step1b_second_rule or self.step1b_third_rule:
            self.step1b1()
        self.step1c()
        self.step2and3()
        self.step4()
        self.step5()
        return self.stemmed

if __name__ == '__main__':
    import sys

    def main():
        stemmer = Stemmer()

        if len(sys.argv) > 1:
            output = []
            for file_ in sys.argv[1:]:
                for line in file(file_, 'r'):
                    output += [stemmer.stem(word) for word in line.split()]
                    print "\n".join(output)

    main()

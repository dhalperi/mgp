#!/usr/bin/env python

"""
Analyze scraped data from the Mathematical Genealogy Project.

Usage: analyze.py INPUT [INPUT ...]
"""

import copy
from docopt import docopt
import itertools
import json


def chain2(iterable):
    return itertools.chain(*iterable)


def do_agg(agg, vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return agg(vals)


def guess_years(authors, people, students, advisors, edges):
    no_year = {auth['mgpid'] : None for auth in authors if auth['year'] is None}
    ACAD_GEN = 5
    while True:
        old = copy.copy(no_year)
        for mgpid in no_year:
            advisor_year = do_agg(max, (people[adv]['year'] or no_year[adv]
                                        for adv in people[mgpid]['advisors']))
            student_year = do_agg(min, (people[stu]['year'] or no_year[stu]
                                        for stu in edges[mgpid]))

            if student_year is not None and advisor_year is not None:
                guess = (student_year + advisor_year) / 2
            elif student_year is not None:
                guess = student_year - ACAD_GEN
            elif advisor_year is not None:
                guess = advisor_year + ACAD_GEN
            else:
                guess = None
            no_year[mgpid] = guess

        if old == no_year:
            break
    return no_year


def make_graph(filename):
    with open(filename, 'r') as file_:
        authors = json.load(file_)
    people = {auth['mgpid'] : auth
              for auth in authors}
    students = {auth['mgpid']
                for auth in authors
                if len(auth['advisors']) > 0}
    advisors = set(chain2(auth['advisors'] for auth in authors))

    edges = {people[adv]['mgpid'] : [auth['mgpid']
                                     for auth in authors
                                     if adv in auth['advisors']]
             for adv in advisors}
    assert len(advisors) == len(edges)
    print "%d people, %d students, %d advisors" % (len(people), len(students), len(advisors))

    guessed_years = guess_years(authors, people, students, advisors, edges)
    print "guessed years for %d people" % len(guessed_years)

    for guess_id in guessed_years:
        people[guess_id]['year'] = guessed_years[guess_id]
    print json.dumps(authors)

    
def main(argv=None):
    args = docopt(__doc__, argv)
    for filename in args['INPUT']:
        make_graph(filename)

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

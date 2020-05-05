#!/usr/bin/env python3
"""tests for gene_ids.py"""

import os
import random
import re
import string
from subprocess import getstatusoutput

prg = './gene_ids.py'
amigo = './inputs/amigo_heat.txt'
tair = './inputs/tair_heat.txt'
repeat = './inputs/amigo_repeat.txt'
outfile = 'out.txt'

# --------------------------------------------------
def random_string():
    """generate a random string"""

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

# --------------------------------------------------
def test_exists():
    """usage"""

    for file in [prg, amigo, tair]:
        assert os.path.isfile(file)


# --------------------------------------------------
def test_usage():
    """usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput('{} {}'.format(prg, flag))
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_missing_file():
    """fails on no input"""

    rv, out = getstatusoutput(f'{prg} -o {outfile}')
    assert rv != 0
    assert re.search('the following arguments are required: -f/--file', out)


# --------------------------------------------------
def test_bad_file():
    """die on bad file"""

    bad = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    rv, out = getstatusoutput(f'{prg} -f {bad}')
    assert rv != 0
    assert re.match('usage:', out, re.I)
    assert re.search(f"No such file or directory: '{bad}'", out)


# --------------------------------------------------
def test_amigo():
    """runs on AmiGO file"""

    out_file = 'out.txt'
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        rv, out = getstatusoutput(f'{prg} -f {amigo}')
        assert rv == 0
        expected = ('  1: amigo_heat.txt\n'
                    'Wrote 16 gene IDs from 1 file to file "out.txt"')
        assert out == expected
        assert os.path.isfile(out_file)
        exp_amigo = '\n'.join(
            sorted("""
            AT5G12020 AT3G24520 AT1G16030 AT4G19630 AT1G64280 AT3G06400
            AT5G41340 AT2G22360 AT5G12140 AT5G03720 AT2G33590 AT1G54050
            AT3G10800 AT3G04120 AT3G24500 AT4G14690
            """.split()))
        assert open(out_file).read().strip() == exp_amigo.strip()

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)


# --------------------------------------------------
def test_tair():
    """runs on TAIR file"""

    out_file = "out.txt"
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        rv, out = getstatusoutput(f'{prg} -f {tair}')
        assert rv == 0
        expected = ('  1: tair_heat.txt\n'
                    'Wrote 5 gene IDs from 1 file to file "out.txt"')
        assert out == expected
        assert os.path.isfile(out_file)
        exp_tair = '\n'.join(
            sorted("""
                    AT5G67030 AT1G13930 AT3G09440 AT1G16540 AT2G22360
                    """.split()))
        assert open(out_file).read().strip() == exp_tair.strip()

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)


# --------------------------------------------------
def test_two_files():
    """runs on TAIR and AmiGO file"""

    out_file = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=5))
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        rv, out = getstatusoutput(f'{prg} -f {tair} {amigo} -o {out_file}')
        assert rv == 0
        assert re.search('1: tair_heat.txt', out)
        assert re.search('2: amigo_heat.txt', out)
        assert re.search(
            f'Wrote 20 gene IDs from 2 files to file "{out_file}"', out)
        assert os.path.isfile(out_file)
        exp_two = '\n'.join(
            sorted("""
                    AT5G12020 AT3G06400 AT2G33590 AT1G54050 AT5G67030 AT4G14690 AT1G16030 AT5G03720 AT3G10800 
                    AT5G12140 AT1G64280 AT3G24500 AT3G09440 AT3G04120 AT4G19630 AT1G16540 AT2G22360 AT1G13930 
                    AT5G41340 AT3G24520
                    """.split()))
        assert open(out_file).read().strip() == exp_two.strip()

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)


# --------------------------------------------------
def test_repeat_seq():
    """runs on AmiGO file with repeated sequences"""

    out_file = "out.txt"
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        rv, out = getstatusoutput(f'{prg} -f {repeat}')
        assert rv == 0
        expected = ('  1: amigo_repeat.txt\n'
                    'Wrote 5 gene IDs from 1 file to file "out.txt"')
        assert out == expected
        assert os.path.isfile(out_file)
        exp_repeat = '\n'.join(
            sorted("""
                    AT4G14690 AT5G41340 AT5G03720 AT5G12020 AT2G22360
                    """.split()))
        assert open(out_file).read().strip() == exp_repeat.strip()

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)

# --------------------------------------------------
def test_repeat_seq():
    """runs on AmiGO file with repeated sequences"""

    out_file = "out.txt"
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        rv, out = getstatusoutput(f'{prg} -f {repeat}')
        assert rv == 0
        expected = ('  1: amigo_repeat.txt\n'
                    'Wrote 5 gene IDs from 1 file to file "out.txt"')
        assert out == expected
        assert os.path.isfile(out_file)
        exp_repeat = '\n'.join(
            sorted("""
                    AT4G14690 AT5G41340 AT5G03720 AT5G12020 AT2G22360
                    """.split()))
        assert open(out_file).read().strip() == exp_repeat.strip()

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)

# --------------------------------------------------
def test_outfile():
    """runs with outfile argument"""

    out_file = random_string() + '.txt'
    try:
        if os.path.isfile(out_file):
            os.remove(out_file)

        rv, out = getstatusoutput(f'{prg} -f {repeat} -o {out_file}')
        assert rv == 0
        expected = (f'  1: amigo_repeat.txt\n'
                    f'Wrote 5 gene IDs from 1 file to file "{out_file}"')
        assert out == expected
        assert os.path.isfile(out_file)
        exp_repeat = '\n'.join(
            sorted("""
                    AT4G14690 AT5G41340 AT5G03720 AT5G12020 AT2G22360
                    """.split()))
        assert open(out_file).read().strip() == exp_repeat.strip()

    finally:
        if os.path.isfile(out_file):
            os.remove(out_file)
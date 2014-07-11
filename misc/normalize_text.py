#!/usr/bin/python3

import sys

def normalize(s):
    lines = []
    pieces = []
    current_line_empty = True
    def flush_line():
        if not pieces: return
        lines.append(' '.join(pieces))
        pieces.clear()
    def current_len():
        return sum((len(piece)+1) for piece in pieces) - 1
    def previous_len():
        return sum((len(piece)+1) for piece in pieces[:-1]) - 1
    for line in s.split('\n'):
        flush_line()
        if not line:
            lines.append('')
            continue
        for piece in line.split(' '):
            pieces.append(piece)
            if current_len() > 79:
                if previous_len() < 0:
                    # very large piece, nothing we can do
                    flush_line()
                    continue
                else:
                    piece = pieces.pop()
                    flush_line()
                    pieces.append(piece)
            if is_end_of_sentence(piece):
                flush_line()
                continue
    flush_line()
    return '\n'.join(lines)

def is_end_of_sentence(piece):
    return piece.endswith(('.', ';')) and len(piece) > 2

if __name__ == '__main__':
    s = sys.stdin.read()
    assert '\t' not in s, 'Tabulation detected'
    s = normalize(s)
    sys.stdout.write(s)



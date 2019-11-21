from matcher import match


def regex_matcher(regex, stack):
    # TODO empty regex always/never match?
    for i, j in zip(range(len(regex))):  # Two indexes for future kleene star
        if not match(regex[i], stack[j]):
            # One element did not match
            return False
    # All elements matched
    return True

# Just exact pattern matching, not ? or *
# TODO implement

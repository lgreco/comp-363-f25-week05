def a(x, y):
    """Simple scoring function: 0 for match, 2 for mismatch."""
    return 0 if x == y else 2


# Gap penalty
a_space = 1


def score(X, Y, scoring_function, a_space=a_space):
    """Compute the penalty table for sequences X and Y."""
    # Lengths of sequences for ease of use
    m = len(X)
    n = len(Y)
    # Initialize penalty table
    P = [[0 for j in range(n + 1)] for i in range(m + 1)]
    # Populate first row and column with initial gap penalties
    for i in range(1, m + 1):
        P[i][0] = i * a_space
    for j in range(1, n + 1):
        P[0][j] = j * a_space
    # Fill in the rest of the table
    for i in range(1, m + 1):
        # Adjusted index for sequence X for 0-based indexing
        x = X[i - 1]
        for j in range(1, n + 1):
            # Adjusted index for sequence Y for 0-based indexing
            y = Y[j - 1]
            # Compute minimum penalty based on match/mismatch and gaps
            P[i][j] = min(
                P[i - 1][j - 1] + scoring_function(x, y),
                P[i - 1][j] + a_space,
                P[i][j - 1] + a_space,
            )
    return P


def trace_back(P, X, Y, scoring_function, a_space=a_space):
    """Trace back through the penalty table to get aligned sequences."""
    # count gaps and match/mismatches for reporting
    gaps = 0
    matches = 0
    mismatches = 0
    # Initialize aligned sequences
    aligned_X = ""
    aligned_Y = ""
    # Start from bottom-right corner of the table
    i = len(X)
    j = len(Y)
    # Trace back until reaching the top-left corner
    while i > 0 or j > 0:
        # Get the current score
        current_score = P[i][j]
        # Determine the direction of the traceback
        if (
            i > 0
            and j > 0
            and current_score == P[i - 1][j - 1] + scoring_function(X[i - 1], Y[j - 1])
        ):
            # Match or mismatch
            aligned_X = X[i - 1] + aligned_X
            aligned_Y = Y[j - 1] + aligned_Y
            i -= 1
            j -= 1
            # Update match/mismatch counts
            if X[i] == Y[j]:
                matches += 1
            else:
                mismatches += 1
        elif i > 0 and current_score == P[i - 1][j] + a_space:
            # Deletion in Y (gap in Y)
            aligned_X = X[i - 1] + aligned_X
            aligned_Y = "-" + aligned_Y
            # Move up in the table
            i -= 1
            # Update gap count
            gaps += 1
        else:
            # Insertion in Y (gap in X)
            aligned_X = "-" + aligned_X
            aligned_Y = Y[j - 1] + aligned_Y
            # Move left in the table
            j -= 1
            # Update gap count
            gaps += 1
    return aligned_X, aligned_Y, matches, mismatches, gaps


# Test
tests = [
    ["CRANE", "RAIN"],
    ["CYCLE", "BICYCLE"],
    ["ASTRONOMY", "GASTRONOMY"],
    ["INTENTION", "EXECUTION"],
    ["AGGTAB", "GXTXAYB"],
    ["GATTACA", "GCATGCU"],
    ["DELICIOUS", "RELIGIOUS"],
]

# For formatting purposes, what's the longest string above?
longest = max((s for pair in tests for s in pair), key=len)
L = len(longest)

# Printing constants
MAP_TO = " --> "
MATCHES = "  matches: "
MISMATCHES = ", mismatches: "
GAPS = "  gaps: "
BOLD = "\033[1m"
UNBOLD = "\033[0m"

for X, Y in tests:
    P = score(X, Y, a)
    aligned_X, aligned_Y, matches, mismatches, gaps = trace_back(P, X, Y, a)

    print(f"{X:>{L}}{MAP_TO}{BOLD}{aligned_X:<{L}}{UNBOLD}{MATCHES}{matches}{MISMATCHES}{mismatches}")
    print(f"{Y:>{L}}{MAP_TO}{BOLD}{aligned_Y:<{L}}{UNBOLD}{GAPS}{gaps}\n")

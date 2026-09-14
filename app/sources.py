"""First-party public sources used for evidence-backed construction leads."""
from __future__ import annotations

BCA_NY_MEMBER_DIRECTORY = "https://www.ny-bca.com/member-directory/"

DEFAULT_SOURCE_URLS = [BCA_NY_MEMBER_DIRECTORY]

# These are search seeds, not contact data. Runtime discovery should fetch current pages.
BCA_NY_QUERIES = [
    'site:ny-bca.com/member-directory/ "PRESIDENT" construction New York',
    'site:ny-bca.com/member-directory/ "CEO" construction New York',
    'site:ny-bca.com/member-directory/ "OWNER" construction New York',
    'site:ny-bca.com/member-directory/ "VICE PRESIDENT" construction New York',
]

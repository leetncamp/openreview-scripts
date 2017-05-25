#!/usr/bin/python

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "/Users/michaelspector/projects/openreview/openreview-scripts/utils"))
import utils

"""
GROUPS

Defines constants for CONF (the name of the conference), and for the names of each group.
All other groups will be named by joining the name with CONF: <CONF>/<NAME>

Example:

    CONF = 'my.conference/2017'
    PROGRAM_CHAIRS = 'Program_Chairs'

    --> my.conference/2017/Program_Chairs

"""

CONF = "swsa.semanticweb.org/ISWC/2017/DeSemWeb"
ADMIN = CONF + '/Admin'
PROGRAM_CHAIRS = CONF + '/Program_Chairs'
AREA_CHAIRS = CONF + '/Area_Chairs'
REVIEWERS = CONF + '/Reviewers'
DUE_TIMESTAMP = 1500695940000
WEBPATH = utils.get_path('../webfield/conf.html', __file__)


"""
INVITATIONS

Defines constants for various invitations.
The full name of an invitation will be generated by joining the name with CONF by "/-/": <CONF>/-/<INVITATION_NAME>

Example:

    CONF = 'my.conference/2017'
    SUBMISSION = 'Submission'

    --> my.conference/2017/-/Submission

"""

SUBMISSION = CONF + '/-/Submission'
COMMENT = CONF + '/-/Comment'


"""
PARAMETERS

Dictionaries that represent argument combinations defining Group and Invitation permissions.

Example:

    restricted = {
        'readers': [CONF],
        'writers': [CONF],
        'signatories': [CONF],
    }

    The "restricted" configuration above will only allow the CONF group to read, write, and sign
    for the newly created Group that uses it.
"""

conf_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'signatories': [CONF],
    'web': WEBPATH
}

group_params = {
    'readers': [CONF],
    'writers': [CONF],
    'signatories': [CONF],
}

submission_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': ['~'],
    'signatures': [CONF],
    'process': utils.get_path('../process/submissionProcess.js', __file__)
}

comment_params = {
    'readers': ['everyone'],
    'writers': [CONF],
    'invitees': ['~'],
    'signatures': [CONF],
    'process': utils.get_path('../process/commentProcess.js', __file__)
}




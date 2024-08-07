#!/usr/bin/env python3

import getopt, sys
import requests
import os
import json


SELFSERVE_QUALITY_URL = 'https://selfserve.eu-west-1.gd.mpi-internal.com:443/api/v1/quality/suites?requestedBy=gp.gt.yotta@adevinta.com'
SELFSERVE_AUTH = (os.getenv('SELFSERVE_USER'), os.getenv('SELFSERVE_SECRET'))
SELFSERVE_HEADERS = { 'Content-Type': 'application/json' }


def SELFSERVE_QUALITY_URL_WITH_OFFSET(offset):
    return f"{SELFSERVE_QUALITY_URL}&offset={offset}"



class DQS:
    def __init__(self, id, path):
        self.id = id
        self.path = path
    def __str__(self):
        return "DQS(" + str(self.id) + ", " + str(self.path) + ")"



def get_selfserve_dqs(verbose):
    """
    Gets all DQS from selfserve
    :param verbose:
    :return: DQS list
    """
    print("Getting DQS from selfserve")

    try:
        offset = 0
        all_dqs = []

        while True:
            response = requests.get(SELFSERVE_QUALITY_URL_WITH_OFFSET(offset), auth=SELFSERVE_AUTH, headers=SELFSERVE_HEADERS)
            response.raise_for_status()
            json = response.json()
            if verbose:
                print("\t%s" % json)

            if len(json['data']) == 0:
                print("\tdone with pagination!")
                break

            for item in json['data']:
                dqs = DQS(item['id'], item['dqcPath'])
                if verbose:
                    print("\t%s" % dqs)
                all_dqs.append(dqs)

            offset += len(json['data'])

        return all_dqs
    except Exception as e:
        print("%s" % (str(e)))
        sys.exit(2)




def get_local_dqs(verbose, path='src/main/resources', suffix='-suite.jslt'):
    """
    Gets all DQS files from file system.
    :param verbose:
    :param path: Resulting list is restricted to files under the given path
    :param suffix: Resulting list is restricted to files having this suffix
    :return: List of file names
    """
    print("Getting DQS files from local file system with suffix=%s and path=%s" % (suffix, path))

    fnames = []
    for root,d_names,f_names in os.walk(path):
        for f in f_names:
            if f.endswith(suffix):
                fnames.append(os.path.join(root, f))

    if verbose:
        for f in fnames:
            print("\t%s" % f)

    return fnames




def register_dqs(file, dry_run, verbose):
    """
    Registers the given file as a DQS in selfserve
    :param file:
    :param dry_run: Do registration if dry_run, skip otherwise
    :param verbose:
    :return:
    """
    if dry_run:
        print("File %s requires registration" % (file))
    else:
        print("Registering file %s" % (file))

        data = {
            'dqcPath': 'https://github.mpi-internal.com/yotta/jslt-lib/blob/master/' + file
        }
        if verbose:
            print("\t%s" % data)

        try:
            response = requests.post(SELFSERVE_QUALITY_URL, auth=SELFSERVE_AUTH, headers=SELFSERVE_HEADERS, json=data)
            response.raise_for_status()
            json = response.json()
            if verbose:
                print("\t%s" % json)
            print("File %s was registered with id %s" % (file, json['id']))
        except Exception as e:
            print("%s" % (str(e)))
            sys.exit(2)





def review_pr(selfserve_dqs, local_dqs, verbose):
    """
    Reviews the PR to determine whether it can be approved or not.

    Following scenarios prevent the PR to be merged:
    - A DQS in selfserve misses the file in the local file system (a DQS got orphaned).

    :param selfserve_dqs: Selfserve-registered DQS list
    :param local_dqs: Local files DQS list
    :param verbose:
    :return: True if PR is not breaking consistency with DQS in selfserve, False otherwise.
    """
    print("Reviewing pull request")

    missing_dqs = []

    for dqs in selfserve_dqs:
        if verbose:
            print("\tProcessing DQS %s %s" % (dqs.id, dqs.path))

        matches = [file for file in local_dqs if dqs.path.endswith(file)]
        if verbose and matches:
            print("\t\tIn-sync with with %s" % str(matches))
        if not matches:
            missing_dqs.append(dqs)

    if missing_dqs:
        print("Following DQS would be orphaned, so this PR cannot be merged")
        for dqs in missing_dqs:
            print(dqs)

    approval = len(missing_dqs) == 0
    print("Approving? %s" % approval)
    
    if not approval:
       print("Make sure your branch is up to date with master branch.")
    return approval




def dqs_sync(selfserve_dqs, local_dqs, dry_run, verbose):
    """
    Keeps DQS in-sync with local files.

    Actions:
    - Register local DQS that were never registered before.

    Use cases to be implemented:
    - Unregister a selfserve DQS if not in use and there is no local DQS anymore.

    :param selfserve_dqs:
    :param local_dqs:
    :param dry_run:
    :param verbose:
    :return:
    """
    print("Synchronizing DQS and local files (dry-run=%d)" % (dry_run))

    new_dqs = []

    for file in local_dqs:
        if verbose:
            print("\tProcessing file %s" % (file))

        matches = [dqs for dqs in selfserve_dqs if dqs.path.endswith(file)]
        if not matches:
            new_dqs.append(file)

    if new_dqs:
        for file in new_dqs:
            register_dqs(file, dry_run, verbose)


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:v", ["mode="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    mode = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            sys.exit(2)
        elif o in ("-m", "--mode"):
            mode = a
        else:
            assert False, "unhandled option"

    selfserve_dqs = get_selfserve_dqs(verbose)
    local_dqs = get_local_dqs(verbose)

    if mode == "review":
        dqs_sync(selfserve_dqs, local_dqs, dry_run=True, verbose=verbose)
        approve = review_pr(selfserve_dqs, local_dqs, verbose=verbose)

        if approve:
            sys.exit(0)
        else:
            sys.exit(2)
    elif mode == "sync":
        dqs_sync(selfserve_dqs, local_dqs, dry_run=False, verbose=verbose)
        sys.exit(0)
    else:
        print("Unexpected mode: %s" % (mode))
        sys.exit(2)


if __name__ == "__main__":
    main()

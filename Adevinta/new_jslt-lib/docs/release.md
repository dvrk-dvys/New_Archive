
# Release

## Versioning 

Release process is automatically triggered for every commit to `master` branch.
The release process generates a version for both Scala 2.11 and Scala 2.12 with the following versioning:
`0.1.<YYYYMMDDHHMM>.<GitHash>`.

## TricklerDowner

TricklerDowner notification is enabled so consumers of the library can get automatic upgrades.
#!/usr/bin/env bash
set -e

./gradlew -PscalaVersion="2.11.11" check --parallel
./gradlew -PscalaVersion="2.12.8" check --parallel

#!/usr/bin/env bash
set -e

./gradlew -PscalaVersion="2.11.11" publish tricklerdowner
./gradlew -PscalaVersion="2.12.8" publish tricklerdowner

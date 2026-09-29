#!/usr/bin/env bash
# Entry point for the feature-local acceptance harness.
#
# The supplied legacy Project is read-only input.  This setup shell creates no
# files; later harness stages may use only temporary or feature-local outputs.

set -euo pipefail

usage() {
  printf 'Usage: %s /absolute/path/to/legacy/Project\n' "${0##*/}" >&2
}

if (( $# != 1 )); then
  usage
  exit 64
fi

legacy_project=$1

if [[ $legacy_project != /* ]]; then
  printf 'Error: legacy Project path must be absolute: %s\n' "$legacy_project" >&2
  usage
  exit 64
fi

if [[ ! -d $legacy_project ]]; then
  printf 'Error: legacy Project directory does not exist: %s\n' "$legacy_project" >&2
  exit 66
fi

# T006/T007 add the runner invocation and source-layout validation.  Keeping
# this shell side-effect-free preserves the supplied project as read-only input.
exit 0

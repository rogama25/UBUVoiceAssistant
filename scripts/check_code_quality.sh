#!/bin/bash
pylint src -ry
pylint --disable=E0401 src/skills -ry
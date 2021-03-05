#!/bin/bash
find . -iname "*.py" | xargs xgettext --from-code utf-8 -o ./src/lang/translation_template.pot
#!/bin/bash
mv src/skills/ubu-calendar src/skills/ubu_calendar
mv src/skills/ubu-course src/skills/ubu_course
mv src/skills/ubu-grades src/skills/ubu_grades
mypy src
mv src/skills/ubu_calendar src/skills/ubu-calendar
mv src/skills/ubu_course src/skills/ubu-course
mv src/skills/ubu_grades src/skills/ubu-grades

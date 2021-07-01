#!/bin/bash
mv src/UBUVoiceAssistant/skills/ubu-calendar src/UBUVoiceAssistant/skills/ubu_calendar
mv src/UBUVoiceAssistant/skills/ubu-course src/UBUVoiceAssistant/skills/ubu_course
mv src/UBUVoiceAssistant/skills/ubu-grades src/UBUVoiceAssistant/skills/ubu_grades
mv src/UBUVoiceAssistant/skills/ubu-help src/UBUVoiceAssistant/skills/ubu_help
mv src/UBUVoiceAssistant/skills/ubu-messages src/UBUVoiceAssistant/skills/ubu_messages
mypy src > report.log
mv src/UBUVoiceAssistant/skills/ubu_calendar src/UBUVoiceAssistant/skills/ubu-calendar
mv src/UBUVoiceAssistant/skills/ubu_course src/UBUVoiceAssistant/skills/ubu-course
mv src/UBUVoiceAssistant/skills/ubu_grades src/UBUVoiceAssistant/skills/ubu-grades
mv src/UBUVoiceAssistant/skills/ubu_help src/UBUVoiceAssistant/skills/ubu-help
mv src/UBUVoiceAssistant/skills/ubu_messages src/UBUVoiceAssistant/skills/ubu-messages

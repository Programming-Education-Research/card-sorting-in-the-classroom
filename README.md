# Card Sorting in the Classroom

Software to parse MoodleXML, student Moodle responses, and generate completions
for cardsort, refute, and reverse tracing questions.

## Project Structure

The bulk of this repository is a python project to bulk-process Moodle data and
generate LLM completions to questions which are all persisted in an SQLite
database. This Python project can be installed as an editable installation:

```bash
pip install -e .
```

The other component of this project is a series of Python and RMarkdown scripts
in the `./scripts` directory. The Python scripts in this directory depend on the
main Python project having been installed.

The data sources for this project have not been included as they are not, and
cannot easily be, anonymised.

## License

Copyright (C) 2025 James Finnie-Ansley

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Affero General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with this program. If not, see <https://www.gnu.org/licenses/>.

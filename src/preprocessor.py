from pathlib import Path

from definitions.exceptions import ParserException


class Preprocessor:

    _content: str
    _source_path: str

    filename: str

    def __init__(self, filename: str):
        self._source_path = Path(filename).parent

        self.filename = filename

    @staticmethod
    def _get_filename(line: str) -> str:
        parts = line.split(None, 1)
        if len(parts) > 1:
            return parts[1].strip()

        raise ParserException(f"Invalid import statement: '{line}'")

    def process(self, filename: str = None) -> str:
        filename = filename if filename else self.filename
        final_content = ''
        with open(filename, 'r') as main_file:
            for line in main_file.readlines():
                if line.startswith('%IMPORT'):
                    f = self._get_filename(line)
                    path = Path(f)

                    if not path.is_absolute():
                        abs_path = Path(self._source_path)
                        path = abs_path.joinpath(Path(f))

                    final_content += self.process(path)

                else:
                    final_content += line

        return final_content

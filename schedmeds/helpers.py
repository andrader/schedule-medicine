from pathlib import Path
import jsonpickle

def write_data(data, path):
    s = jsonpickle.encode(data, indent=2)
    Path(path).write_text(s)


def load_data(path):
    return jsonpickle.decode(Path(path).read_text())

from argparse import ArgumentParser
import json

from polyaxon.tracking import Run
import yaml


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('--param-file', action='append', default=[])
    parser.add_argument('--metric-file', action='append', default=[])
    parser.add_argument('--data-file', action='append', default=[])
    parser.add_argument('--tag', action='append', default=[])
    
    return parser.parse_args()


def startswith(s: str, vals):
    return any(s.startswith(v) for v in vals)


def parse_gin_line(line):
    lhs, rhs = line.split('=')
    lhs = lhs.strip().replace('.', '__').replace('/', '__')
    rhs = rhs.strip()
    if startswith(rhs, ['@', '%', '"', "'"]):
        rhs = rhs.replace('"', '').replace("'", '')
    elif startswith(rhs, ['\\', '[', '(']):
        pass
    elif rhs in ['True', 'False']:
        rhs = rhs == 'True'
    elif '.' in rhs:
        rhs = float(rhs)
    elif rhs == 'None':
        rhs = None
    else:
        rhs = int(rhs)
    return lhs, rhs


def load_gin(stream):
    return {
        parse_gin_line(line)[0]: parse_gin_line(line)[1]
        for line in stream
        if '=' in line and not line.startswith('#')
    }


def get_loader(fname):
    if fname.lower().endswith(".json"):
        return json.load
    if fname.lower().endswith(".yml") or fname.lower().endswith(".yaml"):
        return yaml.load
    if fname.lower().endswith(".gin"):
        return load_gin
    raise ValueError(f'Unsupported file format: {fname}')


def load(fname):
    loader = get_loader(fname)
    with open(fname) as infile:
        return loader(infile)


def load_values(fnames):
    vals = {}
    for fname in fnames:
        vals.update(**load(fname))
    return vals


def load_datasets(fnames):
    from divik._cli._data_io import load_data
    return (
        {'content': load_data(fname), 'name': fname, 'path': fname}
        for fname in fnames
    )


def main():
    args = parse_args()
    experiment = Run()
    params = load_values(args.param_file)
    if params:
        experiment.log_params(**params)
    metrics = load_values(args.metric_file)
    if metrics:
        experiment.log_metrics(**metrics)
    if args.tag:
        experiment.log_tags(args.tag)
    for dataset in load_datasets(args.data_file):
        experiment.log_data_ref(**dataset)


if __name__ == '__main__':
    main()
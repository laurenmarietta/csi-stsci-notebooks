import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

"""
This script requires nbformat and nbconvert >5.x
"""


def execute(nb_in_fn, kernel_name='python3', run_path='.'):
    nb_out_fn = nb_in_fn.replace('.ipynb', '.nbconvert.ipynb')

    with open(nb_in_fn) as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name=kernel_name)

    failed = False
    try:
        out = ep.preprocess(nb, {'metadata': {'path': run_path}})
    except CellExecutionError as e:
        out = None
        print('Error executing the notebook "{}". Traceback:'.format(nb_in_fn))
        print(e.traceback)
        failed = True
    finally:
        with open(nb_out_fn, mode='wt') as f:
            nbformat.write(nb, f)

    return not failed

if __name__ == '__main__':
    import os
    import sys
    from glob import glob

    kernel_name = 'python3'


    nbfns = glob('*/*.ipynb')
    nbfns = [fn for fn in nbfns if not fn.endswith('.nbconvert.ipynb')]

    print("Running the following notebooks:", nbfns)

    succeeded = True
    for nbfn in nbfns:
        nb_dir = os.path.abspath(os.path.join('.', os.path.split(nbfn)[0]))
        succeeded = succeeded and execute(nbfn, kernel_name, nb_dir)

    if not succeeded:
        sys.exit(1)
    else:
        sys.exit(0)

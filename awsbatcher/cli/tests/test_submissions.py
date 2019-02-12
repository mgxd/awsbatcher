import pytest

from awsbatcher import PROJECTS_DIR
from awsbatcher.cli.run import main as submit

@pytest.mark.parametrize('dataset', list(PROJECTS_DIR.keys()))
def test_datasets(tmpdir, dataset):
    args = [dataset, 'job-queue', 'job-definition', '--dry']
    submit(args)

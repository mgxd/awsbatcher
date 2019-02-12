import pytest
from moto import mock_s3

from awsbatcher import PROJECTS_DIR
from awsbatcher.cli.run import main as submit

@mock_s3
@pytest.mark.parametrize('dataset', list(PROJECTS_DIR.keys()))
def test_datasets(tmpdir, dataset):
    args = [dataset, 'job-queue', 'job-definition', '--dry']
    submit(args)

# TidyTrace Tests

Install the test requirements from `tests/requirements.txt`.

## Test decorators

A `@test` decorator is available in the `tests/utils` module. This will mark any
function as a test function.

## Approval Tests

These tests
use [ApprovalTests](https://github.com/approvals/ApprovalTests.Python) and
[pytest](https://docs.pytest.org/en/7.4.x/) with the
[ApprovalTests pytest plugin](https://github.com/approvals/ApprovalTests.Python.PytestPlugin).
To enable diff checking on PyCharm, see
[their documentation](https://github.com/approvals/ApprovalTests.Python.PytestPlugin#tip-for-jetbrains-toolbox-and-pycharm-users)
which describes how to set up a run configuration which uses PyCharm's built-in
diff checker.

The working directory of the tests should be set to be the `tests/` directory.
Your pytest arguments should look something like:

```
--approvaltests-add-reporter-args='diff' \
--approvaltests-add-reporter='/Applications/PyCharm.app/Contents/MacOS/pycharm'
```

Or something like:

```
--approvaltests-add-reporter-args='diff' \
--approvaltests-add-reporter='~/.local/share/JetBrains/Toolbox/apps/pycharm-professional/bin/pycharm'
```

I don't know how to use Windows computers — If you are a Windows user, you are
on your own on this one.

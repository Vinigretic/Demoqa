from typing import Any  # Optional[X] — Union[X, None]

import pytest
from _pytest.runner import CallInfo

from utils.test_handlers import handle_ui_test, handle_api_test, handle_common_test


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Any, call: CallInfo[Any]) -> None:
    outcome = yield
    result = outcome.get_result()

    if any(f in item.funcargs for f in ("driver", "driver_for_download_file")):
        handle_ui_test(item, call, result)
    elif "api_client" in item.funcargs:
        handle_api_test(item, call, result)
    else:
        handle_common_test(item, call, result)

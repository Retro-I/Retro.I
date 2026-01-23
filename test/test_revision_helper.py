import unittest
from unittest.mock import patch

from helper.RevisionHelper import RevisionHelper


class RevisionHelperTests(unittest.TestCase):

    def setUp(self):
        self.revision_helper = RevisionHelper()

    @patch("helper.RevisionHelper.logger.info")
    @patch("helper.RevisionHelper.subprocess.check_output")
    @patch.object(RevisionHelper, "get_branches")
    @patch.object(RevisionHelper, "get_current_revision")
    def test_delete_local_branch(
        self,
        mock_current_revision,
        mock_get_branches,
        mock_check_output,
        mock_logger,
    ):
        mock_current_revision.return_value = "main"

        mock_get_branches.return_value = [
            {"name": "main", "date": "01.01.2024"},
            {"name": "develop", "date": "02.01.2024"},
        ]

        mock_check_output.return_value = "main\ndevelop\nfeature1\n"

        self.revision_helper.cleanup_local_branches()

        mock_check_output.assert_any_call(
            ["git", "branch", "-D", "feature1"],
            text=True,
        )

        mock_logger.assert_any_call('Branch "feature1" deleted!')

    @patch("helper.RevisionHelper.logger.info")
    @patch("helper.RevisionHelper.subprocess.check_output")
    @patch.object(RevisionHelper, "get_current_revision")
    @patch.object(RevisionHelper, "get_current_revision")
    def test_delete_multiple_branches(
        self,
        mock_current_revision,
        mock_get_branches,
        mock_check_output,
        mock_logger,
    ):
        mock_current_revision.return_value = "main"

        mock_get_branches.return_value = [
            {"name": "main", "date": "01.01.2024"},
            {"name": "develop", "date": "02.01.2024"},
        ]

        mock_check_output.return_value = (
            "main\ndevelop\nfeature1\nfeature2\nrenovate-123-456\n"
        )

        self.revision_helper.cleanup_local_branches()

        mock_check_output.assert_any_call(
            ["git", "branch", "-D", "feature1"],
            text=True,
        )
        mock_check_output.assert_any_call(
            ["git", "branch", "-D", "feature2"],
            text=True,
        )
        mock_check_output.assert_any_call(
            ["git", "branch", "-D", "renovate-123-456"], text=True
        )

        mock_logger.assert_any_call('Branch "feature1" deleted!')
        mock_logger.assert_any_call('Branch "feature2" deleted!')
        mock_logger.assert_any_call('Branch "renovate-123-456" deleted!')

    @patch("helper.RevisionHelper.logger.info")
    @patch("helper.RevisionHelper.subprocess.check_output")
    @patch.object(RevisionHelper, "get_branches")
    @patch.object(RevisionHelper, "get_current_revision")
    def test_not_delete_branches(
        self,
        mock_current_revision,
        mock_get_branches,
        mock_check_output,
        mock_logger,
    ):
        mock_current_revision.return_value = "main"

        mock_get_branches.return_value = [
            {"name": "main", "date": "01.01.2024"},
            {"name": "develop", "date": "02.01.2024"},
        ]

        mock_check_output.return_value = "main\ndevelop\n"

        self.revision_helper.cleanup_local_branches()

        delete_calls = [
            call
            for call in mock_check_output.call_args_list
            if "-D" in call.args[0]
        ]

        self.assertEqual(delete_calls, [])
        mock_logger.assert_not_called()

    @patch("helper.RevisionHelper.logger.info")
    @patch("helper.RevisionHelper.subprocess.check_output")
    @patch.object(RevisionHelper, "get_branches")
    @patch.object(RevisionHelper, "get_current_revision")
    def test_not_delete_branches_only_on_remote(
        self,
        mock_current_revision,
        mock_get_branches,
        mock_check_output,
        mock_logger,
    ):
        mock_current_revision.return_value = "main"

        mock_get_branches.return_value = [
            {"name": "main", "date": "01.01.2024"},
            {"name": "develop", "date": "02.01.2024"},
            {"name": "feature1", "date": "03.01.2024"},
        ]

        mock_check_output.return_value = "main\ndevelop\n"

        self.revision_helper.cleanup_local_branches()

        delete_calls = [
            call
            for call in mock_check_output.call_args_list
            if "-D" in call.args[0]
        ]

        self.assertEqual(delete_calls, [])
        mock_logger.assert_not_called()

    @patch("helper.RevisionHelper.logger.info")
    @patch("helper.RevisionHelper.subprocess.check_output")
    @patch.object(RevisionHelper, "get_branches")
    @patch.object(RevisionHelper, "get_current_revision")
    def test_not_delete_when_branch_selected(
        self,
        mock_current_revision,
        mock_get_branches,
        mock_check_output,
        mock_logger,
    ):
        mock_current_revision.return_value = "feature1"

        mock_get_branches.return_value = [
            {"name": "main", "date": "01.01.2024"},
            {"name": "develop", "date": "02.01.2024"},
        ]

        mock_check_output.return_value = "main\ndevelop\nfeature1"

        self.revision_helper.cleanup_local_branches()

        delete_calls = [
            call
            for call in mock_check_output.call_args_list
            if "-D" in call.args[0]
        ]

        self.assertEqual(delete_calls, [])
        mock_logger.assert_not_called()

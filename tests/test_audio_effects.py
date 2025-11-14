import unittest
from tests.base_test import BaseTest


# TODO - fix and enable this with Issue #79
@unittest.skip
class TestAudioEffects(BaseTest):
    def setUp(self):
        super().setUp()

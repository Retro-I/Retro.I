from test.base_test import BaseTest


class TestBassSteps(BaseTest):
    def setUp(self):
        super().setUp()

    def test_default_bass_steps(self):
        actual = self.bass_steps_helper.get_slider()
        expected = [
            {
                "hertz": 120,
                "steps": [
                    {"step": 3, "value": 4},
                    {"step": 2, "value": 2.5},
                    {"step": 1, "value": 1.5},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": 0},
                    {"step": -2, "value": -2},
                    {"step": -3, "value": -3},
                ],
            },
            {
                "hertz": 140,
                "steps": [
                    {"step": 3, "value": 6},
                    {"step": 2, "value": 4},
                    {"step": 1, "value": 2},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": 0},
                    {"step": -2, "value": -2},
                    {"step": -3, "value": -3},
                ],
            },
            {
                "hertz": 200,
                "steps": [
                    {"step": 3, "value": 6},
                    {"step": 2, "value": 4},
                    {"step": 1, "value": 2},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": 0},
                    {"step": -2, "value": -2},
                    {"step": -3, "value": -3},
                ],
            },
            {
                "hertz": 250,
                "steps": [
                    {"step": 3, "value": 6},
                    {"step": 2, "value": 4},
                    {"step": 1, "value": 2},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": 0},
                    {"step": -2, "value": -2},
                    {"step": -3, "value": -3},
                ],
            },
        ]

        self.assertEqual(actual, expected)

    def test_min_step(self):
        actual = self.bass_steps_helper.get_min_step()
        expected = -3

        self.assertEqual(actual, expected)

    def test_max_step(self):
        actual = self.bass_steps_helper.get_max_step()
        expected = 3

        self.assertEqual(actual, expected)

    def test_gain_for_step(self):
        # Default
        actual = self.bass_steps_helper.get_gain_for_step(0, 0)
        self.assertEqual(actual, 0)

        actual = self.bass_steps_helper.get_gain_for_step(1, 120)
        self.assertEqual(actual, 1.5)

        actual = self.bass_steps_helper.get_gain_for_step(-3, 140)
        self.assertEqual(actual, -3)

    def test_steps_count(self):
        actual = self.bass_steps_helper.get_steps_count()
        self.assertEqual(actual, 7)

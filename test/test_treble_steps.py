from test.base_test import BaseTest


class TestTrebleSteps(BaseTest):
    def setUp(self):
        super().setUp()

    def test_default_bass_steps(self):
        slider = self.treble_steps_helper.get_slider()
        expected = [
            {
                "hertz": 1000,
                "steps": [
                    {"step": 3, "value": 3},
                    {"step": 2, "value": 2},
                    {"step": 1, "value": 1},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": -0.75},
                    {"step": -2, "value": -1.25},
                    {"step": -3, "value": -2},
                ],
            },
            {
                "hertz": 2000,
                "steps": [
                    {"step": 3, "value": 3},
                    {"step": 2, "value": 2},
                    {"step": 1, "value": 2},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": -0.75},
                    {"step": -2, "value": -1.25},
                    {"step": -3, "value": -2},
                ],
            },
            {
                "hertz": 5000,
                "steps": [
                    {"step": 3, "value": 6},
                    {"step": 2, "value": 4},
                    {"step": 1, "value": 2},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": -1.5},
                    {"step": -2, "value": -2.5},
                    {"step": -3, "value": -4},
                ],
            },
            {
                "hertz": 8000,
                "steps": [
                    {"step": 3, "value": 12},
                    {"step": 2, "value": 8},
                    {"step": 1, "value": 4},
                    {"step": 0, "value": 0},
                    {"step": -1, "value": -3},
                    {"step": -2, "value": -6},
                    {"step": -3, "value": -9},
                ],
            },
        ]

        self.assertEqual(slider, expected)

    def test_min_step(self):
        actual = self.treble_steps_helper.get_min_step()
        expected = -3

        self.assertEqual(actual, expected)

    def test_max_step(self):
        actual = self.treble_steps_helper.get_max_step()
        expected = 3

        self.assertEqual(actual, expected)

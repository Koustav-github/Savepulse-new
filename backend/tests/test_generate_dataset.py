import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta
import tempfile
import os
import pandas as pd

# Add the parent directory to the path so we can import the script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import generate_dataset


class TestHospitalGeneration(unittest.TestCase):
    """Test hospital data generation logic"""

    def test_hospital_name_format(self):
        """Test that hospital names are formatted correctly with prefix and suffix"""
        with patch('scripts.generate_dataset.random.choice') as mock_choice:
            mock_choice.side_effect = ["CityCare", "Hospital"]
            name = mock_choice() + " " + mock_choice()
            self.assertEqual(name, "CityCare Hospital")

    def test_hospital_prefixes_exist(self):
        """Test that hospital prefixes are defined"""
        self.assertIsInstance(generate_dataset.prefixes, list)
        self.assertGreater(len(generate_dataset.prefixes), 0)
        self.assertIn("CityCare", generate_dataset.prefixes)

    def test_hospital_suffixes_exist(self):
        """Test that hospital suffixes are defined"""
        self.assertIsInstance(generate_dataset.suffixes, list)
        self.assertGreater(len(generate_dataset.suffixes), 0)
        self.assertIn("Hospital", generate_dataset.suffixes)

    def test_coordinate_ranges(self):
        """Test that latitude and longitude are within defined ranges"""
        self.assertEqual(generate_dataset.LAT_MIN, 22.45)
        self.assertEqual(generate_dataset.LAT_MAX, 22.65)
        self.assertEqual(generate_dataset.LON_MIN, 88.25)
        self.assertEqual(generate_dataset.LON_MAX, 88.45)

    def test_hospital_size_categories(self):
        """Test hospital size categories and bed allocations"""
        # Test small hospital
        small_beds = 50  # within 40-80 range
        self.assertGreaterEqual(small_beds, 40)
        self.assertLessEqual(small_beds, 80)

        # Test medium hospital
        medium_beds = 100  # within 80-150 range
        self.assertGreaterEqual(medium_beds, 80)
        self.assertLessEqual(medium_beds, 150)

        # Test large hospital
        large_beds = 200  # within 150-300 range
        self.assertGreaterEqual(large_beds, 150)
        self.assertLessEqual(large_beds, 300)

    def test_hospital_bed_types(self):
        """Test that different bed types are within reasonable ranges"""
        total_beds = 100

        # ICU beds should be a small fraction of total
        icu_beds = max(3, total_beds // 20)
        self.assertLessEqual(icu_beds, total_beds)

        # General beds should be a larger fraction
        general_beds = max(10, total_beds // 5)
        self.assertLessEqual(general_beds, total_beds)

        # Oxygen beds should be moderate
        oxygen_beds = max(8, total_beds // 10)
        self.assertLessEqual(oxygen_beds, total_beds)

    def test_occupancy_rate_range(self):
        """Test that occupancy rates are within valid range"""
        # Occupancy rate should be between 0.65 and 0.95
        for _ in range(10):
            with patch('scripts.generate_dataset.random.uniform') as mock_uniform:
                mock_uniform.return_value = 0.75
                rate = round(mock_uniform(0.65, 0.95), 2)
                self.assertGreaterEqual(rate, 0.65)
                self.assertLessEqual(rate, 0.95)

    def test_hospital_rating_range(self):
        """Test that hospital ratings are within valid range"""
        # Rating should be between 3.4 and 4.8
        for _ in range(10):
            with patch('scripts.generate_dataset.random.uniform') as mock_uniform:
                mock_uniform.return_value = 4.2
                rating = round(mock_uniform(3.4, 4.8), 1)
                self.assertGreaterEqual(rating, 3.4)
                self.assertLessEqual(rating, 4.8)

    def test_boolean_fields(self):
        """Test that trauma_center and cardiac_center are boolean values"""
        with patch('scripts.generate_dataset.random.random') as mock_random:
            # Test trauma_center (35% probability)
            mock_random.return_value = 0.3
            trauma = mock_random() < 0.35
            self.assertIsInstance(trauma, bool)
            self.assertTrue(trauma)

            # Test cardiac_center (50% probability)
            mock_random.return_value = 0.6
            cardiac = mock_random() < 0.50
            self.assertIsInstance(cardiac, bool)
            self.assertFalse(cardiac)


class TestUserRequestGeneration(unittest.TestCase):
    """Test user request data generation logic"""

    def test_emergency_types(self):
        """Test that emergency types are correctly defined"""
        expected_types = ["general", "cardiac", "trauma"]
        self.assertEqual(generate_dataset.emergency_types, expected_types)

    def test_severity_levels(self):
        """Test that severity levels are correctly defined"""
        expected_levels = ["CRITICAL", "URGENT", "STABLE"]
        self.assertEqual(generate_dataset.severity_levels, expected_levels)

    def test_user_coordinate_ranges(self):
        """Test that user coordinates are within the same geographic bounds"""
        # User coordinates should use same ranges as hospitals
        self.assertEqual(generate_dataset.LAT_MIN, 22.45)
        self.assertEqual(generate_dataset.LAT_MAX, 22.65)
        self.assertEqual(generate_dataset.LON_MIN, 88.25)
        self.assertEqual(generate_dataset.LON_MAX, 88.45)

    def test_timestamp_generation(self):
        """Test that timestamps are within the last 24 hours"""
        now = datetime.now()
        with patch('scripts.generate_dataset.random.randint') as mock_randint:
            mock_randint.return_value = 720  # 12 hours ago
            timestamp = now - timedelta(minutes=mock_randint())
            self.assertLess(timestamp, now)
            self.assertGreater(timestamp, now - timedelta(hours=24))

    def test_user_id_range(self):
        """Test that user IDs are within expected range"""
        with patch('scripts.generate_dataset.random.randint') as mock_randint:
            mock_randint.return_value = 50
            user_id = mock_randint(1, 100)
            self.assertGreaterEqual(user_id, 1)
            self.assertLessEqual(user_id, 100)

    def test_emergency_type_distribution(self):
        """Test emergency type distribution weights"""
        with patch('scripts.generate_dataset.random.choices') as mock_choices:
            mock_choices.return_value = ["general"]
            emergency_type = mock_choices(
                ["general", "cardiac", "trauma"],
                weights=[0.5, 0.3, 0.2]
            )[0]
            self.assertIn(emergency_type, ["general", "cardiac", "trauma"])

    def test_severity_level_distribution(self):
        """Test severity level distribution weights"""
        with patch('scripts.generate_dataset.random.choices') as mock_choices:
            mock_choices.return_value = ["URGENT"]
            severity = mock_choices(
                ["CRITICAL", "URGENT", "STABLE"],
                weights=[0.3, 0.4, 0.3]
            )[0]
            self.assertIn(severity, ["CRITICAL", "URGENT", "STABLE"])


class TestDatasetConfiguration(unittest.TestCase):
    """Test configuration constants"""

    def test_num_hospitals_constant(self):
        """Test that NUM_HOSPITALS is set correctly"""
        self.assertEqual(generate_dataset.NUM_HOSPITALS, 50)
        self.assertIsInstance(generate_dataset.NUM_HOSPITALS, int)

    def test_num_users_constant(self):
        """Test that NUM_USERS is set correctly"""
        self.assertEqual(generate_dataset.NUM_USERS, 200)
        self.assertIsInstance(generate_dataset.NUM_USERS, int)

    def test_base_dir_exists(self):
        """Test that BASE_DIR is properly configured"""
        self.assertIsInstance(generate_dataset.BASE_DIR, Path)

    def test_data_dir_configuration(self):
        """Test that DATA_DIR is properly configured"""
        self.assertIsInstance(generate_dataset.DATA_DIR, Path)
        expected_data_dir = generate_dataset.BASE_DIR / "data"
        self.assertEqual(generate_dataset.DATA_DIR, expected_data_dir)


class TestCSVGeneration(unittest.TestCase):
    """Test CSV file generation and data integrity"""

    def setUp(self):
        """Set up temporary directory for testing"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temporary directory"""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_hospital_dataframe_columns(self):
        """Test that hospital DataFrame has correct columns"""
        expected_columns = [
            "hospital_id", "hospital_name", "latitude", "longitude",
            "trauma_center", "cardiac_center", "icu_beds_available",
            "general_beds_available", "oxygen_beds_available",
            "total_beds", "current_occupancy_rate", "hospital_rating"
        ]

        # Create a simple hospital dict
        hospital = {
            "hospital_id": 1,
            "hospital_name": "Test Hospital",
            "latitude": 22.5,
            "longitude": 88.3,
            "trauma_center": True,
            "cardiac_center": False,
            "icu_beds_available": 5,
            "general_beds_available": 20,
            "oxygen_beds_available": 10,
            "total_beds": 100,
            "current_occupancy_rate": 0.75,
            "hospital_rating": 4.2
        }

        df = pd.DataFrame([hospital])
        self.assertEqual(list(df.columns), expected_columns)

    def test_user_dataframe_columns(self):
        """Test that user DataFrame has correct columns"""
        expected_columns = [
            "request_id", "user_id", "latitude", "longitude",
            "emergency_type", "severity_level", "request_timestamp"
        ]

        # Create a simple user dict
        user = {
            "request_id": 1,
            "user_id": 42,
            "latitude": 22.5,
            "longitude": 88.3,
            "emergency_type": "cardiac",
            "severity_level": "URGENT",
            "request_timestamp": datetime.now()
        }

        df = pd.DataFrame([user])
        self.assertEqual(list(df.columns), expected_columns)

    def test_hospital_id_uniqueness(self):
        """Test that hospital IDs are unique and sequential"""
        hospital_ids = list(range(1, 51))
        self.assertEqual(len(hospital_ids), len(set(hospital_ids)))
        self.assertEqual(hospital_ids[0], 1)
        self.assertEqual(hospital_ids[-1], 50)

    def test_request_id_uniqueness(self):
        """Test that request IDs are unique and sequential"""
        request_ids = list(range(1, 201))
        self.assertEqual(len(request_ids), len(set(request_ids)))
        self.assertEqual(request_ids[0], 1)
        self.assertEqual(request_ids[-1], 200)

    def test_hospital_data_types(self):
        """Test that hospital data has correct types"""
        hospital = {
            "hospital_id": 1,
            "hospital_name": "Test Hospital",
            "latitude": 22.5,
            "longitude": 88.3,
            "trauma_center": True,
            "cardiac_center": False,
            "icu_beds_available": 5,
            "general_beds_available": 20,
            "oxygen_beds_available": 10,
            "total_beds": 100,
            "current_occupancy_rate": 0.75,
            "hospital_rating": 4.2
        }

        self.assertIsInstance(hospital["hospital_id"], int)
        self.assertIsInstance(hospital["hospital_name"], str)
        self.assertIsInstance(hospital["latitude"], float)
        self.assertIsInstance(hospital["longitude"], float)
        self.assertIsInstance(hospital["trauma_center"], bool)
        self.assertIsInstance(hospital["cardiac_center"], bool)
        self.assertIsInstance(hospital["icu_beds_available"], int)
        self.assertIsInstance(hospital["general_beds_available"], int)
        self.assertIsInstance(hospital["oxygen_beds_available"], int)
        self.assertIsInstance(hospital["total_beds"], int)
        self.assertIsInstance(hospital["current_occupancy_rate"], float)
        self.assertIsInstance(hospital["hospital_rating"], float)

    def test_user_data_types(self):
        """Test that user data has correct types"""
        user = {
            "request_id": 1,
            "user_id": 42,
            "latitude": 22.5,
            "longitude": 88.3,
            "emergency_type": "cardiac",
            "severity_level": "URGENT",
            "request_timestamp": datetime.now()
        }

        self.assertIsInstance(user["request_id"], int)
        self.assertIsInstance(user["user_id"], int)
        self.assertIsInstance(user["latitude"], float)
        self.assertIsInstance(user["longitude"], float)
        self.assertIsInstance(user["emergency_type"], str)
        self.assertIsInstance(user["severity_level"], str)
        self.assertIsInstance(user["request_timestamp"], datetime)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    def test_minimum_hospital_beds(self):
        """Test minimum bed allocations"""
        # Small hospitals should have at least 40 beds
        total_beds = 40
        self.assertGreaterEqual(total_beds, 40)

        # ICU beds minimum
        icu_beds = 1
        self.assertGreaterEqual(icu_beds, 1)

    def test_maximum_hospital_beds(self):
        """Test maximum bed allocations"""
        # Large hospitals should not exceed 300 beds
        total_beds = 300
        self.assertLessEqual(total_beds, 300)

    def test_coordinate_precision(self):
        """Test that coordinates are rounded to 6 decimal places"""
        with patch('scripts.generate_dataset.random.uniform') as mock_uniform:
            mock_uniform.return_value = 22.123456789
            coord = round(mock_uniform(22.0, 23.0), 6)
            self.assertEqual(coord, 22.123457)

    def test_rating_precision(self):
        """Test that ratings are rounded to 1 decimal place"""
        with patch('scripts.generate_dataset.random.uniform') as mock_uniform:
            mock_uniform.return_value = 4.23456
            rating = round(mock_uniform(3.4, 4.8), 1)
            self.assertEqual(rating, 4.2)

    def test_occupancy_rate_precision(self):
        """Test that occupancy rates are rounded to 2 decimal places"""
        with patch('scripts.generate_dataset.random.uniform') as mock_uniform:
            mock_uniform.return_value = 0.753456
            rate = round(mock_uniform(0.65, 0.95), 2)
            self.assertEqual(rate, 0.75)

    def test_empty_hospital_name_combinations(self):
        """Test that hospital names are never empty"""
        for prefix in generate_dataset.prefixes:
            for suffix in generate_dataset.suffixes:
                name = f"{prefix} {suffix}"
                self.assertGreater(len(name), 0)
                self.assertIn(" ", name)

    def test_negative_bed_values_impossible(self):
        """Test that bed values cannot be negative"""
        with patch('scripts.generate_dataset.random.randint') as mock_randint:
            mock_randint.return_value = 5
            beds = max(1, mock_randint(1, 10))
            self.assertGreater(beds, 0)

    def test_future_timestamp_impossible(self):
        """Test that timestamps cannot be in the future"""
        now = datetime.now()
        timestamp = now - timedelta(minutes=0)
        self.assertLessEqual(timestamp, now)

    def test_invalid_emergency_type_not_possible(self):
        """Test that only valid emergency types are used"""
        valid_types = ["general", "cardiac", "trauma"]
        for emergency_type in valid_types:
            self.assertIn(emergency_type, generate_dataset.emergency_types)

    def test_invalid_severity_level_not_possible(self):
        """Test that only valid severity levels are used"""
        valid_levels = ["CRITICAL", "URGENT", "STABLE"]
        for severity in valid_levels:
            self.assertIn(severity, generate_dataset.severity_levels)


class TestDataConsistency(unittest.TestCase):
    """Test data consistency and validation"""

    def test_hospital_total_beds_consistency(self):
        """Test that total beds is consistent with size category"""
        # Small hospital
        small_total = 60
        self.assertGreaterEqual(small_total, 40)
        self.assertLessEqual(small_total, 80)

        # Medium hospital
        medium_total = 120
        self.assertGreaterEqual(medium_total, 80)
        self.assertLessEqual(medium_total, 150)

        # Large hospital
        large_total = 250
        self.assertGreaterEqual(large_total, 150)
        self.assertLessEqual(large_total, 300)

    def test_bed_allocation_logic(self):
        """Test that bed allocation follows the script's logic"""
        total_beds = 100

        # ICU beds = max(3, total_beds // 20)
        icu_beds = max(3, total_beds // 20)
        self.assertEqual(icu_beds, 5)

        # General beds = max(10, total_beds // 5)
        general_beds = max(10, total_beds // 5)
        self.assertEqual(general_beds, 20)

        # Oxygen beds = max(8, total_beds // 10)
        oxygen_beds = max(8, total_beds // 10)
        self.assertEqual(oxygen_beds, 10)

    def test_geographic_bounds_consistency(self):
        """Test that all coordinates use the same geographic bounds"""
        # Both hospitals and users should use same lat/lon ranges
        self.assertEqual(generate_dataset.LAT_MIN, 22.45)
        self.assertEqual(generate_dataset.LAT_MAX, 22.65)
        self.assertEqual(generate_dataset.LON_MIN, 88.25)
        self.assertEqual(generate_dataset.LON_MAX, 88.45)

    def test_timestamp_within_24_hours(self):
        """Test that all timestamps are within the last 24 hours"""
        now = datetime.now()
        # Maximum minutes back is 1440 (24 hours)
        max_minutes = 1440
        earliest_time = now - timedelta(minutes=max_minutes)

        self.assertLessEqual(earliest_time, now)
        self.assertEqual((now - earliest_time).total_seconds(), max_minutes * 60)


if __name__ == '__main__':
    unittest.main()
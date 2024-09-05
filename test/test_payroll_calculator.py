import unittest
import sys
sys.path.append("src")

from logic.payroll_calculator import calculate_payroll, InvalidSalaryError, InvalidDaysWorkedError, InvalidHoursWorkedError, NegativeCommissionError, NegativeOvertimeHoursError

class TestPayrollCalculator(unittest.TestCase):

    # Normal Test Cases

    def test_overtime_without_commissions(self):
        result = calculate_payroll(salary=2000000, days_worked=30, hours_worked=8, commissions=0, overtime_hours=10)
        self.assertGreater(result["total_earned"], 2000000)
        self.assertEqual(result["health_deductions"], result["total_earned"] * 0.04)

    def test_commissions_without_overtime(self):
        result = calculate_payroll(salary=2000000, days_worked=30, hours_worked=8, commissions=2500000, overtime_hours=0)
        self.assertAlmostEqual(result["total_earned"], 4500000, places=2)

    def test_partial_days_worked(self):
        result = calculate_payroll(salary=2000000, days_worked=15, hours_worked=8, commissions=0, overtime_hours=0)
        self.assertAlmostEqual(result["total_earned"], 1000000, places=2)

    def test_all_standard_variables(self):
        result = calculate_payroll(salary=2000000, days_worked=30, hours_worked=8, commissions=100000, overtime_hours=5)
        self.assertGreater(result["total_earned"], 2000000)
        self.assertGreater(result["final_payroll"], 1840000)

    def test_salary_and_hours_without_days_worked(self):
        with self.assertRaises(InvalidDaysWorkedError):
            calculate_payroll(salary=2000000, days_worked=0, hours_worked=8, commissions=0, overtime_hours=40)

    def test_salary_with_only_days_worked(self):
        result = calculate_payroll(salary=2000000, days_worked=30, hours_worked=8, commissions=0, overtime_hours=0)
        self.assertAlmostEqual(result["total_earned"], 2000000, places=2)

    # Extraordinary Test Cases

    def test_salary_equal_to_4_smlv(self):
        result = calculate_payroll(salary=5200000, days_worked=30, hours_worked=8, commissions=0, overtime_hours=0)
        self.assertEqual(result["total_earned"], 5200000)
        self.assertEqual(result["health_deductions"], 208000)

    def test_salary_greater_than_4_smlv(self):
        result = calculate_payroll(salary=6000000, days_worked=30, hours_worked=8, commissions=1000000, overtime_hours=20)
        self.assertGreater(result["total_earned"], 6000000)
        self.assertGreater(result["final_payroll"], 5200000)

    def test_less_than_15_days_worked(self):
        result = calculate_payroll(salary=2000000, days_worked=10, hours_worked=8, commissions=0, overtime_hours=0)
        self.assertAlmostEqual(result["total_earned"], 666666.67, places=2)
        self.assertAlmostEqual(result["final_payroll"], 613333.33, places=2)

    def test_less_than_8_hours_worked(self):
        result = calculate_payroll(salary=2000000, days_worked=30, hours_worked=4, commissions=0, overtime_hours=0)
        self.assertGreater(result["total_earned"], 2000000)
        self.assertEqual(result["health_deductions"], result["total_earned"] * 0.04)

    def test_extremely_high_salary(self):
        result = calculate_payroll(salary=13000000, days_worked=30, hours_worked=8, commissions=0, overtime_hours=0)
        self.assertEqual(result["total_earned"], 13000000)
        self.assertEqual(result["health_deductions"], 520000)

    def test_significant_commissions(self):
        result = calculate_payroll(salary=2000000, days_worked=30, hours_worked=8, commissions=2000000, overtime_hours=0)
        self.assertEqual(result["total_earned"], 4000000)
        self.assertEqual(result["final_payroll"], 3680000)

    # Error Test Cases

    def test_zero_salary(self):
        with self.assertRaises(InvalidSalaryError):
            calculate_payroll(salary=0, days_worked=30, hours_worked=8, commissions=0, overtime_hours=0)

    def test_negative_salary(self):
        with self.assertRaises(InvalidSalaryError):
            calculate_payroll(salary=-1000000, days_worked=30, hours_worked=8, commissions=0, overtime_hours=0)

    def test_zero_days_worked(self):
        with self.assertRaises(InvalidDaysWorkedError):
            calculate_payroll(salary=2000000, days_worked=0, hours_worked=8, commissions=0, overtime_hours=0)

    def test_negative_days_worked(self):
        with self.assertRaises(InvalidDaysWorkedError):
            calculate_payroll(salary=2000000, days_worked=-5, hours_worked=8, commissions=0, overtime_hours=0)

    def test_negative_hours_worked(self):
        with self.assertRaises(InvalidHoursWorkedError):
            calculate_payroll(salary=2000000, days_worked=30, hours_worked=-8, commissions=0, overtime_hours=0)

    def test_negative_commissions(self):
        with self.assertRaises(NegativeCommissionError):
            calculate_payroll(salary=2000000, days_worked=30, hours_worked=8, commissions=-500000, overtime_hours=0)

if __name__ == '__main__':
    unittest.main()

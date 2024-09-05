class PayrollException(Exception):
    """Base class for payroll exceptions"""
    pass

class InvalidSalaryError(PayrollException):
    """Raised when the salary is less than or equal to zero"""
    pass

class InvalidDaysWorkedError(PayrollException):
    """Raised when the days worked are out of the valid range"""
    pass

class InvalidHoursWorkedError(PayrollException):
    """Raised when the hours worked are out of the valid range"""
    pass

class NegativeCommissionError(PayrollException):
    """Raised when the commissions are negative"""
    pass

class NegativeOvertimeHoursError(PayrollException):
    """Raised when the overtime hours are negative"""
    pass

def validate_inputs(salary, days_worked, hours_worked, commissions, overtime_hours):
    if salary <= 0:
        raise InvalidSalaryError("El sueldo debe ser mayor que 0")
    if days_worked <= 0 or days_worked > 30:
        raise InvalidDaysWorkedError("Los días trabajados deben estar entre 1 y 30")
    if hours_worked < 0 or hours_worked > 24:
        raise InvalidHoursWorkedError("Las horas trabajadas deben estar entre 0 y 24")
    if commissions < 0:
        raise NegativeCommissionError("Las comisiones no pueden ser negativas")
    if overtime_hours < 0:
        raise NegativeOvertimeHoursError("Las horas extras no pueden ser negativas")

def calculate_daily_payment(salary):
    return salary / 30

def calculate_hourly_payment(salary):
    return salary / 240

def calculate_overtime_payment(hourly_payment, overtime_hours):
    return hourly_payment * overtime_hours * 1.25

def calculate_health_deductions(total_earned):
    return total_earned * 0.04

def calculate_pension_deductions(total_earned):
    return total_earned * 0.04

def calculate_payroll(salary, days_worked, hours_worked, commissions, overtime_hours):
    validate_inputs(salary, days_worked, hours_worked, commissions, overtime_hours)

    daily_payment = calculate_daily_payment(salary)
    hourly_payment = calculate_hourly_payment(salary)
    overtime_payment = calculate_overtime_payment(hourly_payment, overtime_hours)

    total_earned = (daily_payment * days_worked) + commissions + overtime_payment
    health_deductions = calculate_health_deductions(total_earned)
    pension_deductions = calculate_pension_deductions(total_earned)

    total_deductions = health_deductions + pension_deductions
    final_payroll = total_earned - total_deductions

    return {
        "total_earned": total_earned,
        "health_deductions": health_deductions,
        "pension_deductions": pension_deductions,
        "total_deductions": total_deductions,
        "final_payroll": final_payroll
    }
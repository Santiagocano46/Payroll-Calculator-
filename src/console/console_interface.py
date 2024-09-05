import sys 
sys.path.append("src")

from logic.payroll_calculator import calculate_payroll, InvalidSalaryError, InvalidDaysWorkedError, InvalidHoursWorkedError, NegativeCommissionError, NegativeOvertimeHoursError

def get_user_input():
    name = input("Ingrese su nombre: ")
    salary = float(input("Ingrese su sueldo: "))
    days_worked = int(input("Ingrese los días trabajados: "))
    hours_worked = int(input("Ingrese las horas trabajadas por día: "))
    commissions = float(input("Ingrese las comisiones totales ganadas: "))
    overtime_hours = int(input("Ingrese las horas extras trabajadas: "))

    return name, salary, days_worked, hours_worked, commissions, overtime_hours

def display_payroll_info(name, payroll_info):
    print(f"\nHola {name}, aquí está la información de tu nómina:")
    print(f"Total Devengado: {payroll_info['total_earned']:.2f}")
    print(f"Deducciones por Salud: {payroll_info['health_deductions']:.2f}")
    print(f"Deducciones por Pensión: {payroll_info['pension_deductions']:.2f}")
    print(f"Total Deducido: {payroll_info['total_deductions']:.2f}")
    print(f"Nómina Final: {payroll_info['final_payroll']:.2f}")

def main():
    try:
        name, salary, days_worked, hours_worked, commissions, overtime_hours = get_user_input()
        payroll_info = calculate_payroll(salary, days_worked, hours_worked, commissions, overtime_hours)
        display_payroll_info(name, payroll_info)
    except (InvalidSalaryError, InvalidDaysWorkedError, InvalidHoursWorkedError, NegativeCommissionError, NegativeOvertimeHoursError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

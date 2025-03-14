package smartask.api.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import smartask.api.models.Employee;
import smartask.api.repositories.EmployeesRepository;

import java.util.*;

@Service
public class EmployeeService {
    @Autowired
    private EmployeesRepository repository;

    @Autowired
    private SequenceGeneratorService sequenceGeneratorService;

    public EmployeeService(EmployeesRepository repository) {
        this.repository = repository;
    }

    public List<Employee> getEmployees() {
        return repository.findAll();
    }

    public void addEmployee(Employee employee){
        saveEmployee(employee);
    }

    public Employee getEmployeeById(Long id){
        Optional<Employee> optionalEmployee = repository.findById(id);
        if (!optionalEmployee.isPresent()) {
            throw new IllegalArgumentException("Employee not found");
        }
        return optionalEmployee.get();
    }

    public void updateEmployee(Long id, Employee employee){
        Employee employeeToUpdate = getEmployeeById(id);
        employeeToUpdate.setName(employee.getName());
        employeeToUpdate.setTeam(employee.getTeam());
        saveEmployee(employeeToUpdate);
    }

    public void addRestrictionToEmployee(Long id, String restrictionType, String date) {
        Employee employee = getEmployeeById(id);
        if (employee.getRestrictions() == null) {
            employee.setRestrictions(new HashMap<>());
        }
        // employee.getRestrictions().computeIfAbsent(restrictionType, k -> new ArrayList<>());
        if (!employee.getRestrictions().get(restrictionType).contains(date)) {
            employee.getRestrictions().get(restrictionType).add(date);
        }
        updateEmployee(id, employee);
    }

    public void removeRestrictionFromEmployee(Long id, String restrictionType, String date) {
        Employee employee = getEmployeeById(id);
        if (employee.getRestrictions() == null) {
            return; 
        }
        List<String> dates = employee.getRestrictions().get(restrictionType);
        if (dates != null) {
            dates.remove(date);
            if (dates.isEmpty()) {
                employee.getRestrictions().remove(restrictionType);
            }
            updateEmployee(id, employee);
        }
    }

    public Map<String, List<String>> getEmployeeRestrictions(Long id) {
        Employee employee = getEmployeeById(id);
        return employee.getRestrictions() != null ? new HashMap<>(employee.getRestrictions()) : new HashMap<>();
    }

    public void saveEmployee(Employee employee) {
        if (employee.getId() == null) {
            employee.setId(sequenceGeneratorService.generateSequence("employees"));
        }
        repository.save(employee);
    }
}

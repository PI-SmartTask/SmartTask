package smartask.api.controllers;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import smartask.api.models.Employee;
import smartask.api.models.requests.RestrictionRequest;
import smartask.api.services.EmployeeService;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Tag(name = "Employee", description = "Employees Management")
@RestController
@RequestMapping("/api/v1/employees")
public class EmployeesController {

    @Autowired
    private EmployeeService employeeService;

    public EmployeesController(EmployeeService employeeService) {
        this.employeeService = employeeService;
    }

    @Operation(summary = "Get all employees")
    @GetMapping("/")
    public ResponseEntity<List<Employee>> getEmployees() {
        List<Employee> employees = employeeService.getEmployees();
        return new ResponseEntity<>(employees, HttpStatus.OK);
    }

    @Operation(summary = "Add a new employee")
    @PostMapping("/")
    public ResponseEntity<String> addEmployee(@RequestBody Employee employee) {
        employeeService.addEmployee(employee);
        return ResponseEntity.ok("Employee created successfully");
    }

    @Operation(
            summary = "Get an employee by name",
            description = "Searches for an employee by their name. If found, returns employee details; otherwise, returns a 404 Not Found response."
    )
    @GetMapping("/{name}")
    public ResponseEntity<Optional<Employee>> getEmpByName(@PathVariable String name) {
        if (employeeService.findByName(name).isPresent()) {
            return ResponseEntity.ok(employeeService.findByName(name));
        }
        return ResponseEntity.notFound().build();
    }

    @Operation(
            summary = "Get all the restriction to an employee by their name",
            description = "Searches for an employee by their name. If found, fetch all his restrictions"
    )
    @GetMapping("/restriction/{name}")
    public ResponseEntity<Map<String, List<String>>> getRestriction(@PathVariable String name) {
        return ResponseEntity.ok(employeeService.getEmployeeRestrictions(name));
    }

    @Operation(
            summary = "Add new restriction to an employee by their name",
            description = "Searches for an employee by their name. If found, add new restriction, e.g. search for [Joao] and add restriction [Fer] for the date [11/05]"
    )
    @PostMapping("/restriction/{name}")
    public ResponseEntity<String> addRestriction(@RequestBody RestrictionRequest restrictionRequest,
                                                 @PathVariable String name) {
        System.out.println(restrictionRequest+" for "+name);
        employeeService.addRestrictionToEmployee(name, restrictionRequest.getRestrictionType(), restrictionRequest.getDate());
        return ResponseEntity.ok("Restriction added successfully");
    }

    @Operation(
            summary = "Update new restriction to an employee by their name",
            description = "Searches for an employee by their name. If found, change the value of the restriction, e.g. search for [Joao] and change restriction [Fer] for the date [11/05]"
    )
    @PutMapping("/restriction/{name}")
    public ResponseEntity<String> updateRestriction(@RequestBody RestrictionRequest restrictionRequest,
                                                    @PathVariable String name) {
        System.out.println(restrictionRequest+" for "+name);
        // Process the received restrictionType and date
        return ResponseEntity.ok("Restriction update successfully");
    }

    @Operation(
            summary = "Delete new restriction to an employee by their name",
            description = "Searches for an employee by their name. If found, delete value of the restriction, e.g. search for [Joao] and  delete the date [11/05] for the restriction [Fer]"
    )
    @DeleteMapping("/restriction/{name}")
    public ResponseEntity<String> deleteRestriction(@RequestBody RestrictionRequest restrictionRequest,
                                                    @PathVariable String name) {
        System.out.println(restrictionRequest+" for "+name);
        employeeService.removeRestrictionFromEmployee(name, restrictionRequest.getRestrictionType(), restrictionRequest.getDate());
        return ResponseEntity.ok("Restriction deleted successfully");
    }
}

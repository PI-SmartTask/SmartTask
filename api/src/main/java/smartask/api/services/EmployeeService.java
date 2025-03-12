package smartask.api.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import smartask.api.models.Employee;
import smartask.api.repositories.EmployeesRepository;

import java.util.List;
import java.util.Optional;

@Service
public class EmployeeService {
    @Autowired
    private EmployeesRepository repository;

    public List<Employee> getAll(){
        return repository.findAll();
    }

    public Optional<Employee> findByName(String name){return repository.findByName(name);}
}

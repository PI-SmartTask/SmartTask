package smartask.api.repositories;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
import smartask.api.models.Employee;

import java.util.Optional;

@Repository
public interface EmployeesRepository extends MongoRepository<Employee, Long> {
    Optional<Employee> findById(Long id);
}

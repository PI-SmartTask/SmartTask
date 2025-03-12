
package smartask.api.services;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import smartask.api.models.Employee;
import smartask.api.models.Schedule;
import smartask.api.repositories.EmployeesRepository;
import smartask.api.repositories.FShandler;
import smartask.api.repositories.SchedulesRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class SchedulesService {

    private final FShandler FShandler = new FShandler();

    @Autowired
    private SchedulesRepository schedulerepository;

    @Autowired
    private EmployeesRepository Emprepository;

    public List<String[]> readex1() {
        saveSchedule();
        return FShandler.readex1();
    }

    private Schedule saveSchedule() {
        List<String[]> rawData = FShandler.readex1();
        List<List<String>> structuredData = rawData.stream()
                .map(List::of)
                .collect(Collectors.toList());

        // Extract employees from the CSV
        List<Employee> employees = new ArrayList<>();
        for (int i = 3; i < rawData.size(); i++) { // Start from index 3 to skip headers
            String[] row = rawData.get(i);
            if (row.length < 2 || row[1].isEmpty()) {
                continue;
            }
            String name = row[1];
            employees.add(new Employee(name));
        }
        Emprepository.saveAll(employees);

        Schedule schedule = new Schedule(structuredData);
        return schedulerepository.save(schedule);
    }

    public List<Schedule> getAllSchedules() {
        return schedulerepository.findAll();
    }
}
package smartask.api.controllers;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import smartask.api.models.Team;
import smartask.api.services.TeamService;
import java.util.List;

@Tag(name = "Team", description = "Teams Management")
@RestController
@RequestMapping("/api/v1/teams")
public class TeamController {
    @Autowired
    private TeamService teamService;

    public TeamController(TeamService teamService) {
        this.teamService = teamService;
    }

    @Operation(summary = "Get all teams")
    @GetMapping("/")
    public ResponseEntity<List<Team>> getTeams() {
        List<Team> teams = teamService.getTeams();
        return new ResponseEntity<>(teams, HttpStatus.OK);
    }

    @Operation(summary = "Get a team by ID")
    @GetMapping("/{id}")
    public ResponseEntity<Team> getTeamById(@PathVariable String id) {
        Team team = teamService.getTeamById(id);
        return new ResponseEntity<>(team, HttpStatus.OK);
    }

    @Operation(summary = "Add a new team")
    @PostMapping("/")
    public ResponseEntity<String> addTeam(@RequestBody Team team) {
        teamService.addTeam(team);
        return ResponseEntity.ok("Team created successfully");
    }

    @Operation(summary = "Update a team")
    @PutMapping("/{id}")
    public ResponseEntity<String> updateTeam(@RequestBody Team team, @PathVariable String id) {
        teamService.updateTeam(id, team);
        return ResponseEntity.ok("Team updated successfully");
    }

    
}

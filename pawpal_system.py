from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Task:
    """Represents one pet care activity."""

    title: str
    task_type: str
    duration_minutes: int
    priority: int
    preferred_time: str
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Return True if the task repeats."""
        return self.frequency.lower() in ["daily", "weekly"]

    def generate_next_occurrence(self) -> Optional["Task"]:
        """Create the next occurrence of a recurring task."""
        if not self.is_recurring():
            return None

        return Task(
            title=self.title,
            task_type=self.task_type,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            preferred_time=self.preferred_time,
            frequency=self.frequency,
            completed=False,
        )


@dataclass
class Pet:
    """Represents a pet and its care tasks."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> bool:
        """Remove a task by title."""
        for task in self.tasks:
            if task.title.lower() == task_title.lower():
                self.tasks.remove(task)
                return True

        return False

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Represents the pet owner."""

    name: str
    preferences: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet

        return None

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks = []

        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())

        return all_tasks


class Scheduler:
    """Organizes tasks into a daily pet care plan."""

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority."""
        return sorted(tasks, key=lambda task: task.priority)

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by preferred time."""
        return sorted(tasks, key=lambda task: task.preferred_time)

    def generate_daily_plan(self, owner: Owner, available_minutes: int) -> List[Task]:
        """Generate a daily plan based on task priority and available time."""
        tasks = self.sort_tasks_by_priority(owner.get_all_tasks())

        plan = []
        used_minutes = 0

        for task in tasks:
            if task.completed:
                continue

            if used_minutes + task.duration_minutes <= available_minutes:
                plan.append(task)
                used_minutes += task.duration_minutes

        return self.sort_tasks_by_time(plan)

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect tasks with the same preferred time."""
        conflicts = []
        seen_times = {}

        for task in tasks:
            if task.preferred_time in seen_times:
                conflicts.append(
                    f"Conflict: {task.title} and {seen_times[task.preferred_time]} "
                    f"are both scheduled at {task.preferred_time}."
                )
            else:
                seen_times[task.preferred_time] = task.title

        return conflicts

    def explain_plan(self, plan: List[Task]) -> str:
        """Explain why the scheduler chose this plan."""
        if not plan:
            return "No tasks were selected because there were no available tasks or not enough available time."

        explanation = "This plan was selected by prioritizing important incomplete tasks that fit within the available time."

        return explanation
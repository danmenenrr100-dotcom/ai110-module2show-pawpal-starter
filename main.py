from pawpal_system import Owner, Pet, Scheduler, Task


def print_plan(owner, plan, scheduler):
    print(f"Daily Plan for {owner.name}")
    print("-" * 40)

    if not plan:
        print("No tasks were scheduled.")
        return

    for task in plan:
        print(
            f"{task.preferred_time} — {task.title} "
            f"({task.duration_minutes} min) "
            f"[priority: {task.priority}]"
        )

    print()
    print("Explanation:")
    print(scheduler.explain_plan(plan))


def main():
    owner = Owner(name="Danny", preferences="Prioritize medication and walks first.")

    dog = Pet(name="Max", species="Dog", age=4)
    cat = Pet(name="Luna", species="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            title="Morning Walk",
            task_type="Walk",
            duration_minutes=30,
            priority=1,
            preferred_time="08:00",
            frequency="daily",
        )
    )

    dog.add_task(
        Task(
            title="Breakfast",
            task_type="Feeding",
            duration_minutes=10,
            priority=2,
            preferred_time="09:00",
            frequency="daily",
        )
    )

    cat.add_task(
        Task(
            title="Medication",
            task_type="Medication",
            duration_minutes=5,
            priority=1,
            preferred_time="08:00",
            frequency="once",
        )
    )

    scheduler = Scheduler()

    plan = scheduler.generate_daily_plan(owner, available_minutes=60)
    print_plan(owner, plan, scheduler)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    print()
    print("Conflict Check")
    print("-" * 40)

    if conflicts:
        for conflict in conflicts:
            print(conflict)
    else:
        print("No conflicts found.")


if __name__ == "__main__":
    main()
    
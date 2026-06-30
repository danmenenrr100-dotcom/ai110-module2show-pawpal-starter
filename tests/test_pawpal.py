from pawpal_system import Pet, Task


def test_task_completion():
    task = Task(
        title="Morning Walk",
        task_type="Walk",
        duration_minutes=30,
        priority=1,
        preferred_time="08:00",
        frequency="daily",
    )

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_task_addition_to_pet():
    pet = Pet(name="Max", species="Dog", age=4)

    task = Task(
        title="Breakfast",
        task_type="Feeding",
        duration_minutes=10,
        priority=2,
        preferred_time="09:00",
        frequency="daily",
    )

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] == task
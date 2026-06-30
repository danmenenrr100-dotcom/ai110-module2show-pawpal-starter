import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")


if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Owner")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler


def task_records_to_rows(records):
    """Convert pet-task records into table rows."""
    rows = []

    for pet, task in records:
        rows.append(
            {
                "Pet": pet.name,
                "Species": pet.species,
                "Time": task.preferred_time,
                "Task": task.title,
                "Type": task.task_type,
                "Duration": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": "Done" if task.completed else "Pending",
            }
        )

    return rows


def tasks_to_rows(tasks):
    """Convert task objects into table rows."""
    rows = []

    for task in tasks:
        rows.append(
            {
                "Time": task.preferred_time,
                "Task": task.title,
                "Type": task.task_type,
                "Duration": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": "Done" if task.completed else "Pending",
            }
        )

    return rows


st.title("🐾 PawPal+")
st.write(
    "Smart pet care planning for daily routines, priorities, available time, "
    "recurring tasks, and conflict warnings."
)


# -----------------------------
# Dashboard
# -----------------------------
all_records = scheduler.get_task_records(owner)
pending_records = scheduler.filter_tasks(owner, completed=False)
completed_records = scheduler.filter_tasks(owner, completed=True)
pending_tasks = [task for _, task in pending_records]
conflicts = scheduler.detect_conflicts(pending_tasks)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Pets", len(owner.pets))

with col2:
    st.metric("Total Tasks", len(all_records))

with col3:
    st.metric("Pending Tasks", len(pending_records))

with col4:
    st.metric("Conflicts", len(conflicts))


# -----------------------------
# Owner Info
# -----------------------------
st.header("Owner Info")

owner_name = st.text_input("Owner name", value=owner.name)
preferences = st.text_area("Owner preferences", value=owner.preferences)

if st.button("Update Owner Info"):
    owner.name = owner_name.strip() or "Pet Owner"
    owner.preferences = preferences.strip()
    st.success("Owner information updated.")


# -----------------------------
# Add Pet
# -----------------------------
st.header("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=1)

    add_pet_submitted = st.form_submit_button("Add Pet")

    if add_pet_submitted:
        if not pet_name.strip():
            st.error("Please enter a pet name.")
        elif owner.find_pet(pet_name.strip()):
            st.warning("A pet with that name already exists.")
        else:
            pet = Pet(name=pet_name.strip(), species=species, age=int(age))
            owner.add_pet(pet)
            st.success(f"{pet.name} was added.")
            st.rerun()


# -----------------------------
# Pet Table
# -----------------------------
st.header("Your Pets")

if not owner.pets:
    st.info("No pets added yet.")
else:
    pet_rows = []

    for pet in owner.pets:
        pet_rows.append(
            {
                "Name": pet.name,
                "Species": pet.species,
                "Age": pet.age,
                "Tasks": len(pet.tasks),
            }
        )

    st.table(pet_rows)


# -----------------------------
# Add Task
# -----------------------------
st.header("Add a Care Task")

if not owner.pets:
    st.warning("Add at least one pet before creating tasks.")
else:
    pet_names = [pet.name for pet in owner.pets]

    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Choose pet", pet_names)
        task_title = st.text_input("Task title")
        task_type = st.selectbox(
            "Task type",
            ["Walk", "Feeding", "Medication", "Grooming", "Enrichment", "Other"],
        )
        duration_minutes = st.number_input(
            "Duration in minutes",
            min_value=1,
            max_value=240,
            value=20,
        )
        priority = st.selectbox(
            "Priority",
            options=[1, 2, 3],
            format_func=lambda value: {1: "High", 2: "Medium", 3: "Low"}[value],
        )
        preferred_time = st.text_input("Preferred time", value="08:00")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

        add_task_submitted = st.form_submit_button("Add Task")

        if add_task_submitted:
            selected_pet = owner.find_pet(selected_pet_name)

            if selected_pet is None:
                st.error("Selected pet was not found.")
            elif not task_title.strip():
                st.error("Please enter a task title.")
            elif not preferred_time.strip():
                st.error("Please enter a preferred time.")
            else:
                task = Task(
                    title=task_title.strip(),
                    task_type=task_type,
                    duration_minutes=int(duration_minutes),
                    priority=int(priority),
                    preferred_time=preferred_time.strip(),
                    frequency=frequency,
                )

                selected_pet.add_task(task)
                st.success(f"Task added for {selected_pet.name}.")
                st.rerun()


# -----------------------------
# Generate Daily Schedule
# -----------------------------
st.header("Generate Daily Schedule")

available_minutes = st.number_input(
    "Available care time today in minutes",
    min_value=1,
    max_value=480,
    value=60,
)

if st.button("Generate Schedule"):
    plan = scheduler.generate_daily_plan(owner, int(available_minutes))

    if not plan:
        st.warning("No tasks fit into the available time.")
    else:
        st.success("Daily schedule generated.")
        st.table(tasks_to_rows(plan))

        st.subheader("Plan Explanation")
        st.write(scheduler.explain_plan(plan))


# -----------------------------
# Smart Filters
# -----------------------------
st.header("Smart Task Filters")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    pet_filter_options = ["All Pets"] + [pet.name for pet in owner.pets]
    selected_pet_filter = st.selectbox("Filter by pet", pet_filter_options)

with filter_col2:
    selected_status_filter = st.selectbox("Filter by status", ["All", "Pending", "Done"])

with filter_col3:
    selected_type_filter = st.selectbox(
        "Filter by task type",
        ["All", "Walk", "Feeding", "Medication", "Grooming", "Enrichment", "Other"],
    )

pet_filter = None if selected_pet_filter == "All Pets" else selected_pet_filter

if selected_status_filter == "Pending":
    completed_filter = False
elif selected_status_filter == "Done":
    completed_filter = True
else:
    completed_filter = None

task_type_filter = None if selected_type_filter == "All" else selected_type_filter

filtered_records = scheduler.filter_tasks(
    owner,
    pet_name=pet_filter,
    completed=completed_filter,
    task_type=task_type_filter,
)

if not filtered_records:
    st.info("No tasks match the selected filters.")
else:
    sorted_filtered_records = sorted(
        filtered_records,
        key=lambda record: record[1].preferred_time,
    )
    st.table(task_records_to_rows(sorted_filtered_records))


# -----------------------------
# Complete Tasks
# -----------------------------
st.header("Complete a Task")

pending_records = scheduler.filter_tasks(owner, completed=False)

if not pending_records:
    st.success("No pending tasks. Great job!")
else:
    sorted_pending_records = sorted(
        pending_records,
        key=lambda record: record[1].preferred_time,
    )

    for index, (pet, task) in enumerate(sorted_pending_records):
        col_a, col_b = st.columns([4, 1])

        with col_a:
            st.write(
                f"**{task.preferred_time}** — {pet.name}: "
                f"{task.title} ({task.duration_minutes} min, {task.frequency})"
            )

        with col_b:
            if st.button("Complete", key=f"complete_{index}_{pet.name}_{task.title}"):
                scheduler.mark_task_complete(pet, task.title)
                st.success(f"Completed {task.title} for {pet.name}.")

                if task.frequency.lower() in ["daily", "weekly"]:
                    st.info("A new recurring task was automatically created.")

                st.rerun()


# -----------------------------
# Conflict Warnings
# -----------------------------
st.header("Conflict Warnings")

pending_records = scheduler.filter_tasks(owner, completed=False)
pending_tasks = [task for _, task in pending_records]
conflicts = scheduler.detect_conflicts(pending_tasks)

if not conflicts:
    st.success("No conflicts found.")
else:
    st.warning(
        "The scheduler found tasks with the same preferred time. "
        "Review these warnings and consider changing one task time."
    )

    for conflict in conflicts:
        st.error(conflict)


# -----------------------------
# All Tasks Sorted
# -----------------------------
st.header("All Tasks Sorted by Time")

all_records = scheduler.get_task_records(owner)

if not all_records:
    st.info("No tasks have been added yet.")
else:
    sorted_records = sorted(all_records, key=lambda record: record[1].preferred_time)
    st.table(task_records_to_rows(sorted_records))
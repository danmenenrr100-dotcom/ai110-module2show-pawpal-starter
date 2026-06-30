import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Pet Owner")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler


st.title("🐾 PawPal+")
st.write("Smart pet care planning for daily routines, priorities, and available time.")


st.header("Owner Info")

owner_name = st.text_input("Owner name", value=owner.name)
preferences = st.text_area("Owner preferences", value=owner.preferences)

if st.button("Update Owner Info"):
    owner.name = owner_name
    owner.preferences = preferences
    st.success("Owner information updated.")


st.header("Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=50, value=1)

    add_pet_submitted = st.form_submit_button("Add Pet")

    if add_pet_submitted:
        if pet_name.strip():
            pet = Pet(name=pet_name.strip(), species=species, age=int(age))
            owner.add_pet(pet)
            st.success(f"{pet.name} was added.")
        else:
            st.error("Please enter a pet name.")


st.header("Your Pets")

if not owner.pets:
    st.info("No pets added yet.")
else:
    pet_data = []

    for pet in owner.pets:
        pet_data.append(
            {
                "Name": pet.name,
                "Species": pet.species,
                "Age": pet.age,
                "Tasks": len(pet.tasks),
            }
        )

    st.table(pet_data)


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
            format_func=lambda value: {
                1: "High",
                2: "Medium",
                3: "Low",
            }[value],
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

        schedule_rows = []

        for task in plan:
            schedule_rows.append(
                {
                    "Time": task.preferred_time,
                    "Task": task.title,
                    "Type": task.task_type,
                    "Duration": task.duration_minutes,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Completed": task.completed,
                }
            )

        st.table(schedule_rows)

        st.subheader("Plan Explanation")
        st.write(scheduler.explain_plan(plan))

        conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

        st.subheader("Conflict Warnings")

        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.success("No conflicts found.")
            
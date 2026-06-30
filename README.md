# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit pet care planning app that helps a pet owner manage daily care tasks for their pets. The app allows users to enter owner and pet information, add pet care tasks, generate a daily plan, detect scheduling conflicts, and explain why a schedule was chosen.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks such as walks, feedings, medications, enrichment, grooming, and appointments
- Consider constraints such as available time, priority, and owner preferences
- Produce a daily care plan
- Explain why the plan was chosen

This project follows a design-first workflow. I first created a UML diagram, then implemented the backend logic in Python, verified it through a CLI demo and pytest tests, and finally connected the logic to a Streamlit UI.

## Features

PawPal+ includes the following features:

- Enter owner information and preferences
- Add pet profiles with name, species, and age
- Add care tasks for each pet
- Store task details including duration, priority, preferred time, frequency, and completion status
- Generate a daily schedule based on available care time and task priority
- Display the generated plan clearly
- Explain why the scheduler selected the plan
- Filter tasks by pet, task type, and completion status
- Detect conflicts when two tasks share the same preferred time
- Mark tasks as complete
- Automatically create a new task when a daily or weekly recurring task is completed
- Verify backend logic with automated pytest tests

## Project Structure

```text
ai110-module2show-pawpal-starter/
├── app.py
├── main.py
├── pawpal_system.py
├── README.md
├── reflection.md
├── requirements.txt
├── diagrams/
│   ├── uml_draft.mmd
│   └── uml_final.mmd
└── tests/
    └── test_pawpal.py

    
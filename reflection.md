# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?


duration + priority
daily schedule/plan
constraints
explanation of reasoning
tests for scheduling behavior


## 1a. Initial design

For the initial design of PawPal+, I chose four main classes: Owner, Pet, Task, and Scheduler.

The Owner class represents the person using the app. It stores the owner’s name, preferences, and pets. The Pet class represents each animal and stores details such as name, species, age, and the pet’s care tasks. The Task class represents one care activity, such as feeding, walking, medication, grooming, or enrichment. Each task stores details like duration, priority, preferred time, frequency, and completion status. The Scheduler class is responsible for organizing tasks into a daily plan, sorting tasks by priority or time, detecting conflicts, and explaining why a plan was chosen.

I chose this structure because it matches the real-world relationship of the system: an owner has pets, pets have tasks, and the scheduler organizes those tasks into a useful care plan.

In Phase 2, I translated my UML design into working Python code. I implemented the Owner, Pet, Task, and Scheduler classes in `pawpal_system.py`. The Owner class manages pets, the Pet class stores care tasks, the Task class tracks details like duration, priority, preferred time, frequency, and completion status, and the Scheduler class generates a daily care plan based on available time and task priority.

I verified the backend logic using a CLI-first workflow by creating `main.py`. This helped me confirm that the system could create pets, add tasks, generate a daily plan, explain the plan, and detect scheduling conflicts before connecting anything to the Streamlit interface. I also added initial pytest tests for task completion and adding tasks to a pet.

2b. Tradeoffs

One tradeoff in my scheduler is that conflict detection only checks for exact matching preferred times. For example, if two tasks are both scheduled at 08:00, the system flags a conflict. However, it does not detect overlapping durations, such as one task from 08:00–08:30 and another task at 08:15.

I chose this simpler approach because my current Task class stores a preferred time and duration, but the conflict detection logic is still lightweight. This keeps the algorithm easier to understand and test. A future improvement would be to calculate start and end times so PawPal+ can detect real overlapping task windows.

### a. What went well

The part of this project I am most satisfied with is the way the backend logic, CLI demo, tests, and Streamlit UI now work together. I started with a UML design, translated it into Python classes, tested the logic in `main.py`, and then connected it to the app interface. The Scheduler class became the main logic layer for sorting tasks, filtering tasks, generating a daily plan, detecting conflicts, and explaining the schedule.

The AI coding assistant was most helpful for brainstorming the class structure, generating method skeletons, suggesting scheduling algorithms, and helping create pytest tests. It helped me move faster, but I still had to review the code and decide what matched the project requirements.

One AI suggestion I rejected was using a separate `pawpal.py` file instead of the required `pawpal_system.py`. I kept the project aligned with the assignment instructions by using `pawpal_system.py` as the main logic layer.

Using separate work phases helped me stay organized. I handled UML design first, then backend implementation, then UI integration, then algorithms, then tests, then final documentation. This made the project easier to manage and prevented me from mixing too many tasks at once.

### b. What you would improve

If I had another iteration, I would improve the scheduler by detecting overlapping task durations instead of only checking exact matching preferred times. Right now, the system can detect two tasks both scheduled at `08:00`, but it does not detect a task from `08:00–08:30` overlapping with another task at `08:15`.

I would also add persistent data storage so pets and tasks remain saved after the Streamlit app closes. Another improvement would be stronger input validation for preferred time formatting, such as requiring `HH:MM` format.

This project helped me understand that being the lead architect means I cannot blindly accept AI-generated code. I need to review the design, keep the system simple, follow the assignment requirements, and make the final decisions about what belongs in the project.


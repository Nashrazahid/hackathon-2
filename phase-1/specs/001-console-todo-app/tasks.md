---
description: "Task list for Console Todo Application implementation"
---

# Tasks: Console Todo Application

**Input**: Design documents from `/specs/001-console-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests will be included as specified in the plan.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan with src/, tests/ directories
- [x] T002 [P] Create src/models/, src/services/, src/controllers/, src/utils/ directories
- [x] T003 [P] Create tests/unit/, tests/integration/, tests/contract/ directories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Create Task model in src/models/task.py with id, title, description, completed fields
- [x] T005 [P] Create validation utilities in src/utils/validation.py for input validation
- [x] T006 Create TodoService in src/services/todo_service.py with in-memory storage
- [x] T007 Create TodoController in src/controllers/todo_controller.py to handle business logic

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Tasks (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks with title and description to the in-memory storage

**Independent Test**: Can be fully tested by running the add command with valid inputs and verifying the task is created and displayed in the system, delivering the core value of task creation.

### Tests for User Story 1 (OPTIONAL - included based on plan) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T008 [P] [US1] Create unit test for Task model in tests/unit/test_task.py
- [x] T009 [P] [US1] Create unit test for add_task functionality in tests/unit/test_todo_service.py
- [x] T010 [P] [US1] Create controller test for add task validation in tests/unit/test_todo_controller.py

### Implementation for User Story 1

- [x] T011 [US1] Implement Task model with validation rules from data-model.md in src/models/task.py
- [x] T012 [US1] Implement add_task method in TodoService in src/services/todo_service.py
- [x] T013 [US1] Implement add_task validation in TodoController in src/controllers/todo_controller.py
- [x] T014 [US1] Add CLI command for adding tasks to main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View and List Tasks (Priority: P1)

**Goal**: Allow users to view all tasks with their details (title, description, completion status) in a clear format

**Independent Test**: Can be fully tested by adding tasks and then using the list command to verify all tasks are displayed correctly with their details, delivering the core value of task visibility.

### Tests for User Story 2 (OPTIONAL - included based on plan) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T015 [P] [US2] Create unit test for list_tasks functionality in tests/unit/test_todo_service.py
- [x] T016 [P] [US2] Create controller test for list tasks in tests/unit/test_todo_controller.py

### Implementation for User Story 2

- [x] T017 [US2] Implement list_tasks method in TodoService in src/services/todo_service.py
- [x] T018 [US2] Implement list_tasks method in TodoController in src/controllers/todo_controller.py
- [x] T019 [US2] Add CLI command for listing tasks to main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Mark Tasks Complete (Priority: P2)

**Goal**: Allow users to update existing tasks or mark them as complete/incomplete

**Independent Test**: Can be fully tested by creating tasks, updating them with new information or completion status, and verifying the changes are reflected, delivering the value of task management.

### Tests for User Story 3 (OPTIONAL - included based on plan) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T020 [P] [US3] Create unit test for update_task functionality in tests/unit/test_todo_service.py
- [x] T021 [P] [US3] Create unit test for mark_complete functionality in tests/unit/test_todo_service.py
- [x] T022 [P] [US3] Create controller test for update task validation in tests/unit/test_todo_controller.py

### Implementation for User Story 3

- [x] T023 [US3] Implement update_task method in TodoService in src/services/todo_service.py
- [x] T024 [US3] Implement mark_complete method in TodoService in src/services/todo_service.py
- [x] T025 [US3] Implement update_task validation in TodoController in src/controllers/todo_controller.py
- [x] T026 [US3] Add CLI command for updating tasks to main.py
- [x] T027 [US3] Add CLI command for marking tasks complete to main.py

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Allow users to remove tasks from the in-memory storage

**Independent Test**: Can be fully tested by creating tasks, deleting them, and verifying they no longer appear in the task list, delivering the value of task removal.

### Tests for User Story 4 (OPTIONAL - included based on plan) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T028 [P] [US4] Create unit test for delete_task functionality in tests/unit/test_todo_service.py
- [ ] T029 [P] [US4] Create controller test for delete task validation in tests/unit/test_todo_controller.py

### Implementation for User Story 4

- [x] T030 [US4] Implement delete_task method in TodoService in src/services/todo_service.py
- [x] T031 [US4] Implement delete_task validation in TodoController in src/controllers/todo_controller.py
- [x] T032 [US4] Add CLI command for deleting tasks to main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T033 [P] Create main.py with CLI loop and menu options following contracts/cli-contracts.md
- [x] T034 [P] Add error handling throughout all layers based on validation contracts
- [x] T035 [P] Create integration tests for CLI flows in tests/integration/test_cli_flow.py
- [x] T036 [P] Create contract tests for CLI commands in tests/contract/test_cli_contracts.py
- [x] T037 [P] Add input validation helpers in src/utils/validation.py
- [x] T038 [P] Add console formatting helpers in src/utils/validation.py
- [x] T039 [P] Add comprehensive error messages following contracts/cli-contracts.md
- [x] T040 [P] Add help command implementation to main.py
- [x] T041 [P] Add exit command implementation to main.py
- [x] T042 [P] Add comprehensive documentation comments to all modules
- [x] T043 [P] Run quickstart.md validation to ensure all features work as described

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Create unit test for Task model in tests/unit/test_task.py"
Task: "Create unit test for add_task functionality in tests/unit/test_todo_service.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with validation rules from data-model.md in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
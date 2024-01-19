# Improvements that can be made.

## Separating business logic from models to its separate service.

### Current scenario.

Currently, the business logic is tightly integrated with Flask models, presenting challenges in readability and maintainability as the codebase expands to 20-30 modules. A more modular and organized architecture is needed to address these issues.

```
class Assignment(FyleBaseModel):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'),
    ...

    @classmethod
    def upsert(cls, assignment_new: 'Assignment'):
        ...
        
    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        ...
```


### Problem with this approach.

1) Scaling
    - Difficulty in managing and scaling as the codebase grows.
2)  Fat models
    - Models become bulky with business logic, violating the principle of thin models.
3)  Everything related to the model will need to be put here.
4)  Too much coupling in the model layer
    - High coupling between models and business logic reduces flexibility.
5) Against DRY principle
6) Testing and Mocking Difficulties:
    - Testing becomes complex with tightly coupled models, and mocking requires database interactions.

## Solution

To make your code more organized and easier to maintain, it's better to separate the business logic into its class, known as a service layer. This service layer can then be called by the API layer, and then the service layer can communicate with the model layer.
<img width="1138" alt="Screenshot 2024-01-19 at 2 21 27 PM" src="https://github.com/loharvikas/fyle-interview-intern-backend/assets/56187207/feac69aa-7569-423c-97d4-151dcaacb50d">

#### Model Layer

```
class Assignment(FyleBaseModel):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'),
    ...
```

#### Service Layer
```
class AssignmentService:
    @classmethod
    def upsert_assignment(cls, assignment_new: 'Assignment'):
        # Business logic for upserting assignments

    @classmethod
    def submit_assignment(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        # Business logic for submitting assignments
```

####  API Layer
```
 from assignment_service import AssignmentService

class AssignmentAPI:
    @classmethod
    def upsert_assignment(cls, assignment_new: 'Assignment'):
        AssignmentService.upsert_assignment(assignment_new)

    @classmethod
    def submit_assignment(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        AssignmentService.submit_assignment(_id, teacher_id, auth_principal)
```
## Benefits

- Less Coupling
- Isolation at the Feature level
- If we want to implement a feature for more than one entity we don’t write business logic for each entity
- Testing
- Avoid needless Abstraction
- DRY Principle
- More scalable
- Because of isolation, the same logic can be used anywhere (e.g Asynchronous task)

# Authentication mechanism

Currently, there is no authentication protocol being used, information inside the header is plain text which is not secure, protocols like JWT can be used.



# Improvements that can be made.

## Seprating business logic from models to its seperate service.

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
    - High coupling between models and business logic reduce flexibility.
5) Against DRY principle
6) Violation of Single Responsibility Principle (SRP):
7) Testing and Mocking Difficulties:
    - Testing becomes complex with tightly coupled models, and mocking requires database interactions.

## Solution

The business logic should be seprated into its own class (service layer) . API layer should directly talk to service layer and service layer will communicate to model layer

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

Currently there is no authenticaiton porotocol being used, information inside header is plain text which is not secure, protocals like JWT can be used.



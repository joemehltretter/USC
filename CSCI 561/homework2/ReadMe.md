# CSCI 561 - Assignment Two

AI algorithms to solve constraint satisfaction problems.

### Key Information:
    
    - Continental Confederation: AFC (Asia), CAF (Africa), CONCACAF (North and Central America),
        CONMEBOL (South Africa), OFC (Ocenia), UEFA (Europe)
    - Pot 1 must have Russia and the 2nd highest Ranked team from 2017.
    - Pot 2 to Pot K contain the next N(i) highest-ranked teams.
        i = 2, ... , K
### Guide:

    1) Number of groups given via script
    2) Assign teams to group 
        a. Teams within assigned group will all play each other.
        b. Because of that we must assign distribute teams in a balance
           based on geography and capabilities and constraints.

### Constraints:

    1) No group can have more than one team from any pot
    2) No group can have more than one team from any continental confederation,
       with exception to UEFA, which can have up to two teams in a group.
       
### CSP Assignments:

   - Variables = Teams
   - Variable Assignment = Group
   - Domains = Group

### Constraint Programming  
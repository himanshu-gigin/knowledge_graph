Graph Explanation
Classes:

JobRole includes an instance Sales Executive.
Skill includes CRM and Negotiation Skills.
Qualification includes Degree in Business Administration and Professional Certification in Sales.
Properties:

requiresSkill: Links Sales Executive to CRM and Negotiation Skills.
name: Provides a literal name for each instance.


Visualization of the RDF Graph
The graph would look like this:

Sales Executive → requiresSkill → CRM
Sales Executive → requiresSkill → Negotiation Skills
CRM → name → "Customer Relationship Management"
Negotiation Skills → name → "Negotiation Skills"
Degree in Business Administration → name → "Degree in Business Administration"
Professional Certification in Sales → name → "Professional Certification in Sales"
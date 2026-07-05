# placement-portal-v2
a placement portal for college admins to create placement drives, and student to have the opportunity to apply to those placement drives

# notes on backend
- this shit is not production ready, backend lacks input validation through pydantic, lacks type hints of primitives and non-primitives, and extensive security aware practices through decorators and middlewares, so please bear with me because this is GOD DAMN MAD2 proj
- I don't want you to drive me nuts for creating a slightly normalized setup of tables and not thinking about system design and security of the server
- tho I'm doing a basic request input validation through reqparser, also felt a big itch to make a graphQL API through strawberry instead of a vanilla HTTP but hey again this is GOD DAMN MAD2 proj
- uuids (universally unique identifiers, for reference) are not used for primary keys in db tables, for obvious reasons this project won't turn into distributed systems so therefore avoiding uuids for simplicity
- There is new HTTP Query method along with good packages like APIFlask (built in support for API docs generation, input built in input validation for APIs), all of these good practices have been avoided because we don't know who the proctor on the other side might be

# notes on frontend
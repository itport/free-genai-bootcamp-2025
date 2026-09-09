# GenAI Architecture Exercise

## Scenario

A language school wants to serve approximately 300 students in Nagasaki while keeping user data and licensed teaching material under its control. The initial hardware budget is USD 10,000–15,000.

## Proposed direction

- host an open-weight language model on school-controlled hardware;
- expose the service through an authenticated application rather than the model server itself;
- keep licensed learning materials in a controlled content store;
- monitor latency, concurrent usage, storage, backups, and network capacity;
- test a smaller pilot before purchasing final hardware.

IBM Granite was considered because its licensing and model documentation may make it easier to assess provenance and permitted use. Model, license, and hardware choices still require verification against the final workload.

## Assumptions and risks

The budget is an input, not proof that one workstation can reliably support 300 active students. A production proposal would first measure concurrency, prompt and response sizes, acceptable latency, model quantization, context-window requirements, and internet capacity. It would also define authentication, encryption, patching, logging, backup, recovery, and content-rights controls.

This document is an architecture exercise; it is not a production capacity guarantee.

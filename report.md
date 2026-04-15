26. Why does the request use a client-generated id rather than a server-generated one?
What problem does this solve in distributed systems?

A client-generated id lets the client identify what the task is before sending it. This is useful in distributed systems because
requests may be retried or processed by different servers. If the client knows their task ID, they can match the response
to the original request and see if there are any duplicate submissions and retry.

27. The status.state can be 'working'. Under what circumstances would a server return this
state in a non-streaming call, and how should a client react?

A server might return a status of 'working' in a non-streaming call when the task has been accepted but
not finished processing yet. This could happen with long works like web searches, large summary tasks or analysis. The client
can treat the response as not yet completed and not treat it as the final result.

28. What is the purpose of the sessionId field? Give a concrete example of two related tasks
that should share a session.

The sessionId field groups related tasks into the same workflow context. It allows the server to understand that
separate requests belong to the same ongoing interaction rather than being unrelated tasks.
One task could be "Summarize this article"
Then the second task could be "Now turn that summary into bullet points for a presentation"
These two tasks should share the same sessionId because the second task relies on the first task for additional context on what
the summary is.

29. The parts array supports types text, file, and data. Describe a realistic multi-agent
workflow where all three part types appear in a single conversation.

An example where all three types might appear in a single conversation if they need to provide additional info that is not text
For example:
A user sends a message, "Review this receipt and tell me if it is reimbursable."
They then attach a pdf for the file part which is an image of the receipt.
Another system could then include the data part which could be a JSON containing things like employee ID, expense category, amount

So an agent will first read the file and get the details into a data format, then a policy agent can use the data to figure out if its reimbursable. Then a response agent can turn that information into a human-readable decision.

37. In report.md Section 4, describe: (a) what the --allow-unauthenticated flag does and its
security implications, (b) how Cloud Run scales to zero and what cold start latency
means for A2A clients.

a) --allow-unauthenticated makes the Cloud Run service publicly invokable over HTTPS, so callers do not need Google-authenticated credentials to send requests. This means that anyone who knows the service URL can call the endpoint, so it should avoid exposing sensitive operations or private data unless there are other protections in place.

b) Cloud Run automatically scales the number of instances based on traffic, so when a revision receives no traffic it scales down to zero instances unless a different minimum instances is put. It is cost efficient to scale to zero, but the next incoming request might need to wait for a new container instance to start, which adds the startup delay known as cold start latency. This means the first request after an idle period can be noticeably slower than later requests, so clients should take this into account when deciding timeouts and retries.
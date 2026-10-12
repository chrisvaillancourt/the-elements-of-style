## Summary

This PR basically makes a number of changes to the way that the export job handles retries. In the past, what would happen is that the job would retry all failures, including ones that were never going to succeed, which was wasteful. Now it only retries errors that are actually transient in nature, such as timeouts and 503s.

## Testing

I have tested this locally and it seems to be working as expected for the most part.

# Stacks: what a named tool fills

Seat defaults per tool the runner names. The folder and the runner's answers win over a block. A wiki, Confluence, or Discussions edited in place has no review; a docs folder in the repo passes the PR.

## GitHub
code: the repo at the remote. Reach: `gh`, or the GitHub MCP when connected.
tracker: Issues in the repo; a Project when the team names one. Reach: `gh issue`, `gh project`.
record: the Issue. The thread is split across the Issue, its PRs, and any Discussion; read all three before calling anything open.

## Atlassian
code: Bitbucket or GitHub, whichever the remote names. Reach: the remote.
tracker: Jira, the project key. Reach: the Atlassian MCP when connected.
record: the Jira ticket; its comments are the thread.
docs: the Confluence space, pointed at by space and topic, never page id. Reach: the Atlassian MCP.

## Azure DevOps
code: Repos in the project. Reach: `az repos`.
tracker: Boards, the project and its process template: Issue, User Story, or PBI under Feature under Epic. Reach: `az boards`.
record: the work item; its Discussion is the thread.
docs: the project Wiki, edited in place or published from a `docs/` folder in Repos. Reach: `az devops wiki`.

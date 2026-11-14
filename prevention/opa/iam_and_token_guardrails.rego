package security.artex_prevention

import future.keywords.contains
import future.keywords.if
import future.keywords.in

# Deny long-lived static IAM access keys (starves autonomous agents of persistent credentials)
deny contains msg if {
    resource := input.resource_changes[_]
    resource.type == "aws_iam_access_key"
    msg := sprintf("POLICY VIOLATION [%s]: Static IAM access keys are prohibited. Use short-lived OIDC/STS federation to prevent autonomous agent persistence.", [resource.address])
}

# Deny overly permissive cross-account AssumeRole trust policies without ExternalId or PrincipalOrgID
deny contains msg if {
    resource := input.resource_changes[_]
    resource.type == "aws_iam_role"
    policy := json.unmarshal(resource.change.after.assume_role_policy)
    statement := policy.Statement[_]
    statement.Effect == "Allow"
    statement.Principal.AWS == "*"
    msg := sprintf("POLICY VIOLATION [%s]: Wildcard AWS Principal in AssumeRole trust policy creates immediate lateral movement path for automated recon agents.", [resource.address])
}

# Enforce short TTLs on ephemeral tokens (< 3600 seconds)
deny contains msg if {
    resource := input.resource_changes[_]
    resource.type == "aws_iam_role"
    resource.change.after.max_session_duration > 3600
    msg := sprintf("POLICY VIOLATION [%s]: max_session_duration (%d) exceeds 3600s limit. Short session TTLs disrupt multi-stage agentic attack chains.", [resource.address, resource.change.after.max_session_duration])
}

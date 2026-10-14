# Double-anonymous review checklist

Before exposing an anonymous mirror, verify all of the following:

- [ ] Repository owner and source-organization name are hidden by the anonymization service.
- [ ] Commit author names/emails are not exposed.
- [ ] No author name, affiliation, ORCID, personal email, or personal website appears in text files.
- [ ] No personal GitHub URL or username appears in README/source/configuration files.
- [ ] No absolute local paths (`/Users/...`, `/home/...`, Windows user directories, Documents/Downloads paths) appear in public-facing files.
- [ ] PDF metadata contains no author identity.
- [ ] PNG/image metadata contains no author identity.
- [ ] No issue/PR links point back to the identifiable private repository.
- [ ] No badges reveal the private repository owner or repository slug.
- [ ] Only the anonymous mirror URL is supplied during review.

Note: the original reproducibility log has been retained for provenance. It contains only generic references to `Documents` and `Downloads`, not a user-specific path. If the anonymization service exposes commit history or repository-owner metadata, configure it to suppress those fields.

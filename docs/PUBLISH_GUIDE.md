# Publish Guide: Ledger v0.1

*For after you approve the package. About 40 minutes total. Each step names what to click and what you should see.*

## Copy-ready text

**Title:** Verification Gap Ledger

**Version:** 0.1.0

**Author:** Stephen Olumide Akindipe, ORCID 0000-0002-1846-9662, Independent Researcher, Albany, NY, USA

**Description:**
The Verification Gap Ledger (VGL) is an open versioned register containing federal and New York State programs targeted towards funding municipal energy and infrastructure. For each program, the VGL records three distinct parameters: what verification of results is required (R), what results are actually made publicly available (C), and whether an external party could attribute outcomes to the funding (A). Every rating is directly linked to the exact source document and section. Version 0.1 covers 24 programs with 80 evidence items.

**Keywords:** municipal energy; infrastructure finance; measurement and verification; program evaluation; federal grants; New York State; open data

**Licenses:** CC BY 4.0 (data and documents); MIT (code)

## Step 1: GitHub (10 min, Claude can do this for you)

Option A, Claude pushes it. Create a token at https://github.com/settings/tokens?type=beta (Fine-grained, repository access "All repositories" or the new repo only, permission Contents: Read and write, Administration: Read and write). Paste it to Claude when asked. Claude creates `Olumide-Akindipe/verification-gap-ledger`, pushes, and tags `v0.1.0`. Revoke the token afterward at the same page.

Option B, you do it. At https://github.com/new, name it `verification-gap-ledger`, Public, no README. Then upload the project folder with "uploading an existing file." You should see the README rendered on the repository page.

## Step 2: Zenodo DOI (10 min)

1. Log in at https://zenodo.org with your GitHub account.
2. Top right menu, **GitHub**. Find `verification-gap-ledger` and flip the switch to On.
3. On GitHub, open the repository, **Releases**, **Draft a new release**, tag `v0.1.0`, title "Verification Gap Ledger v0.1.0", paste the description, **Publish release**.
4. Within a few minutes Zenodo shows a new record. It has two DOIs: one for this version and a "concept" DOI that always points to the latest version. **Use the concept DOI on your CV.**
5. Edit the Zenodo record: add your ORCID to the creator, set license to CC BY 4.0, add the keywords. Save and publish.
6. Tell Claude both DOIs. It adds the DOI to the README, citation file and report, and re-releases the README and citation file.

## Step 3: FAIRsharing record (20 min, after the DOI exists)

1. Go to https://fairsharing.org and sign in with ORCID.
2. Choose to add a new record of type **Database**.
3. Paste the title, description, and keywords above. Homepage: the GitHub URL. Add the concept DOI. Subject areas: energy, public policy, environmental science. License: CC BY 4.0. Maintainer: you, with ORCID.
4. Submit. FAIRsharing curators review new records; you may receive questions by email. Save the record URL when it is approved.

## Step 4: re3data (not now)

re3data lists data repositories, not individual datasets. Revisit at v2.0 only if the Ledger is then hosted as its own searchable repository.

## After each step

Record the date, URL or DOI, and a screenshot in your evidence log the same day. Items not logged the day they happen are the ones that go missing at petition time.

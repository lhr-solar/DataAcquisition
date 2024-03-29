# Quality Assurance Checklist 
To make reviews more efficient, please make sure the software feature meets the following standards and check everything off that meets the quality check. Once everything has been checked, the assigned reviewers will begin the review process. 

There are exceptions with all guidelines. As long as your decisions are justified, then you are good! Contact the reviewers or the leads about any exceptions. 

## Requirements 
- [ ] Followed Coding Style Guide
    - [ ] Reviewed and addressed all PyLint messages
    - [ ] Ran autopep8
- [ ] Code Build checks pass 
- [ ] No merge conflicts
    - [ ] Updated main branch is merged in
- [ ] Software feature has associated unit test
- [ ] Software feature has updated documentation
- [ ] If applicable, software feature has simulation test associated with it (.json & out.json file)
- [ ] Test provides useful information and uses relevant data to accurately represent Data Acquisition system
    - NOTE: If test file already exists, use that one 
- [ ] 2 Members of the team have already reviewed my PR 
    - NOTE: Approver will not look at PR if 2 other members haven't reviewed first 
- [ ] Did you Have Fun?

## Things to Consider 
- [ ] Even if the above are checked, is this the best way of writing my code? 
    - It's possible to write code that works, but are there ways to make code more efficient? 
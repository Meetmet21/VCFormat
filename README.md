# VCFormat
## Description
A simple script to add sample and associated genotypes information to vcf file or vcf.gz file.
## Plan
### Class read:
1. Get metadata
   - [X] Read vcf with file handler
   - [X] Convinient data structure to get different vcf format fields as INFO, FILTER, etc and easy access
   - [X] Get header
2. Get records
   - [X] Convinient data structure to seperate each columns value as CHR, ID, REF..etc
3. Formating functions
   - [ ] add_FORMAT_to_metadata -> metadata
   - [ ] add_FORMAT_to_header -> header
   - [ ] add_SAMPLE_to_header -> header
   - [ ] update_record -> update record with the NEW FORMAT and sample Genotype informations
### Class write:
1. Updat metadata and header:
   - [ ] Open output vcf with wright rights with file handler
   - [ ] update_description -> write updated metadata and header
3. Update records with new sample informations
   - [ ] Write current record

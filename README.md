# VCFormat

## Plan
1. Class read:
   1.1 Get metadata
     1.1.1 Convinient data structure to get different vcf format fields as INFO, FILTER, etc and easy access
     1.1.2 Get header and fill lacking headers
   1.2 Get records
     1.2.1 Convinient data structure to seperate each columns value as CHR, ID, REF..etc
   1.3 Formating functions
     1.3.1 Function to format different header fields and add to current header
       1.3.1.1 add_INFO
       1.3.1.2 add_FILTER
       1.3.1.3 add_FORMAT
       1.3.1.4 add_contig
       1.3.1.5 add_ALT
       1.3.1.6 add_SAMPLE
       1.3.1.7 add_metadata -> reference, fileformat, filedate, source
2. Class write:

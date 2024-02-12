# DESCRIPTION
# Class to read vcf file and extract different data in appropriate data structures
# This program follows the VCF specification v4.4 https://samtools.github.io/hts-specs/VCFv4.4.pdf

# MODULES
import re

# VARIABLES

# CLASS
class Reader:
    def __init__(self, vcf_path):
        # VCF file name
        self.filepath = vcf_path
        # Get header
        self.header = self.get_header()
        # Get metadata
        self.metadata = self.get_metadata()
        # Get records
        self.records = self.get_records()

    # Extract header in a list
    def get_header(self) -> list:
        """
        Extract header from object (vcf) and split each column from string.
        :return: list of names in header
        """
        with open(self.filepath, 'r') as file:
            for line in file.readlines():
                # Line with one '#' is the header
                if line.startswith('#CHROM'):
                    return line.strip().split("\t")

    def get_metadata(self) -> dict:
        """
        Extract metadata information from object (vcf) to appropriate keys in a dict
        :return: Dict of keys corresponding to vcf metadata title, each key contains list of values
        """
        # Dict of metadata fields
        Dict = {
            "fileformat": [],
            "fileDate": [],
            "reference": [],
            "phasing": [],
            "INFO": [],
            "FILTER": [],
            "FORMAT": [],
            "ALT": [],
            "asssembly": [],
            "contig": [],
            "SAMPLE": [],
            "PEDIGREE": [],
        }
        # Assign to appropriate list each key values in metadata
        with open(self.filepath, 'r') as file:
            for line in file.readlines():
                # Look only at metadata
                if line.startswith("##"):
                    # Extract field mame in between ## and = sign
                    field = re.findall(r"##(\w+)?=", line)[0]
                    # Add field value from line to corresponding key in Dict
                    Dict[field].append(line.strip())

        return Dict

    def get_records(self) -> list[dict]:
        """
        Extract from object (vcf) all records. Assign each header name to the records information.
        :return: List of dicts containing for each list item, a record as dict with key-values corresponding to header.
        """
        # List containing each record dict
        out = []
        # Read object
        with open(self.filepath, 'r') as file:
            for line in file.readlines():
                # Ignore metadata
                if not line.startswith("#"):
                    # Remove '\n' at the end split each columns values
                    record = line.strip().split()
                    # Check if all header fields are present in record
                    if len(self.header) == len(record):
                        # Match each name to value in dict
                        match = {self.header[it]: record[it] for it in range(len(self.header))}
                        # Add to out
                        out.append(match)
                    else:
                        print("Header field missing in record.")
                        exit(1)

        return out

    def add_new_FORMAT(self, fid, fnumber, ftype, fdescription):
        """
        Add to metadata new FORMAT tag information, update records FORMAT section
        :return: New FORMAT in metadata and records
            :param fid: FORMAT ID
            :param fnumber: FORMAT Number
            :param ftype: FORMAT Type
            :param fdescription: FORMAT Description
        """
        # Construct well formatted new FORMAT
        metadata_FORMAT = (f"##FORMAT=<ID={fid},Number={str(fnumber)},"
                      f"Type={ftype},Description=\"{fdescription}\">")
        # Extend FORMAT metadata
        self.metadata["FORMAT"].append(metadata_FORMAT)
        # Check if FORMAT exists in header
        if "FORMAT" not in self.header:
            # Add to header
            self.header.append("FORMAT")
            # Add fid to records
            for index in range(len(self.records)):
                self.records[index]["FORMAT"] = fid
            # Track number of tag in FORMAT
            num_tag = 1
        else:
            # Add new_id to records
            for index in range(len(self.records)):
                self.records[index]["FORMAT"] += f":{fid}"
            # Track number of tag in FORMAT
            num_tag = len(self.records[0]["FORMAT"].split(":"))

        print(f"Check if samples values correspond to new FORMAT field tags."
              f"\nCurrent number of tags in FORMAT field is {num_tag}.")

    def add_sample(self, id="NA", assay="NA", ethnicity="NA", disease="NA", tissue="NA", description="NA", tags_value = None):
        """
        Add sample information, according to VCF v4.4 specifications, to metadata, header and records.
        :param id: Sample id
        :param assay: Sample source technics
        :param ethnicity: Source individual ethnicity
        :param disease: Source individual disease
        :param tissue: Sample tissue source
        :param description: Sample description
        :param tags_value: Value of current FORMAT tags for sample. Expected value is a list
                containing tags values in string separated by ':' for each record following the vcf order
        :return: Formatted sections to new samples.
        """
        # Check if FORMAT exists before adding sample information
        if "FORMAT" not in self.header:
            print("The FORMAT field is missing in header. Fix it before adding sample information.")
            exit(1)

        metadata_sample = (f"##SAMPLE=<ID={id},Assay={assay},"
                           f"Ethnicity={ethnicity},Disease={disease},"
                           f"Tissue={tissue},Description=\"{description}\">")

        # Add new to metadata
        self.metadata["SAMPLE"].append(metadata_sample)
        # Add new to header
        self.header.append(id)

        # Treat provided tags value for sample
        if tags_value is not None:
            # Missing records
            if len(tags_value) != len(self.records):
                print(f"Records: {len(self.records)}. Records are missing from Sample.")
                exit(1)
            # Go through records
            else:
                # Add to each record corresponding tag values for sample
                for index in range(len(self.records)):
                    # Missing tags
                    if len(str(tags_value[index]).split(":")) != len(self.records[index]["FORMAT"].split(":")):
                        print(
                            f"Number of tags: {len(self.records[0]['FORMAT'].split(':'))}. "
                            f"Few tags are missing from sample at line {index + 1}. "
                            f"Tags should be separated by ':'.")
                        exit(1)
                    else:
                        self.records[index][id] = tags_value[index]
        # No tag values provided
        else:
            print("Tag values set to 1 for all records and all tags")
            for index in range(len(self.records)):
                self.records[index][id] = re.sub(r"\w+", '1', self.records[index]["FORMAT"])




